from scr import config
from scr.agent.agent import Agent as Agt
from scr.simulator import simulator
from scr.log import logger


def onesimulation(simulation_num, list_id, list_calendar, dict_schedule):
    """ School Virus Infection Simulation. """
    # Prepare outputs.
    output_agent_log = [["daycount", "step"] + list_id[0]]
    output_agent_status_count = [["daycount", "step"] + config.STATUSLIST]
    temp_list = ["daycount", "step"] + ["{}_classroom".format(temp) for temp in list_id[1]]
    temp_list += ["{}_infection_rate".format(temp) for temp in list_id[1]]
    output_infection_log = [temp_list]

    # Prepare agents.
    agent_list = []
    for agent_id_temp in list_id[0]:
        agent_list.append(Agt(agent_id_temp, config.SUSCEPTIBLE))

    # Set an initial infected agent.
    # Future Work: To set an initial infected agent rate.
    agent_list[0].set_status(config.INFECTING_EXPOSED)

    # Calculate each days.
    for one_calender in list_calendar:
        agent_log, agent_count_log, infection_log = onedaysimulation(agent_list, list_id[1], one_calender, dict_schedule)
        output_agent_log.extend(agent_log)
        output_agent_status_count.extend(agent_count_log)
        output_infection_log.extend(infection_log)

    # Output simulation logs.
    logger.save_logs(simulation_num, config.LOGGER_DIR, config.AGENT_STATUS_LOGGER_PATH, output_agent_log)
    logger.save_logs(simulation_num, config.LOGGER_DIR, config.AGENT_STATUS_LOGGER_COUNT_PATH, output_agent_status_count)
    logger.save_logs(simulation_num, config.LOGGER_DIR, config.CLASSROOM_INFECTION_RATE_LOGGER_PATH, output_infection_log)


def onedaysimulation(agent_list, lesson_list, one_calender, dict_schedule):
    """ Simulate one day. """
    # Memo: lesson_day, agent_schedule, classroom_schedule = one_calender

    # Prepare return log.
    oneday_agent_log = []
    oneday_infection_log = []
    oneday_agent_count_log = []

    # Update daycount.
    simulator.count_day(agent_list)

    # Simulate.
    if one_calender[1] != "":
        # Class day.
        list_step = dict_schedule[one_calender[1]].index.values
        for current_step in list_step:
            infection_rate_dic = simulator.simulate(one_calender[0], current_step, agent_list, dict_schedule[one_calender[1]], dict_schedule[one_calender[2]])
            # Store logs.
            temp_agent_status, temp_agent_status_count = logger.agent_logging(one_calender[0], current_step, agent_list)
            oneday_agent_log.append(temp_agent_status)
            oneday_agent_count_log.append(temp_agent_status_count)
            oneday_infection_log.append(logger.infection_rate_logging(one_calender[0], current_step, lesson_list, infection_rate_dic))
    else:
        # Holiday.
        current_step = 1
        infection_rate_dic = {}
        # Store logs.
        temp_agent_status, temp_agent_status_count = logger.agent_logging(one_calender[0], current_step, agent_list)
        oneday_agent_log.append(temp_agent_status)
        oneday_agent_count_log.append(temp_agent_status_count)
        oneday_infection_log.append(logger.infection_rate_logging(one_calender[0], current_step, lesson_list, infection_rate_dic))

    return oneday_agent_log, oneday_agent_count_log, oneday_infection_log
