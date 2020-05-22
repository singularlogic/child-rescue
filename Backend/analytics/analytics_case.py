# import numpy as np
import pandas as pd

# from cases.web_admin_api.serializers import CasesSerializer
from places.models import Place
from feedbacks.models import Feedback
from cases.models import Case
from joblib import load  # , dump

# from datetime import date
from .analytics_utils import (
    obj2df,
    queryset2df,
    calculate_age,
    normalize_age,
    get_dummies_df,
    getDistanceTravelled,
    getDuration,
    values2df,
    get_n_neighbors_model,
    get_geopoint_clusters,
    find_cluster_centroid,
    list_to_nparray,
    calculate_initial_compass_bearing,
    getEndpoint,
)
from .analytics_pois_routes import PlaceEvalEngine
from .analytics_apis import EventfulAPI, FoursquareAPI, OpenWeatherAPI
from django.conf import settings

GO_MISSING_MODEL = settings.ML_DIR + "global_gomissing_model_rf01.joblib"
LOST_MODEL = settings.ML_DIR + "global_lost_model_rf01.joblib"
RUNAWAY_MODEL = settings.ML_DIR + "global_runaway_model_rf01.joblib"
PARENTAL_MODEL = settings.ML_DIR + "global_parental_model_rf01.joblib"
THIRDPARTY_MODEL = settings.ML_DIR + "global_thirdparty_model_rf01.joblib"
UAM_MODEL = settings.ML_DIR + "global_uam_model_rf01.joblib"
ORIGINAL_FEATS = settings.ML_DIR + "original_df.pkl"
ORIGINAL_FEATS_MISS = settings.ML_DIR + "original_miss_df.pkl"
MAIN_RADIUS_MAX = 20.0  # km
MAIN_RADIUS_MIN = 0.2  # km
MAX_DIST_TRAVELLED_ACCEPTED = 60  # km
R_DEF = 1  # km
# We need to add age, gender from child +  curr_days_diff from main_fact
# Add also tag, distance from each place
# For past cases we use final days_diff & distance_found & tag_found
PROFILING_FIELDS = [
    "id",
    "has_money_or_credit",
    "has_mobile_phone",
    "has_area_knowledge",
    "disappearance_reasons",
    "living_environment",
    "triggered_event",
    "concerns",
    "school_grades",
    "addiction",
    "mental_disorders",
    "psychological_disorders",
    "physical_disabilities",
    "medical_treatment_required",
    "is_refugee",
    "is_high_risk",
    "is_first_time_missing",
    "has_trafficking_history",
    "legal_status",
    "relationship_status",
    "disappearance_type",
]

FIND_TYPE_FIELDS = [
    "age",
    "gender",
    "disappearance_reasons",
    "living_environment",
    "triggered_event",
    "concerns",
    "addiction",
    "mental_disorders",
    "psychological_disorders",
    "physical_disabilities",
    "is_refugee",
    "is_first_time_missing",
    "legal_status",
    "relationship_status",
    "disappearance_type",
]

GOMISSING_FIELDS = [
    "age",
    "gender",
    "living_environment",
    "psychological_disorders",
    "addiction",
    "legal_status",
    "has_trafficking_history",
    "relationship_status",
    "disappearance_type",
]

SIMILAR_CASES_FIELDS = [
    "age",
    "gender",
    "disappearance_reasons",
    "living_environment",
    "triggered_event",
    "concerns",
    "school_grades",
    "addiction",
    "mental_disorders",
    "psychological_disorders",
    "physical_disabilities",
    "is_refugee",
    "is_high_risk",
    "is_first_time_missing",
    "has_trafficking_history",
    "relationship_status",
]

IPOI_FIELDS = [
    "age",
    "gender",
    "triggered_event",
    "disappearance_reasons",
    "is_first_time_missing",
    "living_environment",
    "mental_disorders",
    "physical_disabilities",
    "addiction",
    "is_refugee",
    "curr_days_diff",
]


class ProfileEvalEngine(object):
    def __init__(self, case_obj):
        self.case = case_obj
        self.preds = {
            "lost": None,
            "parental": None,
            "runaway": None,
            "thirdparty": None,
            "uam": None,
            "gomissing": None,
            "repeat": None,
        }
        df = obj2df(case_obj)
        df = df.loc[:, PROFILING_FIELDS]
        df = df.fillna("Unknown")
        df["age"] = pd.Series(data=None, dtype=float)
        df["gender"] = pd.Series(data=None, dtype=str)
        df["curr_days_diff"] = pd.Series(data=None, dtype=float)
        if case_obj.child:
            df.at[0, "age"] = calculate_age(case_obj.child.date_of_birth)
            df.at[0, "gender"] = case_obj.child.gender
            df["age"] = df["age"].apply(normalize_age)
        self.max_dist = None
        self.df_columns = None
        self.main_fact = None
        self.main_coords_str = None
        try:
            main_fact = Feedback.objects.filter(case=case_obj.id, is_main=True).first()
            if main_fact:
                self.main_fact = main_fact
                self.max_dist = getDistanceTravelled(then=main_fact.date, speed="auto")
                df.at[0, "curr_days_diff"] = getDuration(then=main_fact.date, interval="days")
                self.main_coords_str = "{}, {}".format(str(main_fact.latitude), str(main_fact.longitude))
            else:
                raise Exception("No main fact for case {}".format(str(case_obj.id)))
        except ValueError:
            self.max_dist = None
        # Create input pattern df for case data
        self.case_df = df

    def get_past_cases_df(self):
        c = self.case
        try:
            # Add code for clustering on runtime
            query_cases = (
                Case.objects.filter(organization=c.organization_id, status__in=["closed", "archived"])
                .select_related("child")
                .order_by("child", "-created_at")
                .distinct("child")
            )
            # org_closed_cases = query_cases.distinct('child_id').order_by('created_at')
            df = queryset2df(query_cases)
            df.fillna("Unknown", inplace=True)
            df["age"] = pd.Series()
            df["gender"] = pd.Series(dtype=str)
            df["age"] = values2df(query_cases.values("child__date_of_birth"))
            df["age"] = df["age"].apply(calculate_age)
            df.loc[:, "age"] = df.loc[:, "age"].apply(normalize_age)
            df["gender"] = values2df(query_cases.values("child__gender"))
        except ValueError:
            df = pd.DataFrame()
        return df

    def fetch_similar_closed_cases(self, limit=4):
        df_c = self.case_df.copy()
        # limit test
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int"
            if limit < 1:
                raise ValueError("'limit' must be greater than zero")

        # Perfom cluster training on past data
        df_past = self.get_past_cases_df()
        if not df_past.empty and df_past.shape[0] > 0:
            df_cluster_features = df_past[SIMILAR_CASES_FIELDS].copy()
            df_cluster_features = get_dummies_df(df_cluster_features)

            # in case the available cases are fewer than the limit, bring all
            if df_past.shape[0] < limit:
                limit = df_past.shape[0]

            # Perfom kNN clustering on current data
            nbrs = get_n_neighbors_model(df_cluster_features, n_neighbors=limit)
            # Construct new input
            df_new = pd.get_dummies(df_c)
            X = df_new.reindex(columns=df_cluster_features.columns, fill_value=0).values
            # get the index
            neighbor_index = nbrs.kneighbors(X, return_distance=False)
            # get the rows of the dataframe
            cases_rows_df = df_past.iloc[neighbor_index[0], :]
            return cases_rows_df["id"].values.tolist()
        else:
            raise Exception("No past cases in database")

    def get_missingcats_preds(self):
        c = self.case
        df_c = self.case_df.copy()
        preds = self.preds
        # Select appropriate input (for the field names check initial lists)
        input_df = df_c[FIND_TYPE_FIELDS]
        df1 = pd.get_dummies(input_df)
        # Expand dummies based on original df
        unpickled_df = pd.read_pickle(ORIGINAL_FEATS)
        new_input_df = df1.reindex(columns=unpickled_df.columns, fill_value=0)
        new_input = new_input_df.values
        # Make predictions per class by loading appropriate model
        if c.status == "active":
            with open(LOST_MODEL, "rb") as m1:
                model_lost = load(m1)
                preds["lost"] = model_lost.predict_proba(new_input)[0][1]
            with open(PARENTAL_MODEL, "rb") as m2:
                model_parental = load(m2)
                preds["parental"] = model_parental.predict_proba(new_input)[0][1]
            with open(RUNAWAY_MODEL, "rb") as m3:
                model_runaway = load(m3)
                preds["runaway"] = model_runaway.predict_proba(new_input)[0][1]
            with open(UAM_MODEL, "rb") as m4:
                model_uam = load(m4)
                preds["uam"] = model_uam.predict_proba(new_input)[0][1]
        else:
            preds["lost"] = None
            preds["parental"] = None
            preds["runaway"] = None
            preds["uam"] = None
            preds["thirdparty"] = None

    def get_gomissing_proba(self):
        c = self.case
        df_c = self.case_df.copy()
        preds = self.preds

        # Select appropriate input
        input_df = df_c[GOMISSING_FIELDS]
        df1 = pd.get_dummies(input_df)
        # Expand dummies based on original df
        unpickled_df = pd.read_pickle(ORIGINAL_FEATS_MISS)
        new_input_df = df1.reindex(columns=unpickled_df.columns, fill_value=0)
        new_input = new_input_df.values
        # Make prediction about probability of disappearance for hosting refugees (need days stayed?)
        if c.status == "inactive":
            with open(GO_MISSING_MODEL, "rb") as gmp:
                model_runaway = load(gmp)
                preds["gomissing"] = model_runaway.predict_proba(new_input)[0][1]
        else:
            preds["gomissing"] = None

    def get_profiling_preds_json(self):
        self.get_missingcats_preds()
        self.get_gomissing_proba()
        return self.classifier_results_to_json(self.preds)

    def classifier_results_to_json(self, res_dict=None):
        results_schema = {
            "profiling": {
                "missing_type": {
                    "lost": res_dict["lost"],
                    "parental": res_dict["parental"],
                    "runaway": res_dict["runaway"],
                    "thirdparty": res_dict["thirdparty"],
                    "uam": res_dict["uam"],
                },
                "gomissing_prob": res_dict["gomissing"],
                "repeat_prob": res_dict["repeat"],
            }
        }
        return results_schema

    def get_venues_from_socialnetworks_apis(self, radius=10):
        loc_coords = self.main_coords_str
        print(loc_coords)
        if loc_coords:
            list_places = []
            # Connect to APIs
            # 1 EVENTFUL
            ev = EventfulAPI(loc_coords)
            list_places.extend(ev.get_weekly_picks(c_radius=radius))
            # 2 FOURSQUARE
            foursq = FoursquareAPI(loc_coords)
            list_places.extend(foursq.get_top_picks(c_radius=radius * 1000, c_lim=5))
            return list_places
        else:
            raise Exception("No location given.")

    def suggest_radius_for_mainfact(self):
        radius = self.max_dist
        if radius and radius > MAIN_RADIUS_MAX:
            radius = MAIN_RADIUS_MAX  # in km
        return radius

    def find_mode_transport_with_rules(self, lat1, lng1):
        mode_trans = "foot"  # default value
        c = self.case
        # Check with weather api first
        try:
            owmapi = OpenWeatherAPI()
            w = owmapi.get_weather(lat=lat1, lng=lng1)
            ws = w.get_status()
            # If bad weather , take transport
            if ws == "Thunderstorm" or ws == "Rain" or ws == "Snow" or ws == "Drizzle":
                mode_trans = "transp"
        except Exception:
            pass
        # If has money or area knowledge, travels faster
        if (c.has_area_knowledge and c.has_area_knowledge == "yes") or (
            c.has_money_or_credit and c.has_money_or_credit == "yes"
        ):
            mode_trans = "transp"
        return mode_trans

    def evaluate_non_fact_places(self):
        # Initial places are those places NOT coming from Feedback
        # Get all places
        c = self.case
        df_c = self.case_df
        data = {}
        input_df = df_c[IPOI_FIELDS].copy()
        input_df["destination_poi_tag"] = pd.Series(data=None, dtype=str)
        prob_destinations = Place.objects.filter(case_id=c.id).exclude(source="facts").exclude(is_event=True)
        if prob_destinations.exists():
            # input_df["destination_poi_tag"] = pd.Series(dtype=str)
            input_df.rename(columns={"curr_days_diff": "days_diff"}, inplace=True)
            # Include only those not so far away
            for place in prob_destinations:
                eval_p = 0.0
                peng = PlaceEvalEngine(place)
                if peng.is_within_travel_distance():
                    data["rad"] = R_DEF
                    data["lat"] = place.latitude
                    data["lng"] = place.longitude
                    # Add POI tag to case_df (days_diff already included)
                    input_df.at[0, "destination_poi_tag"] = place.tag
                    # For each place compute probability
                    eval_p = peng.compute_proba(input_df)
                    data["prob"] = eval_p
                # Update place data
                peng.update_place(eval_p, data)
        # else:
        # raise Exception("No initial places to evaluate.")

    def get_most_recent_feedback(self, cluster_list, f_pois):
        object_ids = []
        for point in cluster_list:
            place_id = point[2]
            place = f_pois.get(pk=place_id)
            object_ids.append(place.feedback_id)
        result = Feedback.objects.filter(id__in=object_ids).order_by("-date")[:1]
        return result[0]

    def evaluate_fact_places(self):
        # Get all F-POIs (places coming from Feedback)
        c = self.case
        data = {}
        # prob_destinations = Place.objects.filter(case_id=c.id).exclude(source="facts")
        f_pois = Place.objects.filter(case_id=c.id, source="facts")
        if f_pois and f_pois.exists():
            count = f_pois.count()

            # CROWD SOURCING FIRST. ONLY WITH PROBABILITIES.
            # Assign initial probability and radius based on population.
            # More pois, less proba, bigger radius
            init_eval_p = 1 / (count + 1)
            init_search_radius = R_DEF / init_eval_p

            # Extract coords as np array
            vlqs = f_pois.values_list("latitude", "longitude", "id")
            mylist = list(vlqs)
            f_points = list_to_nparray(mylist)

            # Find clusters of points within initial search radius
            clusters = get_geopoint_clusters(f_points, init_search_radius)
            print(clusters)
            # Process each cluster to get centroid and radius
            for cluster in clusters:
                centroid = find_cluster_centroid(cluster)
                new_eval_p = init_eval_p * len(cluster)
                new_eval_r = R_DEF / new_eval_p
                if new_eval_r < MAIN_RADIUS_MIN:
                    new_eval_r = MAIN_RADIUS_MIN
                elif new_eval_r > MAIN_RADIUS_MAX:
                    new_eval_r = MAIN_RADIUS_MAX

                for point in cluster:
                    place_id = point[2]
                    place = f_pois.get(pk=place_id)
                    peng = PlaceEvalEngine(place)

                    # ROUTE ESTIMATION. ADDING TIME AND SPEED AND DIRECTION.
                    # if place is single,then is easy. Find related feedback and its time.
                    if len(cluster) == 1:
                        most_recent_feedback = place.feedback
                    # if places are many, take more recent feedback
                    elif len(cluster) > 1:
                        most_recent_feedback = self.get_most_recent_feedback(cluster, f_pois)
                    # Find datetime the child was sighted
                    time_observed = most_recent_feedback.date
                    # print(time_observed)
                    # Find Bearing of Line between two points (main fact and cluster centre)
                    cluster_lat = centroid[0]
                    cluster_lng = centroid[1]
                    if self.main_fact:
                        main_lat = self.main_fact.latitude
                        main_lng = self.main_fact.longitude
                    else:
                        raise Exception("Main fact is missing for this case")
                    bearing = calculate_initial_compass_bearing((main_lat, main_lng), (cluster_lat, cluster_lng))
                    # Set Mode of Transport in order to compute speed
                    if most_recent_feedback.transportation:
                        # 1. first use feedback's data
                        mtf = most_recent_feedback.transportation
                        if mtf == "bus_tram" or mtf == "metro_subway":
                            mode_trans = "transp"
                        elif mtf == "car_motorcycle" or mtf == "train":
                            mode_trans = "auto"
                        elif mtf == "ship_aeroplane":
                            mode_trans = "air"
                        elif mtf == "bicycle_scooter":
                            mode_trans = "bike"
                        else:
                            mode_trans = "foot"
                    else:
                        # 2. if 1 is null, use rule-base
                        mode_trans = self.find_mode_transport_with_rules(cluster_lat, cluster_lng)  # default foot
                    # Compute distance travelled based on speed
                    dist_t = getDistanceTravelled(time_observed, speed=mode_trans)
                    # Have a cut-off threshold
                    if dist_t >= MAX_DIST_TRAVELLED_ACCEPTED:
                        dist_t = MAX_DIST_TRAVELLED_ACCEPTED
                    print(bearing)
                    # Extend line  to find End point
                    end_lat, end_lng = getEndpoint(cluster_lat, cluster_lng, bearing, dist_t)
                    new_alert_r = dist_t
                    # Assign new values in data field and save
                    # search area data
                    data["rad"] = new_eval_r
                    data["lat"] = cluster_lat
                    data["lng"] = cluster_lng
                    data["prob"] = new_eval_p
                    # alert area data
                    data["arad"] = new_alert_r
                    data["alat"] = end_lat
                    data["alng"] = end_lng
                    data["atrans"] = mode_trans

                    peng.update_place(new_eval_p, data)
