import os
from src import config


def agent_logging(lesson_day, current_step, agent_list):
    """ Generate a current list containing the agent status. """
    """ Generate status list """
    temp_status = [temp_agent.get_status() for temp_agent in agent_list]

    list_status = [str(lesson_day), str(current_step)]
    list_status += temp_status
    list_status_count = [str(lesson_day), str(current_step)]

    # Use count() because of len(config.STATUSLIST) is small.
    list_status_count += [str(temp_status.count(one_status)) for one_status in config.STATUS_LIST]

    """ Generate antigen status list """
    temp_antigen_status = [temp_agent.get_antigen_status() for temp_agent in agent_list]
    list_antigen_status = [str(lesson_day), str(current_step)]
    list_antigen_status += temp_antigen_status
    list_antigen_status_count = [str(lesson_day), str(current_step)]
    list_antigen_status_count += \
        [str(temp_antigen_status.count(one_antigen_status)) for one_antigen_status in config.ANTIGEN_STATUS_LIST]

    """ Generate offline online status list """
    temp_offline_online_status = [temp_agent.get_offline_online_status() for temp_agent in agent_list]
    list_offline_online_status = [str(lesson_day), str(current_step)]
    list_offline_online_status += temp_offline_online_status
    list_offline_online_status_count = [str(lesson_day), str(current_step)]
    list_offline_online_status_count += \
        [str(temp_offline_online_status.count(one_offline_online_status)) for one_offline_online_status in
         config.OFFLINE_ONLINE_STATUS_LIST]

    return list_status, list_status_count, \
           list_antigen_status, list_antigen_status_count, \
           list_offline_online_status, list_offline_online_status_count


def infection_rate_logging(lesson_day, current_step, lesson_list, infection_rate_dic):
    """ Generate a current list containing the lesson classroom and infection rate. """
    output_list = []
    for one_lesson in lesson_list:
        if one_lesson in infection_rate_dic.keys():
            temp_list = [str(lesson_day), \
                         str(current_step), \
                         str(one_lesson), \
                         str(infection_rate_dic[one_lesson]['classroom']), \
                         str(infection_rate_dic[one_lesson]['infection_rate_w_mask']), \
                         str(infection_rate_dic[one_lesson]['infection_rate_wo_mask']) \
                         ]
            output_list.append(temp_list)

    if output_list == []:
        # Store empty data on days when there ara no lessons.
        output_list.append([str(lesson_day), str(current_step), "-", "-", "-", "-"])

    return output_list


def save_logs(simulation_num, output_path, file_name, list_log):
    """ Save logs. """
    temp_filename = os.path.join(*output_path, 'sim{:04d}_'.format(simulation_num) + file_name)
    with open(temp_filename, "w", encoding="utf_8_sig") as open_file:
        for one_row in list_log:
            open_file.writelines(",".join(one_row) + "\n")
