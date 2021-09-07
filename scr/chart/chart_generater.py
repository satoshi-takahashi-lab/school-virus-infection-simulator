import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scr import config

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
plt.rcParams["legend.handlelength"] = 1             # Set legend line length.
plt.rcParams["legend.handletextpad"] = 3.           # Set legend distance between line to string.
plt.rcParams["legend.markerscale"] = 2              # Set legend marker scale.
plt.rcParams["legend.borderaxespad"] = 0.           # Set distance between legend box and graph.


def chart_generate():
    # Local variables.
    name_suspectible = "S+P_E"

    # Prepare list of target count files.
    logger_files = glob.glob(os.path.join(*config.LOGGER_DIR, '*.csv'))
    agent_status_logger_count_files = [one_log for one_log in logger_files if config.AGENT_STATUS_LOGGER_COUNT_PATH in one_log]
    multi_flag = bool(len(agent_status_logger_count_files) != 1)

    # Prepare data.
    for idx, one_file in enumerate(agent_status_logger_count_files):
        # Read and concat the agent status count data. Use only step=1 data for each day.
        if idx == 0:
            df_agent_status_logger_count = pd.read_csv(one_file, encoding="utf_8_sig")
            temp_agent_num = df_agent_status_logger_count.loc[0, config.STATUSLIST].sum()
            df_agent_status_logger_count[name_suspectible] = df_agent_status_logger_count[config.SUSCEPTIBLE] + df_agent_status_logger_count[config.PRE_EXPOSED]
            df_agent_status_logger_count = df_agent_status_logger_count[df_agent_status_logger_count["step"] == 1]
        else:
            temp_df = pd.read_csv(one_file, encoding="utf_8_sig")
            temp_df[name_suspectible] = temp_df[config.SUSCEPTIBLE] + temp_df[config.PRE_EXPOSED]
            df_agent_status_logger_count = pd.concat([df_agent_status_logger_count, temp_df[temp_df["step"] == 1]], axis=1)

    generate_sier_graph(df_agent_status_logger_count, temp_agent_num, name_suspectible, multi_flag)
    generate_pe_graph(df_agent_status_logger_count, temp_agent_num, multi_flag)
    generate_boxplot(df_agent_status_logger_count, temp_agent_num)


def generate_sier_graph(df_agent_status_logger_count, agent_num, name_suspectible, multi_flag):
    """ AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_SIER_PATH """
    # Prepare plt.
    fig, ax = plt.subplots(figsize=(8.0, 6.0))
    steps = np.arange(len(df_agent_status_logger_count))
    # Plot susceptible + pre_exposed agents count.
    if multi_flag:
        df_agent_status_logger_summary_count_susceptible_pre_exposed = df_agent_status_logger_count[name_suspectible]
        color = 'blue'
        temp_mean = df_agent_status_logger_summary_count_susceptible_pre_exposed.T.describe().loc['mean']
        temp_std = df_agent_status_logger_summary_count_susceptible_pre_exposed.T.describe().loc['std']
        ax.plot(steps, temp_mean, lw=2, label='S', color=color)
        ax.fill_between(steps, temp_mean+temp_std, temp_mean-temp_std, facecolor=color, alpha=0.5)
        # Plot exposed agents count.
        df_agent_status_logger_summary_count_exposed = df_agent_status_logger_count[config.EXPOSED]
        color = 'yellow'
        temp_mean = df_agent_status_logger_summary_count_exposed.T.describe().loc['mean']
        temp_std = df_agent_status_logger_summary_count_exposed.T.describe().loc['std']
        ax.plot(steps, temp_mean, lw=2, label='E', color=color)
        ax.fill_between(steps, temp_mean+temp_std, temp_mean-temp_std, facecolor=color, alpha=0.5)
        # Plot infecting exposed agents count.
        df_agent_status_logger_summary_count_infecting_exposed = df_agent_status_logger_count[config.INFECTING_EXPOSED]
        color = 'red'
        temp_mean = df_agent_status_logger_summary_count_infecting_exposed.T.describe().loc['mean']
        temp_std = df_agent_status_logger_summary_count_infecting_exposed.T.describe().loc['std']
        ax.plot(steps, temp_mean, lw=2, label='I_E', color=color)
        ax.fill_between(steps, temp_mean+temp_std, temp_mean-temp_std, facecolor=color, alpha=0.5)
        # Plot infected agents count.
        df_agent_status_logger_summary_count_infected = df_agent_status_logger_count[config.INFECTED]
        color = 'pink'
        temp_mean = df_agent_status_logger_summary_count_infected.T.describe().loc['mean']
        temp_std = df_agent_status_logger_summary_count_infected.T.describe().loc['std']
        ax.plot(steps, temp_mean, lw=2, label='I', color=color)
        ax.fill_between(steps, temp_mean+temp_std, temp_mean-temp_std, facecolor=color, alpha=0.5)
        # Plot recovered agents count.
        df_agent_status_logger_summary_count_recovered = df_agent_status_logger_count[config.RECOVERED]
        color = 'green'
        temp_mean = df_agent_status_logger_summary_count_recovered.T.describe().loc['mean']
        temp_std = df_agent_status_logger_summary_count_recovered.T.describe().loc['std']
        ax.plot(steps, temp_mean, lw=2, label='R', color=color)
        ax.fill_between(steps, temp_mean+temp_std, temp_mean-temp_std, facecolor=color, alpha=0.5)
    else:
        ax.plot(steps, df_agent_status_logger_count[name_suspectible], lw=2, label='S', color="blue")
        ax.plot(steps, df_agent_status_logger_count[config.EXPOSED], lw=2, label='E', color="yellow")
        ax.plot(steps, df_agent_status_logger_count[config.INFECTING_EXPOSED], lw=2, label='I_E', color="red")
        ax.plot(steps, df_agent_status_logger_count[config.INFECTED], lw=2, label='I', color="pink")
        ax.plot(steps, df_agent_status_logger_count[config.RECOVERED], lw=2, label='R', color="green")
    # Set legend.
    ax.legend()
    ax.set_xlabel('Day')
    ax.set_ylabel('Number')
    # Set grid.
    ax.grid()
    ax.set_ylim([0, agent_num])
    plt.grid(color='black', linestyle='dotted', linewidth=1)
    fig.tight_layout()
    # Save figure.
    fig.savefig(os.path.join(*config.AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_DIR, config.AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_SIER_PATH))
    plt.clf()
    plt.close()


def generate_pe_graph(df_agent_status_logger_count, agent_num, multi_flag):
    """ AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_PE_PATH """
    # Prepare plt.
    fig, ax = plt.subplots(figsize=(8.0, 6.0))
    steps = np.arange(len(df_agent_status_logger_count))
    # Plot pre exposed agents count.
    if multi_flag:
        df_agent_status_logger_summary_count_pre_exposed = df_agent_status_logger_count[config.PRE_EXPOSED]
        color = 'red'
        temp_mean = df_agent_status_logger_summary_count_pre_exposed.T.describe().loc['mean']
        temp_std = df_agent_status_logger_summary_count_pre_exposed.T.describe().loc['std']
        ax.plot(steps, temp_mean, lw=2, label='P_E', color=color)
        ax.fill_between(steps, temp_mean+temp_std, temp_mean-temp_std, facecolor=color, alpha=0.5)
    else:
        ax.plot(steps, df_agent_status_logger_count[config.PRE_EXPOSED], lw=2, label='P_E', color="red")
    # Set legend.
    ax.legend()
    ax.set_xlabel('Day')
    ax.set_ylabel('Number')
    # Set grid.
    ax.grid()
    ax.set_ylim([0, agent_num])
    plt.grid(color='black', linestyle='dotted', linewidth=1)
    fig.tight_layout()
    # Save figure.
    fig.savefig(os.path.join(*config.AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_DIR, config.AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_PE_PATH))
    plt.clf()
    plt.close()


def generate_boxplot(df_agent_status_logger_count, agent_num):
    """ AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_I_BOXPLOT_PATH """
    # Prepare plt.
    fig, ax = plt.subplots(figsize=(8.0, 6.0))
    # Plot data.
    df_agent_status_logger_summary_count_infected = df_agent_status_logger_count[config.INFECTED]
    ax.boxplot(df_agent_status_logger_summary_count_infected.max())
    # Set axis.
    ax.set_xticklabels(['Infected'])
    ax.set_ylim([0, int(agent_num*1.25)])
    plt.ylabel('Number')
    plt.grid(color='black', linestyle='dotted', linewidth=1)
    fig.tight_layout()
    # Save figure.
    fig.savefig(os.path.join(*config.AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_DIR, config.AGENT_STATUS_LOGGER_SUMMARY_COUNT_GRAPH_I_BOXPLOT_PATH))
    plt.clf()
    plt.close()
