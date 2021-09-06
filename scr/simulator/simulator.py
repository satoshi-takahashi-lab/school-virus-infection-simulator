from scr.simulator import infection


def count_day(agent_list):
    """ Update a daycount. """
    for temp_agent in agent_list:
        temp_agent.countday()


def simulate(lesson_day, current_step, agent_list, df_agent_schedule, df_classroom):
    """ Update the infection status. """
    # Read and set the place of agents in current_step.
    list_current_lesson = []
    for temp_agent in agent_list:
        temp_lesson = df_agent_schedule.at[current_step, temp_agent.get_name()]
        if temp_lesson is not None:
            temp_agent.set_lesson(temp_lesson)
            temp_agent.set_place(df_classroom.at[temp_lesson, 'classroom'])
            list_current_lesson.append(temp_lesson)
    list_current_lesson = sorted(list(set(list_current_lesson)))

    # Future Work: Add absence process for infected agents.

    # Calcurate the infection rate for each classroom,
    # and update the infection status of agents.
    infection_rate_dic = {}
    for lesson, clsrm, vol, ach in zip(df_classroom.index, df_classroom["classroom"], df_classroom["volume"], df_classroom["ach"]):
        if lesson not in list_current_lesson:
            continue

        # Read the place of agents.
        temp_place_agent_list = [temp_agent for temp_agent in agent_list if temp_agent.get_place() == clsrm]

        # Calcurate and update.
        infection_rate = infection.judge_infection_wells_riley(temp_place_agent_list, vol, ach)

        # # Store infection rate for summarize in other method.
        infection_rate_dic[lesson] = {}
        infection_rate_dic[lesson]["classroom"] = clsrm
        infection_rate_dic[lesson]["infection_rate"] = infection_rate

    return infection_rate_dic
