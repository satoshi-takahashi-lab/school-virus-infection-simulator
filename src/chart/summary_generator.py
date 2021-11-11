import os
import glob
import numpy as np
import pandas as pd
from src import config



def generate_summary():
    """ Generate summary files from simulated logs. """
    # Prepare list of target files.
    logger_files = glob.glob(os.path.join(*config.OUTPUT_ROOT_DIR, "log", "*.csv"))
    list_path_agent_status_count = [one_log for one_log in logger_files if config.AGENT_STATUS_LOGGER_COUNT_PATH in one_log]
    list_path_classroom_infection_log = [one_log for one_log in logger_files if config.CLASSROOM_INFECTION_RATE_LOGGER_PATH in one_log]

    # Summarize agent status count data.
    df_stats_sim, df_stats_day, df_stats_cumsum_sim, df_stats_cumsum_day = summarize_agent_status_count(list_path_agent_status_count)

    # Summarize classroom infection rate data.
    df_freq_inf_rate_with_mask, df_freq_inf_rate_without_mask = summarize_classroom_infection_rate(list_path_classroom_infection_log)

    # Save dataframes.
    save_df(config.SUMMARY_DIR, config.PATH_AGENT_STATUS_SUMMARY_SIMULATIONS, df_stats_sim)
    save_df(config.SUMMARY_DIR, config.PATH_AGENT_STATUS_SUMMARY_DAYS, df_stats_day)
    save_df(config.SUMMARY_DIR, config.PATH_AGENT_STATUS_SUMMARY_SIMULATIONS_WITH_CUMSUM, df_stats_cumsum_sim)
    save_df(config.SUMMARY_DIR, config.PATH_AGENT_STATUS_SUMMARY_DAYS_WITH_CUMSUM, df_stats_cumsum_day)
    if config.MASK:
        save_df(config.SUMMARY_DIR, config.PATH_CLASSROOM_INFECTION_RATE_SUMMALY, df_freq_inf_rate_with_mask)
    else:
        save_df(config.SUMMARY_DIR, config.PATH_CLASSROOM_INFECTION_RATE_SUMMALY, df_freq_inf_rate_without_mask)


def summarize_agent_status_count(list_path):
    """ Summarize results of agents' status count logs by SVIS. \n
        Calculate statistics of agents' status count \n
        of each day/simulation or cumulative sum of each day/simulation. """
    # Local variables.
    name_suspectible = "S+P_E"
    list_target_status = [name_suspectible] + config.STATUSLIST
    dict_diff = {"perweek": 7, "per2week": 14}

    # Prepare data
    for idx, one_file in enumerate(list_path):
        # Read and concat the agent status count data. Use only step=0 data for each day.
        if idx == 0:
            df_agent_status_logger_count = pd.read_csv(one_file, encoding="utf_8_sig")
            df_agent_status_logger_count[name_suspectible] = df_agent_status_logger_count[config.SUSCEPTIBLE] + df_agent_status_logger_count[config.PRE_EXPOSED]
            df_agent_status_logger_count = df_agent_status_logger_count[df_agent_status_logger_count["step"] == 0]
        else:
            temp_df = pd.read_csv(one_file, encoding="utf_8_sig")
            temp_df[name_suspectible] = temp_df[config.SUSCEPTIBLE] + temp_df[config.PRE_EXPOSED]
            df_agent_status_logger_count = pd.concat([df_agent_status_logger_count, temp_df[temp_df["step"] == 0]], axis=1)

    # Calculate statistics of each day/simulation.
    df_stats_sim = calc_status_stats(df_agent_status_logger_count, list_target_status, calc_type=0)
    df_stats_day = calc_status_stats(df_agent_status_logger_count, list_target_status, calc_type=1)
    # Calculate statistics with cumulative sum of each day/simulation.
    df_stats_cumsum_sim = calc_stats_with_cumsum(df_agent_status_logger_count, [config.INFECTED], dict_diff, calc_type=0)
    df_stats_cumsum_day = calc_stats_with_cumsum(df_agent_status_logger_count, [config.INFECTED], dict_diff, calc_type=1)

    return df_stats_sim, df_stats_day, df_stats_cumsum_sim, df_stats_cumsum_day


def calc_status_stats(df_tgt, list_tgt_status, calc_type=0):
    """ Calculate statistics of target status types. \n
        calc_type=0: calculate for each simulation result. \n
        calc_type=1: calculate for each daycount result. """
    # Prepare front side of dataframe.
    if calc_type == 0:
        sim_num = len(df_tgt[list_tgt_status[0]].columns)
        output_df = pd.DataFrame([i for i in range(sim_num)], columns=["sim_num"])
    else:
        output_df = df_tgt.iloc[:, :2].copy()

    # Calculate statistics.
    for one_status in list_tgt_status:
        if calc_type == 0:
            # Each simulation.
            temp_df = df_tgt[one_status].copy().T
            output_df.loc[:, "{}_mean".format(one_status)] = temp_df.mean(axis=1).values.T
            output_df.loc[:, "{}_std".format(one_status)] = temp_df.std(axis=1).values.T
            output_df.loc[:, "{}_min".format(one_status)] = temp_df.min(axis=1).values.T
            output_df.loc[:, "{}_quartile1".format(one_status)] = temp_df.quantile(q=0.25, axis=1).values.T
            output_df.loc[:, "{}_median".format(one_status)] = temp_df.median(axis=1).values.T
            output_df.loc[:, "{}_quartile3".format(one_status)] = temp_df.quantile(q=0.75, axis=1).values.T
            output_df.loc[:, "{}_max".format(one_status)] = temp_df.max(axis=1).values.T
        else:
            # Each day.
            temp_df = df_tgt[one_status].copy()
            output_df.loc[:, "{}_mean".format(one_status)] = temp_df.mean(axis=1)
            output_df.loc[:, "{}_std".format(one_status)] = temp_df.std(axis=1)
            output_df.loc[:, "{}_min".format(one_status)] = temp_df.min(axis=1)
            output_df.loc[:, "{}_quartile1".format(one_status)] = temp_df.quantile(q=0.25, axis=1)
            output_df.loc[:, "{}_median".format(one_status)] = temp_df.median(axis=1)
            output_df.loc[:, "{}_quartile3".format(one_status)] = temp_df.quantile(q=0.75, axis=1)
            output_df.loc[:, "{}_max".format(one_status)] = temp_df.max(axis=1)

    return output_df


def calc_stats_with_cumsum(df_tgt, list_tgt_status, dict_diff, calc_type=0):
    """ Calculate statistics with cumulative sum of target status types. \n
        "dict_diff" is dictionaly of name key and difference value. ex) {"perweek": 7, "per2week": 14} \n
        calc_type=0: calculate for each simulation result. \n
        calc_type=1: calculate for each daycount result. """
    # Prepare front side of dataframe.
    if calc_type == 0:
        sim_num = len(df_tgt[list_tgt_status[0]].columns)
        output_df = pd.DataFrame([i for i in range(sim_num)], columns=["sim_num"])
    else:
        output_df = df_tgt.iloc[:, :2].copy()

    # Calculate statistics with cumulative sum.
    for one_status in list_tgt_status:
        # Extract target status data.
        one_tgt_df = df_tgt[one_status]
        # Calculate the days difference in dict_diff.
        dict_df_diff = {}
        for one_key, one_diff in dict_diff.items():
            temp_df_diff = one_tgt_df.cumsum().diff(one_diff)
            temp_df_diff.iloc[one_diff-1, :] = one_tgt_df.cumsum().iloc[one_diff-1, :]
            dict_df_diff[one_key] = temp_df_diff

        if calc_type == 0:
            # Each simulation.
            output_df.loc[:, "{}_perday_mean".format(one_status)] = one_tgt_df.T.mean(axis=1).values
            output_df.loc[:, "{}_perday_std".format(one_status)] = one_tgt_df.T.std(axis=1).values
            output_df.loc[:, "{}_perday_min".format(one_status)] = one_tgt_df.T.min(axis=1).values
            output_df.loc[:, "{}_perday_quartile1".format(one_status)] = one_tgt_df.T.quantile(q=0.25, axis=1).values
            output_df.loc[:, "{}_perday_median".format(one_status)] = one_tgt_df.T.median(axis=1).values
            output_df.loc[:, "{}_perday_quartile3".format(one_status)] = one_tgt_df.T.quantile(q=0.75, axis=1).values
            output_df.loc[:, "{}_perday_max".format(one_status)] = one_tgt_df.T.max(axis=1).values
            for one_key, one_diff in dict_diff.items():
                output_df.loc[:, "{}_{}_mean".format(one_status, one_key)] = dict_df_diff[one_key].T.mean(axis=1).values
                output_df.loc[:, "{}_{}_std".format(one_status, one_key)] = dict_df_diff[one_key].T.std(axis=1).values
                output_df.loc[:, "{}_{}_min".format(one_status, one_key)] = dict_df_diff[one_key].T.min(axis=1).values
                output_df.loc[:, "{}_{}_quartile1".format(one_status, one_key)] = dict_df_diff[one_key].T.quantile(q=0.25, axis=1).values
                output_df.loc[:, "{}_{}_median".format(one_status, one_key)] = dict_df_diff[one_key].T.median(axis=1).values
                output_df.loc[:, "{}_{}_quartile3".format(one_status, one_key)] = dict_df_diff[one_key].T.quantile(q=0.75, axis=1).values
                output_df.loc[:, "{}_{}_max".format(one_status, one_key)] = dict_df_diff[one_key].T.max(axis=1).values
        else:
            # Each day.
            output_df.loc[:, "{}_perday_mean".format(one_status)] = one_tgt_df.mean(axis=1)
            output_df.loc[:, "{}_perday_std".format(one_status)] = one_tgt_df.std(axis=1)
            output_df.loc[:, "{}_perday_min".format(one_status)] = one_tgt_df.min(axis=1)
            output_df.loc[:, "{}_perday_quartile1".format(one_status)] = one_tgt_df.quantile(q=0.25, axis=1)
            output_df.loc[:, "{}_perday_median".format(one_status)] = one_tgt_df.median(axis=1)
            output_df.loc[:, "{}_perday_quartile3".format(one_status)] = one_tgt_df.quantile(q=0.75, axis=1)
            output_df.loc[:, "{}_perday_max".format(one_status)] = one_tgt_df.max(axis=1)
            for one_key, one_diff in dict_diff.items():
                # Note: Processing is well done, but numpy warning occurs.
                # Note: Because all the data of first few days in "perweek" and "per2week" become np.NaN.
                output_df.loc[:, "{}_{}_mean".format(one_status, one_key)] = dict_df_diff[one_key].mean(axis=1)
                output_df.loc[:, "{}_{}_std".format(one_status, one_key)] = dict_df_diff[one_key].std(axis=1)
                output_df.loc[:, "{}_{}_min".format(one_status, one_key)] = dict_df_diff[one_key].min(axis=1)
                output_df.loc[:, "{}_{}_quartile1".format(one_status, one_key)] = dict_df_diff[one_key].quantile(q=0.25, axis=1)
                output_df.loc[:, "{}_{}_median".format(one_status, one_key)] = dict_df_diff[one_key].median(axis=1)
                output_df.loc[:, "{}_{}_quartile3".format(one_status, one_key)] = dict_df_diff[one_key].quantile(q=0.75, axis=1)
                output_df.loc[:, "{}_{}_max".format(one_status, one_key)] = dict_df_diff[one_key].max(axis=1)

    return output_df


def summarize_classroom_infection_rate(list_path):
    """ Summarize results of classroom infection rate by SVIS. \n
        Calculate the frequency with 0.05 bin range. \n
        Note: The joint lesson cannot be separated because counting logs line by line. """
    # Prepare bin range.
    # Current: 0.00, <=0.05, <=0.10, <=0.15, ,,, <=1.00
    bins = np.arange(0.0, 1.05, 0.05, dtype=float)
    bins = np.around(bins, decimals=4)
    list_column = ["0.00"] + ["<={:.02f}".format(one_bin) for one_bin in bins[1:]]

    # Read one log file and extract variables for output.
    temp_df = pd.read_csv(list_path[0], encoding="utf_8_sig")
    temp_lesson_days = len(temp_df.drop_duplicates(subset=["daycount"]))
    temp_lesson_num = len(temp_df.drop_duplicates(subset=["step"]))
    temp_df = temp_df.drop_duplicates(subset=["classroom_name"])
    temp_df = temp_df[temp_df["classroom_name"] != "-"]
    temp_df = temp_df[~temp_df["classroom_name"].str.contains("virtual")]
    temp_classroom_num = len(temp_df)

    # Prepare output dataframe.
    output_df_with_mask = pd.DataFrame([], index=range(temp_lesson_days), columns=list_column).fillna(0)
    output_df_with_mask.insert(0, "daycount", output_df_with_mask.index)
    output_df_without_mask = pd.DataFrame([], index=range(temp_lesson_days), columns=list_column).fillna(0)
    output_df_without_mask.insert(0, "daycount", output_df_without_mask.index)

    # Load and store data.
    for one_path in list_path:
        with open(one_path, "r", encoding="utf_8_sig") as open_file:
            next(open_file) # Ignore header.
            for row in open_file:
                # Separate strings with commas.
                list_row = row.replace("\n", "").split(",")

                # Ignore the lesson in virtual classroom.
                if "virtual" in list_row[3]:
                    continue

                # Extract day.
                temp_day = int(list_row[0])

                if list_row[3] == "-":
                    # In holiday, count the infection rate in each classroom of each step as zero.
                    output_df_with_mask.at[temp_day, "0.00"] += temp_lesson_num * temp_classroom_num
                    output_df_without_mask.at[temp_day, "0.00"] += temp_lesson_num * temp_classroom_num
                else:
                    # Add to the target bin.
                    temp_col = list_column[bins[bins < float(list_row[4])].shape[0]]
                    output_df_with_mask.at[temp_day, temp_col] += 1
                    temp_col = list_column[bins[bins < float(list_row[5])].shape[0]]
                    output_df_without_mask.at[temp_day, temp_col] += 1

    return output_df_with_mask, output_df_without_mask


def save_df(list_path_output, name_output, target_df):
    """ Save dataframe. """
    temp_path_output = os.path.join(*list_path_output, name_output)
    target_df.to_csv(temp_path_output, index=False, encoding="utf_8_sig")
