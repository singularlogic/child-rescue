# execute script using Django extensions
# python manage.py runscript a

from alerts.models import Alert
from users.models import User
from feedbacks.models import Feedback
from cases.models import Case
import analytics.analytics_basic as ab
import analytics.analytics_case as ac
from datetime import datetime
import pandas as pd


def run():
    print(">>> Starting testing of new scripts...")
    # 01. SMART SEARCH example
    orgid = 1
    search = ab.IntelliSearch()
    result = search.run_rawsql_namesearch("Mohamet Alistalhi", orgid, thres=12, limit=10)
    print(result)

    # 02. USER EVALUATION
    user1 = User.objects.get(id=1)
    r = ab.UserRanking(user1)
    fr = r.get_new_user_rank()
    user1.ranking = fr
    user1.save()
    print("rank = %f" % fr)

    # 03. FACT EVALUATION
    fact1 = Feedback.objects.get(id=3)
    ff = ab.FactEvalEngine(fact1)
    # ff.train_ML_model()
    # res = ff.score_fact(fact1)
    # print(res)
    # h1= ff.compute_time_diff_hh(datetime(2019, 11, 5, 23, 8, 15),datetime.now())
    # h2 = ff.compute_max_dist_travelled(datetime(2019, 12, 12, 8, 34, 15),datetime.now())
    # print(h1, h2)

    # ab.train_fact_spam_model()
    res = ff.evaluate(fact1)
    print("fact score: %f" % res)

    # 04. Fetch similar cases
    case1 = Case.objects.get(id=3)
    ceng = ac.CaseEvalEngine(case1)
    cases = ceng.fetch_similar_closed_cases()
    # for mcase in cases:
    #     print(mcase.created_at, mcase.id)
    print(cases.head())

    print(">>> End scripts.")
