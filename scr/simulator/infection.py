import math
from scr import config


def judge_infection_wells_riley(agent_list, classroom_volume, classroom_ach):
    """ Judge infection. """
    # Store susceptible agents and count infecting exposed agents.
    susceptible_number_list = []
    infecting_exposed_number = 0
    for temp_agent in agent_list:
        if temp_agent.get_status() == config.SUSCEPTIBLE:
            susceptible_number_list.append(temp_agent)
        elif temp_agent.get_status() == config.INFECTING_EXPOSED:
            infecting_exposed_number += 1

    # Calculate infection rate.
    infection_rate = infection_formula("wells_riley", infecting_exposed_number, classroom_volume, classroom_ach)

    # Jadge.
    for temp_susceptible in susceptible_number_list:
        prob = config.get_random()
        if prob < infection_rate:
            temp_susceptible.set_status(config.PRE_EXPOSED)

    return infection_rate


def infection_formula(name_model, infecting_exposed_number, classroom_volume, classroom_ach):
    """ Calculate infection rate by selected model. """
    # Future Work: Add infection models for calculate infection rate.

    if name_model == "wells_riley":
        # Use wells riley model.
        if config.MASK:
            effect_mask = 4.0
        else:
            effect_mask = 1.0
        infection_rate = 1.0 - math.exp(-infecting_exposed_number * config.QUANTUM_GENERATION_RATE * config.PULMONARY_VENTILATIION_RATE * (config.LESSON_TIME / 60) / (classroom_volume * classroom_ach * effect_mask))
    else:
        infection_rate = 0.0

    return infection_rate
