#
# Copyright (c) [2021] [Satoshi Takahashi, Masaki Kitazawa, Atsushi Yoshikawa]
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

from src import config, utils
from src.generator import input_generator
from src.simulator import onesimulator
from src.chart import summary_generator, chart_generator
import sys


def main(input_dir):
    """ Main process. """
    # Read and set config.
    config.set_parameter(input_dir)

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
    summary_generator.generate_summary()
    chart_generator.chart_generate(list_id)


if __name__ == '__main__':
    args = sys.argv
    main(args[1])
