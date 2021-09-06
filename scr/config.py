import os
import sys
import random
import datetime
import shutil
import configparser

# Simulation.
CALENDAR_PATH = ""
OUTPUT_ROOT_DIR = "output"
SIMULATION_COUNT = 10
RANDOM_SEED = None
# Agent.
MASK = False
# Classroom.
CLASSROOM_VOLUME = 150
CLASSROOM_ACH = 1.15
LESSON_TIME = 100
# Infection.
PULMONARY_VENTILATIION_RATE = 0.3
QUANTUM_GENERATION_RATE = 8
EXPOSED_LIMIT_DAYS = 3
INFECTING_EXPOSED_LIMIT_DAYS = 5
INFECTED_LIMIT_DAYS = 11
# Generate.
GENERATE = False
AGENT_NUM = 100
CLASSROOM_NUM = 1
LESSON_DAYS = 100
LESSON_NUM = 4
GENERATE_SEED = None

# Output directory paths.
LOGGER_DIR = ['log']
AGENT_STATUS_LOGGER_PATH = r'agent_status_logger.csv'
AGENT_STATUS_LOGGER_COUNT_PATH = r'agent_status_logger_count.csv'
CLASSROOM_INFECTION_RATE_LOGGER_PATH = r'classroom_infection_rate_logger.csv'
AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_DIR = ['graph']
AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_SIER_PATH = r'agent_status_logger_summary_count_sier.png'
AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_PE_PATH = r'agent_status_logger_summary_count_pe.png'
AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_I_BOXPLOT_PATH = r'agent_status_logger_summary_count_i_boxplot.png'

# For generating input data.
AGENT_SCHEDULE_DIR = ['input', 'agent_schedule']
AGENT_SCHEDULE_PATH_LIST = {
    'mon' : r'agent_schedule_mon.csv',
    'tue' : r'agent_schedule_tue.csv',
    'wed' : r'agent_schedule_wed.csv',
    'thu' : r'agent_schedule_thu.csv',
    'fri' : r'agent_schedule_fri.csv',
}
CLASSROOM_DIR = ['input', 'classroom_schedule']
CLASSROOM_PATH_LIST = {
    'mon' : r'classroom_mon.csv',
    'tue' : r'classroom_tue.csv',
    'wed' : r'classroom_wed.csv',
    'thu' : r'classroom_thu.csv',
    'fri' : r'classroom_fri.csv',
}

# Agent status.
SUSCEPTIBLE = 'S'
PRE_EXPOSED = 'P_E'
EXPOSED = 'E'
INFECTING_EXPOSED = 'I_E'
INFECTED = 'I'
RECOVERED = 'R'
STATUSLIST = [SUSCEPTIBLE, PRE_EXPOSED, EXPOSED, INFECTING_EXPOSED, INFECTED, RECOVERED]


def set_parameter(config_ini_path):
    """ Read a config file and set parameters. """
    global CALENDAR_PATH
    global OUTPUT_ROOT_DIR
    global SIMULATION_COUNT
    global RANDOM_SEED
    global MASK
    global CLASSROOM_VOLUME
    global CLASSROOM_ACH
    global LESSON_TIME
    global PULMONARY_VENTILATIION_RATE
    global QUANTUM_GENERATION_RATE
    global EXPOSED_LIMIT_DAYS
    global INFECTING_EXPOSED_LIMIT_DAYS
    global INFECTED_LIMIT_DAYS
    global GENERATE
    global AGENT_NUM
    global CLASSROOM_NUM
    global LESSON_DAYS
    global LESSON_NUM
    global GENERATE_SEED
    global AGENT_SCHEDULE_DIR
    global CLASSROOM_DIR
    global LOGGER_DIR
    global AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_DIR

    # Check error and read a config file.
    if not os.path.exists(os.path.join(*config_ini_path)):
        print(os.path.join(*config_ini_path) + " is not exists")
        sys.exit()
    config = configparser.ConfigParser()
    config.read(os.path.join(*config_ini_path), encoding="utf_8")

    # Set [simulation] parameters.
    # Caution: Debug config errors that occured when string is enclosed quotation mark.
    now = datetime.datetime.now()
    OUTPUT_ROOT_DIR = [config['SIMULATION']['output_root_dir']] + ['{0:%Y%m%d_%H%M%S}'.format(now)]
    os.makedirs(os.path.join(*OUTPUT_ROOT_DIR, 'input'), exist_ok=True)
    shutil.copy(os.path.join(*config_ini_path), os.path.join(*OUTPUT_ROOT_DIR, *config_ini_path))
    if config['SIMULATION']['calendar_path'] != "":
        GENERATE = False
        CALENDAR_PATH = ['input'] + [config['SIMULATION']['calendar_path']]
        shutil.copy(os.path.join(*CALENDAR_PATH), os.path.join(*OUTPUT_ROOT_DIR, *CALENDAR_PATH))
    else:
        GENERATE = True
        CALENDAR_PATH = ['input', 'generate_sim_calendar.csv']
    SIMULATION_COUNT = int(config['SIMULATION']['simulation_count'])
    if config['SIMULATION']['random_seed'] in ["", "None"]:
        RANDOM_SEED = None
    else:
        RANDOM_SEED = config['SIMULATION']['random_seed']

    # Set [Agent] parameters.
    if config['AGENT']['mask'] == "True":
        MASK = True
    elif config['AGENT']['mask'] == "False":
        MASK = False
    else:
        print("Mask parameter should be Boolean.")
        sys.exit()

    # Set [classroom] parameters.
    CLASSROOM_VOLUME = int(config['CLASSROOM']['classroom_volume'])
    CLASSROOM_ACH = float(config['CLASSROOM']['classroom_ach'])

    # Set [infection] parameters.
    PULMONARY_VENTILATIION_RATE = float(config['INFECTION']['pulmonary_ventilation_rate'])
    QUANTUM_GENERATION_RATE = int(config['INFECTION']['quantum_generation_rate'])
    EXPOSED_LIMIT_DAYS = int(config['INFECTION']['exposed_limit_days'])
    INFECTING_EXPOSED_LIMIT_DAYS = int(config['INFECTION']['infecting_exposed_limit_days'])
    INFECTED_LIMIT_DAYS = int(config['INFECTION']['infected_limit_days'])

    # set [generate] parameters.
    if GENERATE:
        AGENT_NUM = int(config['GENERATE']['agent_num'])
        CLASSROOM_NUM = int(config['GENERATE']['classroom_num'])
        LESSON_DAYS = int(config['GENERATE']['lesson_days'])
        LESSON_NUM = int(config['GENERATE']['lesson_num'])
        if config['GENERATE']['generate_seed'] in ["", "None"]:
            GENERATE_SEED = None
        else:
            GENERATE_SEED = config['GENERATE']['generate_seed']
    else:
        shutil.copytree(os.path.join(*AGENT_SCHEDULE_DIR), os.path.join(*OUTPUT_ROOT_DIR, *AGENT_SCHEDULE_DIR))
        shutil.copytree(os.path.join(*CLASSROOM_DIR), os.path.join(*OUTPUT_ROOT_DIR, *CLASSROOM_DIR))
    AGENT_SCHEDULE_DIR = OUTPUT_ROOT_DIR + AGENT_SCHEDULE_DIR
    CLASSROOM_DIR = OUTPUT_ROOT_DIR + CLASSROOM_DIR

    # Update folder.
    LOGGER_DIR = OUTPUT_ROOT_DIR + LOGGER_DIR
    AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_DIR = OUTPUT_ROOT_DIR + AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_DIR
    os.makedirs(os.path.join(*LOGGER_DIR), exist_ok=True)
    os.makedirs(os.path.join(*AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_DIR), exist_ok=True)


def set_random_seed():
    """ Set random seed to control random numbers for verification. """
    random.seed(RANDOM_SEED)


def get_random():
    """ Return random number [0.0, 1.0). """
    return random.random()
