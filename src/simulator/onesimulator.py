from src import config
from src.agent.agent import Agent as Agt
from src.simulator import infection
from src.log import logger


def onesimulation(simulation_num, list_id, list_calendar, dict_schedule):
    """ School Virus Infection Simulation. """
    # Prepare outputs.
    output_agent_log = [["daycount", "step"] + list_id[0]]
    output_agent_status_count = [["daycount", "step"] + config.STATUSLIST]
    output_infection_log = [["daycount", "step", "lesson_name", "classroom_name", "infection_rate_with_mask", "infection_rate_without_mask"]]

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
        agent_log, agent_count_log, infection_log = simulate_oneday(agent_list, list_id[1], one_calendar, dict_schedule)
        output_agent_log.extend(agent_log)
        output_agent_status_count.extend(agent_count_log)
        output_infection_log.extend(infection_log)

    # Output simulation logs.
    logger.save_logs(simulation_num, config.LOGGER_DIR, config.AGENT_STATUS_LOGGER_PATH, output_agent_log)
    logger.save_logs(simulation_num, config.LOGGER_DIR, config.AGENT_STATUS_LOGGER_COUNT_PATH, output_agent_status_count)
    logger.save_logs(simulation_num, config.LOGGER_DIR, config.CLASSROOM_INFECTION_RATE_LOGGER_PATH, output_infection_log)


def simulate_oneday(agent_list, lesson_list, one_calendar, dict_schedule):
    """ Simulate one day. """
    # Note: lesson_day, agent_schedule, classroom_schedule = one_calendar

    # Prepare return log.
    oneday_agent_log = []
    oneday_agent_count_log = []
    oneday_infection_log = []

    # Update a daycount.
    for temp_agent in agent_list:
        temp_agent.countday()

    # Simulate.
    if one_calendar[1] != "":
        # Class day.
        list_step = dict_schedule[one_calendar[1]].index.values
        for current_step in list_step:
            # Each step in the class day.
            infection_rate_dic = simulate_onestep(one_calendar[0], current_step, agent_list, dict_schedule[one_calendar[1]], dict_schedule[one_calendar[2]])
            # Store logs.
            temp_agent_status, temp_agent_status_count = logger.agent_logging(one_calendar[0], current_step, agent_list)
            oneday_agent_log.append(temp_agent_status)
            oneday_agent_count_log.append(temp_agent_status_count)
            oneday_infection_log.extend(logger.infection_rate_logging(one_calendar[0], current_step, lesson_list, infection_rate_dic))
    else:
        # Holiday.
        current_step = 0
        infection_rate_dic = {}
        # Store logs.
        temp_agent_status, temp_agent_status_count = logger.agent_logging(one_calendar[0], current_step, agent_list)
        oneday_agent_log.append(temp_agent_status)
        oneday_agent_count_log.append(temp_agent_status_count)
        oneday_infection_log.extend(logger.infection_rate_logging(one_calendar[0], current_step, lesson_list, infection_rate_dic))

    return oneday_agent_log, oneday_agent_count_log, oneday_infection_log


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
    for lesson, clsrm, vol, ach in zip(df_classroom.index, df_classroom["classroom"], df_classroom["volume"], df_classroom["ach"]):
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
            infection_rate_w_mask, infection_rate_wo_mask = infection.judge_infection_wells_riley(temp_place_agent_list, vol, ach)

        # # Store infection rate for summarize in other method.
        infection_rate_dic[lesson] = {}
        infection_rate_dic[lesson]["classroom"] = clsrm
        infection_rate_dic[lesson]["infection_rate_w_mask"] = infection_rate_w_mask
        infection_rate_dic[lesson]["infection_rate_wo_mask"] = infection_rate_wo_mask

    return infection_rate_dic
