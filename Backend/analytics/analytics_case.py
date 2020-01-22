from .analytics_utils import AnalyticsUtils
from feedbacks.models import Feedback
from cases.models import Case
from cases.mobile_api.serializers import CaseSerializer
import pandas as pd
import numpy as np
from datetime import date


class CaseEvalEngine(object):
    def __init__(self, case):
        self.case = case
        self.org_id = case.organization_id
        self.born = case.child.date_of_birth
        try:
            self.main_fact = Feedback.objects.get(case=case.id, is_main=True)
        except:
            self.main_fact = None

    def __calculate_age(self, born):
        born_date = self.born
        # born = datetime.strptime(born_date, "%d.%m.%Y").date()
        today = date.today()
        return today.year - born_date.year - ((today.month, today.day) < (born_date.month, born_date.day))

    def compute_max_dist_travelled(self):
        inifact = self.main_fact
        dist = None
        if inifact:
            au = AnalyticsUtils()
            dist = au.getDistanceTravelled(then=inifact.date, speed="default")
        return dist

    def get_past_cases(self):
        c = self.case
        org_id = c.organization_id
        # Add code for clustering on runtime
        org_closed_cases = (
            Case.objects.filter(organization=org_id, status__in=["closed", "archived"])
            .select_related("child")
            .values(
                "id",
                "organization_id",
                "has_money_or_credit",
                "has_mobile_phone",
                "has_area_knowledge",
                "disappearance_reasons",
                "addiction",
                "mental_disorders",
                "psychological_disorders",
                "physical_disabilities",
                "is_refugee",
                "is_high_risk",
                "child__date_of_birth",
                "child__gender",
            )
        )
        df = pd.DataFrame.from_records(org_closed_cases)
        df["age"] = df["child__date_of_birth"].apply(self.__calculate_age)
        df.fillna("Unknown", inplace=True)
        return df

    def fetch_similar_closed_cases(self, limit=None):
        c = self.case
        df_c = pd.DataFrame([[c.id, c.child.date_of_birth]], columns=["id", "child__date_of_birth"])
        df_c["age"] = df_c["child__date_of_birth"].apply(self.__calculate_age)
        # Perfom cluster training on past data
        df_past = self.get_past_cases()
        au = AnalyticsUtils()
        # Perfom cluster training on current data
        km = au.get_kmeans_clusters(df_past[["id", "age"]].values, 2)
        print(km.cluster_centers_)
        labels = km.labels_
        # Find which cluster the case belongs
        # c_1 = np.array(df_c[['id','age']])
        pred = km.predict(df_c[["id", "age"]].values)  # c_1.reshape(-1,len(c_1)))
        # Format results as a DataFrame
        results = pd.DataFrame([df_past["id"], labels]).T
        print(results)
        print(pred)
        # Return top X cases of that cluster
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
            df_c = df_c[:limit]
        return df_c

    def get_gomissing_proba(self):
        c = self.case
        proba = 0.5
        if c.status == "inactive":
            pass
        else:
            pass

        return proba
