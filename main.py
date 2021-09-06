#
# Copyright (c) [2021] [Satoshi Takahashi, Masaki Kitazawa, Atsushi Yoshikawa]
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

from scr import config, utils
from scr.generator import input_generator
from scr.simulator import onesimulator
from scr.chart import chart_generater


def main():
    """ Main process. """
    # Define variables.
    path_config = ["input", "config.ini"]

    # Read and set config.
    config.set_parameter(path_config)

    # Generate input data.
    if config.GENERATE:
        input_generator.generate()

    # Read a calendar.
    list_calendar = utils.read_calendar()

    # Prepare schedules.
    dict_schedule, list_id = utils.prepare_schedules(list_calendar)

    # Simulate.
    config.set_random_seed()
    for simulation_num in range(0, config.SIMULATION_COUNT):
        print("simulation_num: " + str(simulation_num))
        onesimulator.onesimulation(simulation_num, list_id, list_calendar, dict_schedule)

    # Generate output chart.
    chart_generater.chart_generate()


if __name__ == '__main__':
    main()
