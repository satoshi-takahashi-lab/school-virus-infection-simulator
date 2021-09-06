from scr import config

class Agent:
    """ Student agent class. """
    # Parameters
    # Agent's name.
    __name = ''
    # Agent's status. Ex) S, P_E, E, I_E, I, R etc.
    __status = ''
    # Agent's place.
    __place = ''
    # Agent's lesson name.
    __lesson = ''
    # Exposed days of agent.
    __exposed_days = 0
    # ingecting exposed days of agent.
    __infecting_exposed_days = 0
    # infected days of agent.
    __infected_days = 0


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

    def set_place(self, temp_place):
        self.__place = temp_place

    def get_place(self):
        return self.__place

    def set_lesson(self, temp_lesson):
        self.__lesson = temp_lesson

    def get_lesson(self):
        return self.__lesson

    def countday(self):
        if self.get_status() == config.PRE_EXPOSED:
            # Pre exposed: Infected yesterday.
            self.set_status(config.EXPOSED)
            self.__exposed_days = 0
        elif self.get_status() == config.EXPOSED:
            # Exposed: Not yet infectious after infection.
            self.__exposed_days += 1
            if self.__exposed_days > config.EXPOSED_LIMIT_DAYS:
                self.set_status(config.INFECTING_EXPOSED)
                # self.__infecting_exposed_days = 0
        elif self.get_status() == config.INFECTING_EXPOSED:
            # Infecting exposed: Infectious condition.
            self.__infecting_exposed_days += 1
            if self.__infecting_exposed_days > config.INFECTING_EXPOSED_LIMIT_DAYS:
                self.set_status(config.INFECTED)
                # self.__infected_days = 0
        elif self.get_status() == config.INFECTED:
            # Infected: Not infectious but with symptoms.
            self.__infected_days += 1
            if self.__infected_days > config.INFECTED_LIMIT_DAYS:
                self.set_status(config.RECOVERED)

    def get_exposed_days(self):
        return self.__exposed_days
