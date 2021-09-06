import os
import random
import numpy as np
import pandas as pd
from scr import config


def generate():
    """ Generate input data. """
    # Set random seed. It is independent of global random generator.
    random.seed(config.GENERATE_SEED)

    # Generate classroom schedules.
    os.makedirs(os.path.join(*config.CLASSROOM_DIR), exist_ok=True)
    cols = ['lesson', 'classroom', 'volume', 'ach']
    for classroom_path in config.CLASSROOM_PATH_LIST.values():
        df_classroom = pd.DataFrame(index=[], columns=cols)
        for lesson_num_temp in range(config.LESSON_NUM):
            for classroom_temp in range(config.CLASSROOM_NUM):
                record = pd.Series(['lesson' + str(lesson_num_temp) + "-" + str(classroom_temp), 'classroom' + str(classroom_temp), config.CLASSROOM_VOLUME, config.CLASSROOM_ACH], index=df_classroom.columns)
                df_classroom = df_classroom.append(record, ignore_index=True)
        df_classroom.to_csv(os.path.join(*config.CLASSROOM_DIR, classroom_path), index=False)

    # Generate agents schedules.
    os.makedirs(os.path.join(*config.AGENT_SCHEDULE_DIR), exist_ok=True)
    agent_list = ["agent" + str(i).zfill(3) for i in range(config.AGENT_NUM)]
    for agent_schedule_path in config.AGENT_SCHEDULE_PATH_LIST.values():
        df_agent_schedule = pd.DataFrame(index=[], columns=agent_list)
        for lesson_num_temp in range(config.LESSON_NUM):
            lesson_size_list = [len(i) for i in list(np.array_split(agent_list, config.CLASSROOM_NUM))]
            lesson_list = []
            for classroom_temp in range(config.CLASSROOM_NUM):
                lesson_list.extend(['lesson' + str(lesson_num_temp) + "-" + str(classroom_temp)] * lesson_size_list[classroom_temp])
            random.shuffle(lesson_list)
            record = pd.Series(lesson_list, index=df_agent_schedule.columns)
            df_agent_schedule = df_agent_schedule.append(record, ignore_index=True)
        df_agent_schedule.index.name = "step"
        df_agent_schedule.to_csv(os.path.join(*config.AGENT_SCHEDULE_DIR, agent_schedule_path))

    # Generate calendar.
    day_of_the_week_list = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    with open(os.path.join(*config.OUTPUT_ROOT_DIR, *config.CALENDAR_PATH), "w", encoding="utf_8_sig") as open_file:
        open_file.writelines(",".join(["daycount", "agent_schedule", "classroom_schedule"]) + "\n")
        for one_day in range(config.LESSON_DAYS):
            temp_day = day_of_the_week_list[one_day % 7]
            if temp_day not in ["sun", "sat"]:
                open_file.writelines(",".join([str(one_day), config.AGENT_SCHEDULE_PATH_LIST[temp_day], config.CLASSROOM_PATH_LIST[temp_day]]) + "\n")
            else:
                open_file.writelines(",".join([str(one_day), '', '']) + "\n")
