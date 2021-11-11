import math
from src import config


def judge_infection_wells_riley(agent_list, classroom_volume, classroom_ach):
    """ Judge infection. """
    # Store susceptible agents and count infectious agents.
    susceptible_number_list = []
    infectious_number = 0
    for temp_agent in agent_list:
        if temp_agent.get_status() == config.SUSCEPTIBLE:
            susceptible_number_list.append(temp_agent)
        elif temp_agent.get_status() == config.INFECTING_EXPOSED:
            infectious_number += 1
        elif temp_agent.get_status() == config.INFECTED_ASYMPTOMATIC:
            infectious_number += 1

    # Calculate infection rate.
    infection_rate_w_mask, infection_rate_wo_mask = infection_formula("wells_riley", infectious_number, classroom_volume, classroom_ach)

    # Jadge.
    for temp_susceptible in susceptible_number_list:
        prob = config.get_random()
        if temp_susceptible.get_mask():
            # When the agent is wearing a mask.
            if prob < infection_rate_w_mask:
                temp_susceptible.set_status(config.PRE_EXPOSED)
        else:
            # When the agent is not wearing the mask.
            if prob < infection_rate_wo_mask:
                temp_susceptible.set_status(config.PRE_EXPOSED)         

    return infection_rate_w_mask, infection_rate_wo_mask


def infection_formula(name_model, infectious_number, classroom_volume, classroom_ach):
    """ Calculate infection rate of with/without a mask by selected model. """

    if name_model == "wells_riley":
        # Use wells riley model.
        effect_mask = 1.0 / ((1.0 - config.EXHALATION_FILTRATION_EFFICIENCY) * (1.0 - config.RESPIRATION_FILTRATION_EFFICIENCY))
        infection_rate_w_mask = 1.0 - math.exp(-infectious_number * config.QUANTUM_GENERATION_RATE * config.PULMONARY_VENTILATIION_RATE * (config.LESSON_TIME / 60) / (classroom_volume * classroom_ach * effect_mask))
        infection_rate_wo_mask = 1.0 - math.exp(-infectious_number * config.QUANTUM_GENERATION_RATE * config.PULMONARY_VENTILATIION_RATE * (config.LESSON_TIME / 60) / (classroom_volume * classroom_ach))
    else:
        # Future Work: Add infection models for calculate infection rate.
        infection_rate_w_mask = 0.0
        infection_rate_wo_mask = 0.0

    return infection_rate_w_mask, infection_rate_wo_mask
