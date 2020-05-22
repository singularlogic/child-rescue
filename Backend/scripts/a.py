# execute script using Django extensions
# python manage.py runscript a

from alerts.models import Alert
from users.models import User
from feedbacks.models import Feedback
from cases.models import Case
from cases.web_admin_api.serializers import CasesSerializer
import analytics.analytics_basic as ab
import analytics.analytics_case as ac
from datetime import datetime
import json


def run():
    print(">>> Starting testing of new scripts...")

    # # 01. SMART SEARCH example --> OnStringSearch

    orgid = 1
    # search = ab.IntelliSearch()
    # result = search.run_rawsql_namesearch("Mohamet Alistalhi", orgid, thres=12, limit=10)
    # print(result)

    # # 02. USER EVALUATION --> OnUserSave

    # user1 = User.objects.get(id=1)
    # r = ab.UserRanking(user1)
    # fr = r.get_new_user_rank()
    # user1.ranking = fr
    # user1.save()
    # print("rank = %f" % fr)

    # # 03. FACT EVALUATION --> OnFactSave

    # fact1 = Feedback.objects.get(id=3)
    # ff = ab.FactEvalEngine(fact1)
    # # ff.train_ML_model()
    # # res = ff.score_fact(fact1)
    # # print(res)
    # # h1= ff.compute_time_diff_hh(datetime(2019, 11, 5, 23, 8, 15),datetime.now())
    # # h2 = ff.compute_max_dist_travelled(datetime(2019, 12, 12, 8, 34, 15),datetime.now())
    # # print(h1, h2)

    # # ab.train_fact_spam_model()
    # res = ff.evaluate(fact1)
    # print("fact score: %f" % res)

    # # 04. PROFILING --> OnCaseSave
    case1 = Case.objects.select_related("child").get(id=3)  # step 1: Get current case with child's data
    ceng = ac.ProfileEvalEngine(case1)  # step 2: Initialize case engine

    # # 04.a Predict category types and/or proba of disappearance
    p_json1 = ceng.get_profiling_preds_json()  # compute_probability and return json
    print(p_json1)
    case1.data = p_json1 # put json in case's data field
    case1.save() #save case

    # 04.b Fetch similar cases of the same org

    similar_list = ceng.fetch_similar_closed_cases()  # return list of 2 similar cases ids
    # print(similar_list)
    # if similar_list:
    #     similar_cases = Case.objects.select_related("child").filter(id__in=similar_list)

    # 04.c Evaluate initial Places _part1
    print("Get Radius for main fact: {}km".format(str(ceng.suggest_radius_for_mainfact())))
    ceng.evaluate_non_fact_places() # writes to DB (places)
    ceng.evaluate_fact_places()  # writes to DB (places)
    # # for mcase in cases:
    # #     print(mcase.created_at, mcase.id)
    # print(cases.head())

    # 05. Route and POIs
    # 05.a Evaluate initial Places _part2 --> OnPlaceSave

    # 06. External APIs
    # 06.a Get information on Case creation only

    # case6 = Case.objects.select_related("child").get(id=1)  # step 1: Get current case with child's data
    # ceng = ac.ProfileEvalEngine(case6)
    # list_of_event_places = ceng.get_venues_from_socialnetworks_apis(radius=20)
    # for p in list_of_event_places:
    #     print(p)
    print(">>> End scripts.")
