import os
import sys
import random
import datetime
import shutil
import configparser

# Simulation.
CALENDAR_PATH = ""
OUTPUT_ROOT_DIR = "output"
SIMULATION_COUNT = 100
LESSON_TIME = 45
RANDOM_SEED = None
# Agent.
MASK = False
# Infection.
PULMONARY_VENTILATIION_RATE = 0.54
QUANTUM_GENERATION_RATE = 48
EXHALATION_FILTRATION_EFFICIENCY = 0.5
RESPIRATION_FILTRATION_EFFICIENCY = 0.5
ASYMPTOMATIC_RATE = 0.3
EXPOSED_LIMIT_DAYS = 3
INFECTING_EXPOSED_LIMIT_DAYS = 2
INFECTED_LIMIT_DAYS = 14
INFECTED_ASYMPTOMATIC_LIMIT_DAYS = 8
# Generate.
GENERATE = False
AGENT_NUM = 480
CLASSROOM_NUM = 20
CLASSROOM_VOLUME = 180
CLASSROOM_ACH = 3
LESSON_DAYS = 84
LESSON_NUM = 7
GENERATE_SEED = None

# Output directory paths.
LOGGER_DIR = ['log']
AGENT_STATUS_LOGGER_PATH = r'agent_status_logger.csv'
AGENT_STATUS_LOGGER_COUNT_PATH = r'agent_status_logger_count.csv'
CLASSROOM_INFECTION_RATE_LOGGER_PATH = r'classroom_infection_rate_logger.csv'
SUMMARY_DIR = ['summary']
PATH_AGENT_STATUS_SUMMARY_DAYS = r'summary_agent_status_count_eachDay.csv'
PATH_AGENT_STATUS_SUMMARY_SIMULATIONS = r'summary_agent_status_count_eachSim.csv'
PATH_AGENT_STATUS_SUMMARY_DAYS_WITH_CUMSUM = r'summary_agent_status_count-cumsum_eachDay.csv'
PATH_AGENT_STATUS_SUMMARY_SIMULATIONS_WITH_CUMSUM = r'summary_agent_status_count-cumsum_eachSim.csv'
PATH_CLASSROOM_INFECTION_RATE_SUMMALY = r'summary_classroom_infection_rate_allSim.csv'
SUMMARY_GRAPH_DIR = ['graph']
PATH_AGENT_STATUS_SUMMARY_COUNT_TIMESERIES_GRAPH = r'summary_agent_status_count_{}_timeseries.png'
PATH_AGENT_STATUS_SUMMARY_COUNT_BOXPLOT_GRAPH = r'summary_agent_status_count_{}-{}-{}_boxplot.png'

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
INFECTED_ASYMPTOMATIC = 'I_A'
RECOVERED = 'R'
STATUSLIST = [SUSCEPTIBLE, PRE_EXPOSED, EXPOSED, INFECTING_EXPOSED, INFECTED, INFECTED_ASYMPTOMATIC, RECOVERED]


def set_parameter(config_ini_path):
    """ Read a config file and set parameters. """
    global CALENDAR_PATH
    global OUTPUT_ROOT_DIR
    global SIMULATION_COUNT
    global LESSON_TIME
    global RANDOM_SEED
    global MASK
    global PULMONARY_VENTILATIION_RATE
    global QUANTUM_GENERATION_RATE
    global ASYMPTOMATIC_RATE
    global EXHALATION_FILTRATION_EFFICIENCY
    global RESPIRATION_FILTRATION_EFFICIENCY
    global EXPOSED_LIMIT_DAYS
    global INFECTING_EXPOSED_LIMIT_DAYS
    global INFECTED_LIMIT_DAYS
    global INFECTED_ASYMPTOMATIC_LIMIT_DAYS
    global GENERATE
    global AGENT_NUM
    global CLASSROOM_NUM
    global CLASSROOM_VOLUME
    global CLASSROOM_ACH
    global LESSON_DAYS
    global LESSON_NUM
    global GENERATE_SEED
    global AGENT_SCHEDULE_DIR
    global CLASSROOM_DIR
    global LOGGER_DIR
    global SUMMARY_DIR
    global SUMMARY_GRAPH_DIR

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
    LESSON_TIME = int(config['SIMULATION']['lesson_time'])
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

    # Set [infection] parameters.
    PULMONARY_VENTILATIION_RATE = float(config['INFECTION']['pulmonary_ventilation_rate'])
    QUANTUM_GENERATION_RATE = int(config['INFECTION']['quantum_generation_rate'])
    EXHALATION_FILTRATION_EFFICIENCY = float(config['INFECTION']['exhalation_filtration_efficiency'])
    RESPIRATION_FILTRATION_EFFICIENCY = float(config['INFECTION']['respiration_filtration_efficiency'])
    ASYMPTOMATIC_RATE = float(config['INFECTION']['asymptomatic_rate'])
    EXPOSED_LIMIT_DAYS = int(config['INFECTION']['exposed_limit_days'])
    INFECTING_EXPOSED_LIMIT_DAYS = int(config['INFECTION']['infecting_exposed_limit_days'])
    INFECTED_LIMIT_DAYS = int(config['INFECTION']['infected_limit_days'])
    INFECTED_ASYMPTOMATIC_LIMIT_DAYS = int(config['INFECTION']['infected_asymptomatic_limit_days'])

    # set [generate] parameters.
    if GENERATE:
        AGENT_NUM = int(config['GENERATE']['agent_num'])
        CLASSROOM_NUM = int(config['GENERATE']['classroom_num'])
        CLASSROOM_VOLUME = int(config['GENERATE']['classroom_volume'])
        CLASSROOM_ACH = float(config['GENERATE']['classroom_ach'])
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
    SUMMARY_DIR = OUTPUT_ROOT_DIR + SUMMARY_DIR
    SUMMARY_GRAPH_DIR = OUTPUT_ROOT_DIR + SUMMARY_GRAPH_DIR
    os.makedirs(os.path.join(*LOGGER_DIR), exist_ok=True)
    os.makedirs(os.path.join(*SUMMARY_DIR), exist_ok=True)
    os.makedirs(os.path.join(*SUMMARY_GRAPH_DIR), exist_ok=True)


def set_random_seed():
    """ Set random seed to control random numbers for verification. """
    random.seed(RANDOM_SEED)


def get_random():
    """ Return random number [0.0, 1.0). """
    return random.random()
