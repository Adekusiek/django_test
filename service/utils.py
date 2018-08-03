from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from .models import Customer, Lesson, Curriculum
import numpy as np

# returns the array of [["2018/3", 0], ["2018/2", -1],["2018/1", -2],["2017/12", -3]...]
def get_month_array(num_of_months=3):

    # prepare an array to show year-month choice
    month_infos = []
    today = date.today()
    for m in np.arange(0, -(num_of_months+1), -1):
        shifted_date = today + relativedelta(months=m)
        year_month_str = "%d年%d月" % (shifted_date.year, shifted_date.month)
        month_infos.append([year_month_str, m])

    return month_infos

# Returns the first date and the last date of the month concerned
# prev_month=0 means this month
# prev_month=-1 means last month
def get_start_end_month(prev_month=0):

    today = date.today()
    first_day_of_month = today + relativedelta(months=prev_month) - timedelta(days=today.day-1)
    end_day_of_month   = today + relativedelta(months=prev_month+1) - timedelta(days=today.day)

    return first_day_of_month, end_day_of_month


def report_calculator(age_band_flg=False, prev_month=0):

    first_day_of_month, end_day_of_month = get_start_end_month(prev_month=prev_month)

    lessons = Lesson.objects.filter(date__gte=first_day_of_month, date__lte=end_day_of_month).select_related()

    sex_choices = dict(((1,'男性'),(2,'女性'),))

    curriculums = Curriculum.objects.all()
    curriculum_choices = dict([(c.id, c.name) for c in curriculums ])

    data_array = []

    # 性別　x　ジャンル　x 年代 レポート機能
    if age_band_flg:
        for s_k, s_v in sex_choices.items():
            for c_k, c_v in curriculum_choices.items():
                lesson_list = [l for l in list(lessons) if l.customer.sex == s_k and l.curriculum_id == c_k]
                age_list = [l.customer.age for l in lesson_list]
                bins = np.arange(10, 100, 10)
                age_bands = np.digitize(age_list, bins)

                for i in np.arange(1, 8):
                    lesson_at_age_band = []
                    for lesson, age_band in zip(lesson_list, age_bands):
                        if age_band == i:
                            lesson_at_age_band.append(lesson)

                    lesson_count = len(lesson_at_age_band)                                   # レッスン数
                    customer_count = len(set([l.customer for l in lesson_at_age_band ]))     # 受講者数
                    total_charge = sum([l.charge for l in lesson_at_age_band ])              # 売り上げ
                    data_array.append([s_v, c_v, bins[i-1], lesson_count, customer_count, total_charge])

    # 性別　x　ジャンル　レポート機能
    else:
        for s_k, s_v in sex_choices.items():
            for c_k, c_v in curriculum_choices.items():
                lesson_list = [l for l in list(lessons) if l.customer.sex == s_k and l.curriculum_id == c_k]
                lesson_count = len(lesson_list)                                   # レッスン数
                customer_count = len(set([l.customer for l in lesson_list ]))     # 受講者数
                total_charge = sum([l.charge for l in lesson_list ])              # 売り上げ
                data_array.append([s_v, c_v, lesson_count, customer_count, total_charge])

    return data_array
