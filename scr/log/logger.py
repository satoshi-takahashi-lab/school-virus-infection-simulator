import os
from scr import config


def agent_logging(lesson_day, current_step, agent_list):
    """ Generate a current list containing the agent status. """
    temp_status = [temp_agent.get_status() for temp_agent in agent_list]

    list_status = [str(lesson_day), str(current_step)]
    list_status += temp_status
    list_status_count = [str(lesson_day), str(current_step)]
    # Use count() because of len(config.STATUSLIST) is small.
    list_status_count += [str(temp_status.count(one_status)) for one_status in config.STATUSLIST]
    return list_status, list_status_count


def infection_rate_logging(lesson_day, current_step, lesson_list, infection_rate_dic):
    """ Generate a current list containing the lesson classroom and infection rate. """
    temp_list_classroom = []
    temp_list_rate = []
    for one_lesson in lesson_list:
        if one_lesson in infection_rate_dic.keys():
            temp_list_classroom.append(str(infection_rate_dic[one_lesson]['classroom']))
            temp_list_rate.append(str(infection_rate_dic[one_lesson]['infection_rate']))
        else:
            temp_list_classroom.append("-")
            temp_list_rate.append("-")
    output_list = [str(lesson_day), str(current_step)] + temp_list_classroom + temp_list_rate
    return output_list


def save_logs(simulation_num, output_path, file_name, list_log):
    """ Save logs. """
    temp_filename = os.path.join(*output_path, 'sim{:03d}_'.format(simulation_num) + file_name)
    with open(temp_filename, "w", encoding="utf_8_sig") as open_file:
        for one_row in list_log:
            open_file.writelines(",".join(one_row) + "\n")
