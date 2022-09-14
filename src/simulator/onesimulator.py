from src import config
from src.agent.agent import Agent as Agt
from src.simulator import infection
from src.log import logger


def onesimulation(simulation_num, list_id, list_calendar, dict_schedule):
    """ School Virus Infection Simulation. """
    # Prepare outputs.
    output_agent_log = [["daycount", "step"] + list_id[0]]
    output_agent_status_count = [["daycount", "step"] + config.STATUS_LIST]
    output_agent_antigen_log = [["daycount", "step"] + list_id[0]]
    output_agent_antigen_count = [["daycount", "step"] + config.ANTIGEN_STATUS_LIST]
    output_agent_offline_online_log = [["daycount", "step"] + list_id[0]]
    output_agent_offline_online_status_count = [["daycount", "step"] + config.OFFLINE_ONLINE_STATUS_LIST]
    output_infection_log = [["daycount", "step", "lesson_name", "classroom_name", "infection_rate_with_mask",
                             "infection_rate_without_mask"]]

    # Prepare agents.
    agent_list = []
    for agent_id_temp in list_id[0]:
        agent_list.append(Agt(agent_id_temp, config.SUSCEPTIBLE))

    # Set with/without a mask for each agent.
    # Future Work: To set the rate of agents with masks.
    for temp_agent in agent_list:
        temp_agent.set_mask(config.MASK)

    # Set an initial infected agent.
    # Future Work: To set an initial infected agent rate.
    agent_list[0].set_initial_infected()

    # Calculate each days.
    for one_calendar in list_calendar:
        agent_log, agent_count_log, \
        agent_antigen_log, agent_antigen_count_log, \
        agent_offline_online_log, agent_offline_online_count_log, infection_log = simulate_oneday(agent_list, list_id[1], one_calendar, dict_schedule)
        output_agent_log.extend(agent_log)
        output_agent_status_count.extend(agent_count_log)
        output_agent_antigen_log.extend(agent_antigen_log)
        output_agent_antigen_count.extend(agent_antigen_count_log)
        output_agent_offline_online_log.extend(agent_offline_online_log)
        output_agent_offline_online_status_count.extend(agent_offline_online_count_log)
        output_infection_log.extend(infection_log)

    # Output simulation logs.
    logger.save_logs(simulation_num, config.LOGGER_DIR, config.AGENT_STATUS_LOGGER_PATH, output_agent_log)
    logger.save_logs(simulation_num, config.LOGGER_DIR, config.AGENT_STATUS_LOGGER_COUNT_PATH,
                     output_agent_status_count)
    logger.save_logs(simulation_num, config.LOGGER_DIR, config.AGENT_ANTIGEN_LOGGER_PATH, output_agent_antigen_log)
    logger.save_logs(simulation_num, config.LOGGER_DIR, config.AGENT_ANTIGEN_LOGGER_COUNT_PATH,
                     output_agent_antigen_count)
    logger.save_logs(simulation_num, config.LOGGER_DIR, config.AGENT_OFFLINE_ONLINE_LOGGER_PATH, output_agent_offline_online_log)
    logger.save_logs(simulation_num, config.LOGGER_DIR, config.AGENT_OFFLINE_ONLINE_LOGGER_COUNT_PATH,
                     output_agent_offline_online_status_count)
    logger.save_logs(simulation_num, config.LOGGER_DIR, config.CLASSROOM_INFECTION_RATE_LOGGER_PATH,
                     output_infection_log)

def simulate_oneday(agent_list, lesson_list, one_calendar, dict_schedule):
    """ Simulate one day. """
    # Note: lesson_day, agent_schedule, classroom_schedule = one_calendar

    # Prepare return log.
    oneday_agent_log = []
    oneday_agent_count_log = []
    oneday_agent_antigen_log = []
    oneday_agent_antigen_count_log = []
    oneday_agent_offline_online_log = []
    oneday_agent_offline_online_count_log = []
    oneday_infection_log = []

    # Update a daycount.
    for temp_agent in agent_list:
        temp_agent.countday()

    # Simulate.
    if one_calendar[1] != "":
        # Antigen_test
        if one_calendar[3]:
            antigen_test(agent_list, dict_schedule[one_calendar[1]], dict_schedule[one_calendar[2]])
        # Class day.
        list_step = dict_schedule[one_calendar[1]].index.values
        for current_step in list_step:
            # Each step in the class day.
            infection_rate_dic = simulate_onestep(one_calendar[0], current_step, agent_list,
                                                  dict_schedule[one_calendar[1]], dict_schedule[one_calendar[2]])
            # Store logs.
            temp_agent_status, temp_agent_status_count, \
            temp_antigen_status, temp_antigen_status_count, \
            temp_offline_online_status, temp_offline_online_status_count\
                = logger.agent_logging(one_calendar[0], current_step, agent_list)
            oneday_agent_log.append(temp_agent_status)
            oneday_agent_count_log.append(temp_agent_status_count)
            oneday_agent_antigen_log.append(temp_antigen_status)
            oneday_agent_antigen_count_log.append(temp_antigen_status_count)
            oneday_agent_offline_online_log.append(temp_offline_online_status)
            oneday_agent_offline_online_count_log.append(temp_offline_online_status_count)
            oneday_infection_log.extend(
                logger.infection_rate_logging(one_calendar[0], current_step, lesson_list, infection_rate_dic))
    else:
        # Holiday.
        current_step = 0
        infection_rate_dic = {}
        # Store logs.
        temp_agent_status, temp_agent_status_count, \
        temp_antigen_status, temp_antigen_status_count, \
        temp_offline_online_status, temp_offline_online_status_count \
            = logger.agent_logging(one_calendar[0], current_step, agent_list)
        oneday_agent_log.append(temp_agent_status)
        oneday_agent_count_log.append(temp_agent_status_count)
        oneday_agent_antigen_log.append(temp_antigen_status)
        oneday_agent_antigen_count_log.append(temp_antigen_status_count)
        oneday_agent_offline_online_log.append(temp_offline_online_status)
        oneday_agent_offline_online_count_log.append(temp_offline_online_status_count)
        oneday_infection_log.extend(
            logger.infection_rate_logging(one_calendar[0], current_step, lesson_list, infection_rate_dic))

    return oneday_agent_log, oneday_agent_count_log, \
           oneday_agent_antigen_log, oneday_agent_antigen_count_log, \
           oneday_agent_offline_online_log, oneday_agent_offline_online_count_log, \
           oneday_infection_log


def simulate_onestep(lesson_day, current_step, agent_list, df_agent_schedule, df_classroom):
    """ Update the infection status at one step. """
    # Read and set the place of agents in current_step from schedule.
    list_current_lesson = []
    for temp_agent in agent_list:
        temp_lesson = df_agent_schedule.at[current_step, temp_agent.get_name()]
        if temp_lesson is None:
            temp_agent.set_lesson('')
            temp_agent.set_place('')
        else:
            temp_agent.set_lesson(temp_lesson)
            temp_agent.set_place(df_classroom.at[temp_lesson, 'classroom'])
            list_current_lesson.append(temp_lesson)
    list_current_lesson = sorted(list(set(list_current_lesson)))

    # Calcurate the infection rate for each classroom,
    # and update the infection status of agents.
    infection_rate_dic = {}
    for lesson, clsrm, vol, ach in zip(df_classroom.index, df_classroom["classroom"], df_classroom["volume"],
                                       df_classroom["ach"]):
        if lesson not in list_current_lesson:
            continue

        if "virtual" in clsrm:
            # Infection rate of virtual classroom is zero.
            infection_rate_w_mask = 0.0
            infection_rate_wo_mask = 0.0
        else:
            # Read the place of agents.
            temp_place_agent_list = [temp_agent for temp_agent in agent_list if temp_agent.get_place() == clsrm]
            # Calcurate infection and update agents' status.
            infection_rate_w_mask, infection_rate_wo_mask = infection.judge_infection_wells_riley(temp_place_agent_list,
                                                                                                  vol, ach)

        # # Store infection rate for summarize in other method.
        infection_rate_dic[lesson] = {}
        infection_rate_dic[lesson]["classroom"] = clsrm
        infection_rate_dic[lesson]["infection_rate_w_mask"] = infection_rate_w_mask
        infection_rate_dic[lesson]["infection_rate_wo_mask"] = infection_rate_wo_mask

    return infection_rate_dic


def antigen_test(agent_list, df_agent_schedule, df_classroom):
    # Pick up antigen test target agents
    antigen_test_target_agents = []
    for temp_agent in agent_list:
        if (temp_agent.get_status() != config.INFECTED) and (temp_agent.get_antigen_status() == config.NOT_TESTED):
            for current_step in range(len(df_agent_schedule)):
                temp_lesson = df_agent_schedule.at[current_step, temp_agent.get_name()]
                if temp_lesson is not None:
                    temp_classroom = df_classroom.at[temp_lesson, 'classroom']
                    if "virtual" in temp_classroom:
                        continue
                    else:
                        antigen_test_target_agents.append(temp_agent)
                        break

    #  Random pick up target agents
    if len(antigen_test_target_agents) > config.ANTIGENTEST_NUM:
        antigen_test_target_agents = config.get_random_sample(antigen_test_target_agents, config.ANTIGENTEST_NUM)

    # Antigen test
    for temp_agent in antigen_test_target_agents:
        if temp_agent.get_status() in [config.INFECTING_EXPOSED, config.INFECTED_ASYMPTOMATIC]:
            if config.get_random() < config.TRUE_POSITIVE_RATE:
                temp_agent.set_antigen_status(config.TRUE_POSITIVE)
        else:
            if config.get_random() < config.FALSE_POSITIVE_RATE:
                temp_agent.set_antigen_status(config.FALSE_POSITIVE)
