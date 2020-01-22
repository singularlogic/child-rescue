# Prerequisites for postgresql DB:

import os

from cases.models import Child
from feedbacks.models import Feedback
from django.conf import settings

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier

import pickle
import pandas as pd
from datetime import datetime
from .analytics_utils import AnalyticsUtils


class IntelliSearch(object):
    def __init__(self):
        from django.db import connection

        self.conn = connection

    def run_rawsql_namesearch(self, full_name_str, org_id, type="LEVENSHTEIN", thres=11, limit=10):
        from django.db import Error

        connection = self.conn
        rows = []
        lev_threshold = thres
        sim_threshold = 0.25
        try:
            with connection.cursor() as cursor:
                if type == "DMETAPHONE":  # double metaphone similarity (only for latin)
                    cursor.execute(
                        'SELECT  child.id, first_name, last_name, c.id AS case_id, c.status AS case_status, \
                        SIMILARITY( DMETAPHONE_ALT(concat_ws(\' \', first_name, last_name)), DMETAPHONE_ALT(%s) ) AS SIM FROM child \
                        INNER JOIN "case" AS c  ON (child.id = c.child_id) \
                        WHERE c.organization_id = %s AND c.created_at = (SELECT MAX(created_at) FROM "case" WHERE child_id = child.id)\
                        ORDER BY SIM DESC LIMIT %s',
                        [full_name_str, str(org_id), str(limit)],
                    )
                    rows = cursor.fetchall()
                elif type == "LEVENSHTEIN":  # Levenshtein distance (works well for all)
                    cursor.execute(
                        "SELECT  child.id, first_name, last_name, c.id AS case_id, c.status AS case_status, \
                        LEVENSHTEIN(concat_ws(' ', first_name, last_name), %s) AS LEV FROM child \
                        INNER JOIN \"case\" AS c  ON (child.id = c.child_id) \
                        WHERE LEVENSHTEIN(concat_ws(' ', first_name, last_name), %s) <= %s \
                        AND c.organization_id = %s AND c.created_at = (SELECT MAX(created_at) FROM \"case\" WHERE child_id = child.id)\
                        ORDER BY LEV ASC LIMIT %s",
                        [full_name_str, full_name_str, str(lev_threshold), str(org_id), str(limit)],
                    )
                    rows = cursor.fetchall()
                else:  # trigram similarity
                    cursor.execute(
                        "SELECT  child.id, first_name, last_name, c.id AS case_id, c.status AS case_status, \
                        SIMILARITY(concat_ws(' ', first_name, last_name), %s) AS SIM FROM child \
                        INNER JOIN \"case\" AS c  ON (child.id = c.child_id) \
                        WHERE SIMILARITY(concat_ws(' ', first_name, last_name), %s) > %s \
                        AND c.organization_id = %s AND c.created_at = (SELECT MAX(created_at) FROM \"case\" WHERE child_id = child.id)\
                        ORDER BY SIM DESC LIMIT %s",
                        [full_name_str, full_name_str, str(sim_threshold), str(org_id), str(limit)],
                    )
                    rows = cursor.fetchall()
        except Error as e:
            print("Connection error: %s" % e.__cause__)
        return rows


# User Ranking
# Roles: Anonymous, Registered, Volunteer, Other
# Note 1: a simple user usually participates in any missing child case no more than 1-2 times during his lifetime.
# Note 2: User Ranking is computed on user.save() and on feedback.save()
# if there is feedback.user and (feedback.status='spam' or is_valid != null)
class UserRanking(object):
    def __init__(self, curr_user):
        self.curr_user = curr_user
        self.curr_user_rank = curr_user.ranking

    def set_base_rank(self, crole=None):
        BR = 0.5  # (to be used when a feedback has an external source, e.g. through phone call)
        # source "Anonymous"
        # Role Base Ranking
        if crole == None:
            BR = 0.25
        elif crole == "simple_user":
            BR = 0.5
        elif crole == "volunteer":
            BR = 1.0
        print("BR:" + str(BR))
        return BR

    def get_profile_completeness(self):
        # For a 100% complete profile, weighted fields
        cuser = self.curr_user
        comple = 0.0
        if cuser.phone and len(cuser.phone) > 5:
            comple = comple + 0.4
        if cuser.date_of_birth:
            comple = comple + 0.1
        if cuser.address and len(cuser.address) > 2:
            comple = comple + 0.3
        if cuser.first_name and len(cuser.first_name) > 2:
            comple = comple + 0.05
        if cuser.last_name and len(cuser.last_name) > 2:
            comple = comple + 0.15
        print("comple:" + str(comple))
        return comple

    def get_sucessrate_facts(self, latest=10):
        # Recent success rate on archived facts
        cuser = self.curr_user
        su_rate = 0
        if latest == -1:
            arch_facts = Feedback.objects.filter(user=cuser).filter(is_valid__isnull=False)
        else:
            arch_facts = (
                Feedback.objects.filter(user=cuser).filter(is_valid__isnull=False).order_by("-created_at")[:latest]
            )
        if arch_facts.count() > 0:
            true_facts_num = 0
            true_facts = [f for f in arch_facts if f.is_valid]
            if true_facts:
                true_facts_num = len(true_facts)
            # true_facts = arch_facts.filter(is_valid=True)
            su_rate = true_facts_num / arch_facts.count()
            print("su_rate:" + str(su_rate))
        return su_rate

    def get_spamrate_facts(self, latest=10):
        # Recent spam rate on facts
        cuser = self.curr_user
        sp_rate = 0
        if latest > 0:
            recent_facts = Feedback.objects.filter(user=cuser).order_by("-created_at")[:latest]
        else:
            recent_facts = Feedback.objects.filter(user=cuser).order_by("-created_at")

        if recent_facts.count() > 0:
            spam_facts_num = 0
            spam_facts = [f for f in recent_facts if f.feedback_status == "spam"]
            if spam_facts:
                spam_facts_num = len(spam_facts)
            sp_rate = spam_facts_num / recent_facts.count()
            print("sp_rate:" + str(sp_rate))
        return sp_rate

    def get_new_user_rank(self, latest=10):
        # FINAL result (recompute from scratch)
        cuser = self.curr_user
        final_ranking = 0.0
        if cuser:
            try:
                BR = self.set_base_rank(cuser.role)
                comple = self.get_profile_completeness()
                su_rate = self.get_sucessrate_facts()
                sp_rate = self.get_spamrate_facts()
                final_ranking = BR + (BR * ((comple + su_rate) / 2 - sp_rate))  # in [0, 2*curr_ranking]
            except:
                raise
        return final_ranking


# Note: Fact Evaluation is computed when fact is saved for first time
class FactEvalEngine(object):
    def __init__(self, fact=None):
        self.fact = fact
        self.org_id = None
        self.caseid = None
        self.main_fact = None
        if fact:
            self.org_id = fact.organization_id
            self.caseid = fact.case_id
            self.main_fact = Feedback.objects.get(case=fact.case_id, is_main=True)

    def compute_max_dist_travelled(self, point1_date, point2_date):
        au = AnalyticsUtils()
        return au.getDistanceTravelled(point1_date, point2_date, "auto")

    def compute_dist_diff_km(self):
        au = AnalyticsUtils()
        inifact = self.main_fact
        curfact = self.fact
        max_d = au.getDistanceTravelled(then=inifact.date, speed="auto")
        point1 = (inifact.latitude, inifact.longitude)
        point2 = (curfact.latitude, curfact.longitude)
        fact_d = au.getDistance(point1, point2)
        ddiff = max_d - fact_d
        print("ddif: %f" % ddiff)
        return ddiff > 0

    def compute_time_diff_hh(self):
        au = AnalyticsUtils()
        inifact = self.main_fact
        curfact = self.fact
        hours = au.getDuration(inifact.date, curfact.date, "hours")
        print("hours diff: %d" % hours)
        return hours > 0

    def train_ML_model(self, org_id=None):
        # Get facts to create corpus with labels

        if not org_id:
            org_id = self.org_id
        prefix = "orgid_" + str(org_id)
        print(">>> Training model for organisation with id:%s" % prefix)
        modelname = prefix + "_facteval_model.pcl"
        vectorizername = prefix + "_facteval_vectorizer.pcl"
        facts = Feedback.objects.filter(organization=org_id).exclude(feedback_status="pending", comment__isnull=True)
        data_df = pd.DataFrame(list(facts.values("id", "comment", "score", "feedback_status")))
        data_df["label"] = (data_df["feedback_status"] == "spam").astype(int)
        data_df.drop(columns=["feedback_status"], inplace=True)

        # Create vectorizer
        maxdf = 0.9
        max_features = 200
        vectorizer = TfidfVectorizer(
            min_df=1,
            max_df=maxdf,
            sublinear_tf=True,
            use_idf=True,
            max_features=max_features,
            binary=False,
            strip_accents="unicode",
        )
        # print(vectorizer.fit_transform(data_df["comment"]))
        data_df["textVect"] = list(vectorizer.fit_transform(data_df["comment"]).toarray())

        # Perform training
        model = DecisionTreeClassifier()
        model.fit(data_df["textVect"].tolist(), data_df["label"].tolist())

        # Save vectorizer for future use
        vecpath = settings.ML_DIR + vectorizername
        os.makedirs(os.path.dirname(vecpath), exist_ok=True)
        with open(vecpath, "wb") as f1:
            pickle.dump(vectorizer, f1)

        # Save the trained model
        modelpath = settings.ML_DIR + modelname
        os.makedirs(os.path.dirname(modelpath), exist_ok=True)
        with open(modelpath, "wb") as f2:
            pickle.dump(model, f2)

    def score_fact(self, fact):
        org_id = self.org_id
        modelname = "orgid_" + str(org_id) + "_facteval_model.pcl"
        vectorizername = "orgid_" + str(org_id) + "_facteval_vectorizer.pcl"
        # Load vectorizer
        vecpath = settings.ML_DIR + vectorizername
        with open(vecpath, "rb") as f1:
            vectorizer = pickle.load(f1)

        # Load the trained model
        modelpath = settings.ML_DIR + modelname
        with open(modelpath, "rb") as f2:
            ml_model = pickle.load(f2)
        # filepath = '~/mlmodels/'+modelname

        # Compute prediction for given fact
        doc = fact.comment
        tfidf_vectorizer_vector = vectorizer.transform([doc])
        score = ml_model.predict_proba(tfidf_vectorizer_vector)  # two values ['not spam prob' 'spam prob']
        return score[0][1]  # return spam probability

    def evaluate(self, cfact=None):
        if not cfact:
            cfact = self.fact
        score = 0.0
        ev_user_rank = 0.75
        if cfact.user:
            ev_user_rank = cfact.user.ranking
        elif cfact.feedback_status and cfact.feedback_status == "credible":
            ev_user_rank = 1.0
        elif cfact.uuid_id:
            ev_user_rank = 0.25

        if not self.compute_time_diff_hh():
            # Step 1. Check time to mark as problematic
            score = -1.0
        elif not self.compute_dist_diff_km():
            # Step 2. Check distance to mark as problematic
            score = -2.0
        else:
            # Step 3. Check if spam
            spam_prediction = self.score_fact(cfact)
            reliable_level = 1 - spam_prediction
            if spam_prediction >= 0.5:
                score = -10.0
            else:
                # Step 4. Compute reliability
                print("reliable: %f" % reliable_level)
                score = reliable_level * ev_user_rank
                if score > 1.0:
                    score = 1.0

        return score


# def train_fact_spam_model(org_id=None):
#     from organizations.models import Organization
#     if org_id:
#         ff = FactEvalEngine()
#         ff.train_ML_model(org_id)
#     else:
#         orgs = Organization.objects.all()
#         for org in orgs:
#             ff = FactEvalEngine()
#             ff.train_ML_model(org.id)
