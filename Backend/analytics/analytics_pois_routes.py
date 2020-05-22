import pandas as pd

from feedbacks.models import Feedback
from django.db import Error
from django.conf import settings

# from django.conf import settings
# from sklearn import preprocessing
from joblib import load
from .analytics_utils import (
    getDistance,
    compute_dist_diff_km,
    get_geopoint_clusters
)  # , getDistanceTravelled, getDuration

RADIUS_MIN = 0.1  # km
RADIUS_DEFAULT = 0.5  # km
RADIUS_MAX = 20.0  # km
NEAR_RANGE = 1.0
CITY_RANGE = 8.0
REGION_RANGE = 50.0
NATION_RANGE = 500.0
RANGE_LABELS = ["neighbourhood_range", "city_range", "region_range", "national_range", "international_range"]
ORIGINAL_FEATS_IPOIS = settings.ML_DIR + "original_ipoi_df.pkl"
IPOI_MODEL = settings.ML_DIR + "global_ipoi_model_rf01.joblib"


class PlaceEvalEngine(object):
    def __init__(self, place):
        self.place = place
        self.case_id = None
        self.org_id = None
        self.main_dist = None
        if place:
            self.case_id = place.case_id
            self.org_id = place.case.organization_id
            try:
                self.main_fact = Feedback.objects.get(case=place.case_id, is_main=True)
            except Error():
                self.main_fact = None

    def compute_place_dist_from_main(self, inifact=None):
        inifact = self.main_fact
        place = self.place
        if inifact:
            point1 = (place.latitude, place.longitude)
            point2 = (inifact.latitude, inifact.longitude)
            self.main_dist = getDistance(point1, point2)

    def is_within_travel_distance(self):
        inifact = self.main_fact
        curplace = self.place
        point1 = (inifact.latitude, inifact.longitude)
        point2 = (curplace.latitude, curplace.longitude)
        ddiff = compute_dist_diff_km(inifact.date, point1, point2)
        # print("ddif: %f" % ddiff)
        return ddiff > 0

    def compute_proba(self, df_features):
        preds_list = self.initial_poi_classifier_execute(df_features)
        pr = 0
        # result order: ['city_range', 'international_range', 'national_range', 'neighbourhood_range', 'region_range']
        if self.main_dist and self.main_dist <= NEAR_RANGE:
            pr = preds_list[3]
        elif self.main_dist and self.main_dist <= CITY_RANGE:
            pr = preds_list[0]
        elif self.main_dist and self.main_dist <= REGION_RANGE:
            pr = preds_list[4]
        elif self.main_dist and self.main_dist <= NATION_RANGE:
            pr = preds_list[2]
        else:
            pr = preds_list[1]
        return pr

    def get_dist_category(self, dist=None):
        if not dist:
            dist = self.main_dist
        label = None
        # distance in kilometers
        if dist and dist <= NEAR_RANGE:
            label = RANGE_LABELS[0]
        elif dist and dist <= CITY_RANGE:
            label = RANGE_LABELS[1]
        elif dist and dist <= REGION_RANGE:
            label = RANGE_LABELS[2]
        elif dist and dist <= NATION_RANGE:
            label = RANGE_LABELS[3]
        elif dist and dist > NATION_RANGE:
            label = RANGE_LABELS[4]
        return label

    def create_dataset(self, training=False):
        if training:
            # Get all final places from DB or from anonymised df
            pass
        else:
            # p = self.place
            pass
        return 0  # df_merged

    def initial_poi_classifier_train(self, df):
        # Create dataset
        # le = preprocessing.LabelEncoder()
        # df_labels = le.fit_transform(df["Distance"])
        # df_labels

        # Train classifier

        # Save model (separately for each organisation)
        pass

    def initial_poi_classifier_execute(self, df_features):  # TO-DO
        # convert to model input
        df1 = pd.get_dummies(df_features)
        # Expand dummies based on original df
        unpickled_df = pd.read_pickle(ORIGINAL_FEATS_IPOIS)
        new_input = df1.reindex(columns=unpickled_df.columns, fill_value=0)
        # Load model
        with open(IPOI_MODEL, "rb") as f2:
            ml_model = load(f2)
        # return prediction list
        preds = ml_model.predict_proba(new_input.values)
        return preds[0]

    def results_to_json(self, res_dict):
        results_schema = {
            "search_area": {
                "latitude": res_dict["lat"] if "lat" in res_dict else None,
                "longitude": res_dict["lng"] if "lng" in res_dict else None,
                "radius": res_dict["rad"] if "rad" in res_dict else None,
                "probability": res_dict["prob"] if "prob" in res_dict else None,
            },
            "alert_area": {
                "latitude": res_dict["alat"] if "alat" in res_dict else None,
                "longitude": res_dict["alng"] if "alng" in res_dict else None,
                "radius": res_dict["arad"] if "arad" in res_dict else None,
                "transport": res_dict["atrans"] if "atrans" in res_dict else None,
            }
        }
        return results_schema

    def update_place(self, eval, data_dict=None):
        place = self.place
        place.evaluation = eval
        if data_dict:
            place.data = self.results_to_json(data_dict)
        try:
            place.save()
            print('*** Place updated ***')
        except Error():
            raise Exception('*** Place failed to update ***')

