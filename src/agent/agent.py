from src import config

class Agent:
    """ Student agent class. """
    # Parameters
    # Agent's name.
    __name = ''
    # Agent's status. Ex) S, P_E, E, I_E, I, I_A, R etc.
    __status = ''
    # Agent's mask flag.
    __mask = False
    # Agent's place.
    __place = ''
    # Agent's lesson name.
    __lesson = ''
    # Exposed days of agent.
    __exposed_days = 0
    # Infecting exposed days of agent.
    __infecting_exposed_days = 0
    # Infected days of agent.
    __infected_days = 0
    # Infected asymptomatic days of agent.
    __infected_asymptomatic_days = 0
    # Antigen test status. EX) TP, FP, NT
    __antigen_status = config.NOT_TESTED
    # Antigen test positive days of agent.
    __antigen_positive_days = 0

    def __init__(self, temp_name, temp_status):
        self.set_name(temp_name)
        self.set_status(temp_status)

    def set_name(self, temp_name):
        self.__name = temp_name

    def get_name(self):
        return self.__name

    def set_status(self, temp_status):
        self.__status = temp_status

    def get_status(self):
        return self.__status

    def set_mask(self, flag_mask):
        self.__mask = flag_mask

    def get_mask(self):
        return self.__mask

    def set_place(self, temp_place):
        self.__place = temp_place

    def get_place(self):
        return self.__place

    def set_lesson(self, temp_lesson):
        self.__lesson = temp_lesson

    def get_lesson(self):
        return self.__lesson

    def set_antigen_status(self, antigen_status):
        self.__antigen_status = antigen_status

    def get_antigen_status(self):
        return self.__antigen_status

    def get_offline_online_status(self):
        temp_offline_online_status = config.OFFLINE
        if self.__place == "":
            temp_offline_online_status = config.NO_LESSON
        elif self.__status == config.INFECTED:
            temp_offline_online_status = config.NO_LESSON
        elif "virtual" in self.__place:
            temp_offline_online_status = config.ONLINE
        elif self.__antigen_status in [config.TRUE_POSITIVE, config.FALSE_POSITIVE]:
            temp_offline_online_status = config.ONLINE

        return temp_offline_online_status

    def set_initial_infected(self):
        self.__status = config.INFECTING_EXPOSED
        self.__infecting_exposed_days = -1

    def countday(self):
        if self.get_status() == config.PRE_EXPOSED:
            # Pre exposed: Infected yesterday.
            self.set_status(config.EXPOSED)
            self.__exposed_days = 0
        elif self.get_status() == config.EXPOSED:
            # Exposed: Not yet infectious after infection.
            self.__exposed_days += 1
            if self.__exposed_days >= config.EXPOSED_LIMIT_DAYS:
                self.set_status(config.INFECTING_EXPOSED)
                # self.__infecting_exposed_days = 0
        elif self.get_status() == config.INFECTING_EXPOSED:
            # Infecting exposed: Infectious condition.
            self.__infecting_exposed_days += 1
            if self.__infecting_exposed_days >= config.INFECTING_EXPOSED_LIMIT_DAYS:
                # To match the v1.0 result, remain a condition that does not use random number.
                if config.ASYMPTOMATIC_RATE == 0.0:
                    self.set_status(config.INFECTED)
                    # self.__infected_days = 0
                else:
                    temp_value = temp_value = config.get_random()
                    if temp_value < config.ASYMPTOMATIC_RATE:
                        self.set_status(config.INFECTED_ASYMPTOMATIC)
                        # self.__infected_asymptomatic_days = 0
                    else:
                        self.set_status(config.INFECTED)
                        # self.__infected_days = 0
        elif self.get_status() == config.INFECTED:
            # Infected: Not infectious but with symptoms.
            self.__infected_days += 1
            if self.__infected_days >= config.INFECTED_LIMIT_DAYS:
                self.set_status(config.RECOVERED)
        elif self.get_status() == config.INFECTED_ASYMPTOMATIC:
            # Infected asymptomatic : Infectious condition but without symptoms.
            self.__infected_asymptomatic_days += 1
            if self.__infected_asymptomatic_days >= config.INFECTED_ASYMPTOMATIC_LIMIT_DAYS:
                self.set_status(config.RECOVERED)

        if self.__antigen_status in [config.TRUE_POSITIVE, config.FALSE_POSITIVE]:
            self.__antigen_positive_days += 1
            if self.__antigen_positive_days >= config.ANTIGEN_POSITIVE_LIMIT_DAYS:
                self.set_antigen_status(config.NOT_TESTED)
                self.__antigen_positive_days = 0

    def get_exposed_days(self):
        return self.__exposed_days
