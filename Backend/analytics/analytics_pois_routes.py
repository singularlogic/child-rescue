from .analytics_utils import AnalyticsUtils
from feedbacks.models import Feedback
from cases.models import Case
from django.conf import settings


import pickle
import pandas as pd


class PlaceEvalEngine(object):
    def __init__(self, place=None):
        self.place = place
        self.caseid = None
        if place:
            self.caseid = place.case_id

    def compute_max_dist_travelled(self, point1_date, point2_date):
        au = AnalyticsUtils()
        return au.getDistanceTravelled(point1_date, point2_date, "auto")

    def compute_initial_proba():
        pass

    def markov_chain():
        pass
