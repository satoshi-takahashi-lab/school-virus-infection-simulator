import os
import csv
import pandas as pd
from scr import config



def read_calendar():
    """ Read calender file. """
    with open(os.path.join(*config.OUTPUT_ROOT_DIR, *config.CALENDAR_PATH), "r", encoding="utf_8_sig") as open_file:
        list_calendar = list(csv.reader(open_file))
        list_calendar = list_calendar[1:]   # Delete header.
    return list_calendar


def prepare_schedules(list_calendar):
    """ Prepare schedules. Output: dict_schedule, list_id. """
    dict_schedule = {}
    list_agent_scedule = list({one_cldr[1] for one_cldr in list_calendar if one_cldr[1] != ''})
    list_agent_id = []
    for one_schedule in list_agent_scedule:
        temp_df = pd.read_csv(os.path.join(*config.AGENT_SCHEDULE_DIR, one_schedule), index_col=0, encoding="utf_8_sig")
        list_agent_id.extend(temp_df.columns.values)
        temp_df = temp_df.where(temp_df.notnull(), None)
        dict_schedule[one_schedule] = temp_df
    list_agent_id = sorted(list(set(list_agent_id)))

    list_classroom_scedule = list({one_cldr[2] for one_cldr in list_calendar if one_cldr[2] != ''})
    list_lesson = []
    for one_schedule in list_classroom_scedule:
        temp_df = pd.read_csv(os.path.join(*config.CLASSROOM_DIR, one_schedule), index_col=0, encoding="utf_8_sig")
        list_lesson.extend(temp_df.index.values)
        temp_df = temp_df.where(temp_df.notnull(), None)
        dict_schedule[one_schedule] = temp_df
    list_lesson = sorted(list(set(list_lesson)))

    return dict_schedule, [list_agent_id, list_lesson]
