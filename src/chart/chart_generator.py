import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src import config

# Set graph parameters.
plt.rcParams['font.family'] = 'Times New Roman'     # Set font family.
plt.rcParams['mathtext.fontset'] = 'stix'           # Set math text font.
plt.rcParams["font.size"] = 24                      # Set font size.
plt.rcParams['xtick.labelsize'] = 24                # Set x label size.
plt.rcParams['ytick.labelsize'] = 24                # Set y label size.
plt.rcParams['xtick.direction'] = 'in'              # Set x axis direction.
plt.rcParams['ytick.direction'] = 'in'              # Set y axis direction.
plt.rcParams['axes.linewidth'] = 1.0                # Set axis line width.
plt.rcParams["legend.fancybox"] = False             # Set legend box corner.
plt.rcParams["legend.framealpha"] = 1               # Set legend box alpha (transparency).
plt.rcParams["legend.edgecolor"] = 'black'          # Set legend box edge color.
plt.rcParams["legend.handlelength"] = 0.5           # Set legend line length.
plt.rcParams["legend.handletextpad"] = 0.3          # Set legend distance between line to string.
plt.rcParams["legend.markerscale"] = 2              # Set legend marker scale.
plt.rcParams["legend.borderaxespad"] = 0.           # Set distance between legend box and graph.


def chart_generate(list_id):
    """ Generate charts from a summaly of SVIS results. """
    # Local variables.
    name_suspectible = "S+P_E"
    list_target_status = [name_suspectible] + config.STATUS_LIST[2:]
    num_agent = len(list_id[0])

    # Read summaly files.
    df_stats_day = pd.read_csv(os.path.join(*config.SUMMARY_DIR, config.PATH_AGENT_STATUS_SUMMARY_DAYS), encoding="utf_8_sig")
    df_stats_cumsum_sim = pd.read_csv(os.path.join(*config.SUMMARY_DIR, config.PATH_AGENT_STATUS_SUMMARY_SIMULATIONS_WITH_CUMSUM), encoding="utf_8_sig")
    df_offline_online_each_student = pd.read_csv(os.path.join(*config.SUMMARY_DIR, config.PATH_AGENT_OFFLINE_ONLINE_SUMMARY_EACH_AGENTS), encoding="utf_8_sig")

    # Generate charts.
    generate_timeseries_graph("sier", df_stats_day, list_target_status, num_agent)
    generate_timeseries_graph("pe", df_stats_day, [config.PRE_EXPOSED], num_agent)
    generate_boxplot_graph(df_stats_cumsum_sim, [config.INFECTED], ["perday", "max"], num_agent)
    generate_boxplot_graph(df_stats_cumsum_sim, [config.INFECTED], ["perweek", "max"], num_agent*7)
    generate_boxplot_graph(df_stats_cumsum_sim, [config.INFECTED], ["per2week", "max"], num_agent*14)
    generate_histogram_graph(df_offline_online_each_student, config.ONLINE, config.LESSON_DAYS * config.LESSON_NUM)
    generate_histogram_graph(df_offline_online_each_student, config.OFFLINE, config.LESSON_DAYS * config.LESSON_NUM)
    generate_histogram_graph(df_offline_online_each_student, config.NO_LESSON, config.LESSON_DAYS * config.LESSON_NUM)


def generate_timeseries_graph(file_keyword, df_stats, list_target_status, max_ylim, list_cmap=None):
    """ Generate a timeseries graph for each target status using summary dataframe of SVIS. """
    # Prepare valiables.
    steps = np.arange(len(df_stats))
    if list_cmap is None:
        list_cmap = plt.get_cmap("tab10")

    # Generate figure frame.
    fig, ax = plt.subplots(figsize=(8.0, 6.0))

    # Plot each status.
    for idx, one_status in enumerate(list_target_status):
        temp_mean = df_stats.loc[:, "{}_mean".format(one_status)]
        temp_std = df_stats.loc[:, "{}_std".format(one_status)]
        ax.plot(steps, temp_mean, lw=2, label=one_status, color=list_cmap(idx))
        ax.fill_between(steps, temp_mean+temp_std, temp_mean-temp_std, facecolor=list_cmap(idx), alpha=0.5)
    # Set legend.
    ax.legend()
    ax.set_xlabel('Day')
    ax.set_ylabel('Number of agents')
    # Set grid.
    ax.grid()
    ax.set_ylim([0, max_ylim])
    plt.grid(color='black', linestyle='dotted', linewidth=1)
    fig.tight_layout()
    # Save figure.
    fig.savefig(os.path.join(*config.SUMMARY_GRAPH_DIR, config.PATH_AGENT_STATUS_SUMMARY_COUNT_TIMESERIES_GRAPH.format(file_keyword)))
    plt.clf()
    plt.close()


def generate_boxplot_graph(df_stats, list_target_status, list_type, max_ylim):
    """ Generate a boxplot graph for each target status in list_type using summary dataframe of SVIS. """
    # Prepare and adjust variables.
    if not isinstance(list_target_status, list):
        list_target_status = list(list_target_status)
    tgt_index, tgt_stats = list_type

    for one_status in list_target_status:
        # Prepare figure frame.
        fig, ax = plt.subplots(figsize=(8.0, 6.0))
        # Plot data.
        ax.boxplot(df_stats.loc[:, "{}_{}_{}".format(one_status, tgt_index, tgt_stats)])
        # Set axis.
        ax.set_xticklabels(["Status-{}".format(one_status)])
        ax.set_ylim([0, max_ylim])
        plt.ylabel('Number of agents')
        plt.grid(color='black', linestyle='dotted', linewidth=1)
        fig.tight_layout()
        # Save figure.
        fig.savefig(os.path.join(*config.SUMMARY_GRAPH_DIR, config.PATH_AGENT_STATUS_SUMMARY_COUNT_BOXPLOT_GRAPH.format(one_status, tgt_index, tgt_stats)))
        plt.clf()
        plt.close()


def generate_histogram_graph(df_stats, target_status, max_xlim):
    """ Generate a timeseries graph for each target status using summary dataframe of SVIS. """
    # Generate figure frame.
    fig, ax = plt.subplots(figsize=(8.0, 6.0))

    # Plot each status.
    plt.hist(df_stats[target_status].values.tolist(), density=True, range=(0, max_xlim))
    # Set legend.
    ax.set_xlabel('Day')
    ax.set_ylabel('Number of agents')
    # Set grid.
    ax.grid()
    plt.grid(color='black', linestyle='dotted', linewidth=1)
    fig.tight_layout()
    # Save figure.
    fig.savefig(os.path.join(*config.SUMMARY_GRAPH_DIR, config.PATH_AGENT_STATUS_SUMMARY_COUNT_TIMESERIES_GRAPH.format(target_status)))
    plt.clf()
    plt.close()