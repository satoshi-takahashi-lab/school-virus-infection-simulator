# School-Virus-Infection-Simulator

## Output

SVIS outputs following **<a href="#graphs">`graphs`</a>** and **<a href="#csv-files">`csv files`</a>** to output/YYYYMMDD_HHMMSS/graph, output/YYYYMMDD_HHMMSS/log, and output/YYYYMMDD_HHMMSS/summary.<br>


### Graphs

#### Legends

S: Susceptible.<br>
P_E: P_E is a student who becomes Exposed on that day. P_E becomes E (Exposed) the next day.<br>
E: Exposed.<br>
I_E: Infectious-exposed.<br>
I_A: Asymptomatic.<br>
I: Infectious.<br>
R: Removed.<br>

**<a href="#directory-structure">`summary_agent_status_count_sier_timeseries.png`</a>** describes the daily number of each status student.<br>
The filled area shows the standard deviation, and the line shows the average.<br>
<img src="https://user-images.githubusercontent.com/89981267/138490116-4de41584-a457-4e9a-b325-62f19db4a6cd.png" width="500"><br>
<br>

**<a href="#directory-structure">`summary_agent_status_count_pe_timeseries.png`</a>** describes the daily number of newly infected students.<br>
<img src="https://user-images.githubusercontent.com/89981267/138490417-50c46378-0020-4428-8fe8-28ffa6b3bd56.png" width="500"><br>
<br>

**<a href="#directory-structure">`summary_agent_status_count_I-perday-max_boxplot.png`</a>**, **<a href="#directory-structure">`summary_agent_status_count_I-perweek-max_boxplot.png`</a>**, and **<a href="#directory-structure">`summary_agent_status_count_I-per2week-max_boxplot.png`</a>** describe the maximum number of students infected simultaneously per day, per week, and per two weeks.<br>
<img src="https://user-images.githubusercontent.com/89981267/138490841-a7667bbc-818d-491d-baf1-6d78f6d0dc94.png" width="250">
<img src="https://user-images.githubusercontent.com/89981267/138490851-37000da0-a900-4f1b-a1d3-839b0accfa41.png" width="250">
<img src="https://user-images.githubusercontent.com/89981267/138490868-dc34d873-db12-4383-8efa-bf507b529e4c.png" width="250"><br>


### CSV Files

#### Students Status

S: Susceptible.<br>
P_E: P_E is a student who becomes Exposed on that day. P_E becomes E (Exposed) the next day.<br>
E: Exposed.<br>
I_E: Infectious-exposed.<br>
I_A: Asymptomatic.<br>
I: Infectious.<br>
R: Removed.<br>

#### log
**<a href="#directory-structure">`simXXXX_agent_status_logger.csv`</a>** describes each student's status at each step.<br>
XXXX is the sequential number of simulations.<br>

```
daycount, step, agent000, agent001, agent002, agent003,	agent004
0, 0, I_E, S, S, S, S
0, 1, I_E, S, S, S, S
0, 2, I_E, S, S, S, S
0, 3, I_E, S, P_E, S, S
1, 0, I_E, S, E, S, S
```

<br>

**<a href="#directory-structure">`simXXXX_agent_status_logger_count.csv`</a>** describes the number of each status student at each step.<br>

```
daycount, step, S, P_E, E, I_E, I, I_A, R
0, 0, 99, 0, 0, 1, 0, 0, 0
0, 1, 98, 1, 0, 1, 0, 0, 0
0, 2, 98, 1, 0, 1, 0, 0, 0
0, 3, 98, 1, 0, 1, 0, 0, 0
1, 0, 98, 0, 1, 1, 0, 0, 0
```

<br>

**<a href="#directory-structure">`simXXXX_classroom_infection_rate_logger.csv`</a>** describes the infection_rate of each classroom at each step.<br>

```
daycount, step, lesson_name, classroom_name, infection_rate_with_mask, infection_rate_without_mask
0, 0, lesson0-0, classroom0, 0, 0
0, 0, lesson0-1, classroom1, 0, 0
0, 0, lesson0-2, classroom2, 0, 0
0, 0, lesson0-3, classroom3, 0.019801327, 0.076883654
0, 1, lesson1-0, classroom0, 0, 0
```

#### summary
**<a href="#directory-structure">`summary_agent_status_count_eachDay.csv`</a>** describes fundamental statistics of S+P_E, S, P_E, E, I_E, I, and R at each step.<br>

```
daycount, step, S+P_E_mean, S+P_E_std, S+P_E_min, S+P_E_quartile1, S+P_E_median, S+P_E_quartile3, S+P_E_max, S_mean,,,,
0, 0, 99, 0, 99, 99, 99, 99, 99, 98.53,,,,
1, 0, 97.14, 1.28723335, 93, 96, 97, 98, 99, 96.7,,,,
2, 0, 95.27, 1.879474459, 90, 94, 95, 96.25, 99, 95.07,,,,
3, 0, 94.72, 2.370185178, 88, 93, 95, 96, 99, 94.61,,,,
```

<br>

**<a href="#directory-structure">`summary_agent_status_count_eachSim.csv`</a>** describes fundamental statistics of S+P_E, S, P_E, E, I_E, I, and R at each simulation.<br>

```
sim_num, S+P_E_mean, S+P_E_std, S+P_E_min, S+P_E_quartile1, S+P_E_median, S+P_E_quartile3, S+P_E_max, S_mean,,,,
0, 18.5, 33.66036545, 0, 0, 0, 14, 99, 18.22,,,,
1, 12.62, 27.27294882, 1, 1, 1, 1, 99, 12.25,,,,
2, 23.02, 36.08966947, 2, 2, 2, 23.5, 99, 22.79,,,,
3, 98.01, 0.1, 98, 98, 98, 98, 99, 98.01,,,,
```

<br>

**<a href="#directory-structure">`summary_agent_status_count-cumsum_eachDay.csv`</a>** describes fundamental statistics of I per day, per week, and per two weeks at step zero of each day.<br>

```
daycount, step, I_perday_mean, I_perday_std, I_perday_min, I_perday_quartile1, I_perday_median, I_perday_quartile3, I_perday_max, I_perweek_mean,,,,
0, 0, 0, 0, 0, 0, 0, 0, 0,,,,
1, 0, 0, 0, 0, 0, 0, 0, 0,,,,
2, 0, 0.74, 0.440844002, 0, 0, 1, 1, 1,,,,
3, 0, 0.74, 0.440844002, 0, 0, 1, 1, 1,,,,
```

<br>

**<a href="#directory-structure">`summary_agent_status_count-cumsum_eachSim.csv`</a>** describes fundamental statistics of I per day, per week, and per two weeks at each simulation.<br>

```
sim_num, I_perday_mean, I_perday_std, I_perday_min, I_perday_quartile1, I_perday_median, I_perday_quartile3, I_perday_max, I_perweek_mean,,,,
0, 9.94, 15.93789715, 0, 0, 0, 13.25, 51, 73.91489362,,,,
1, 9.94, 18.63515739, 0, 0, 0, 7, 61, 74.0212766,,,,
2, 10.64, 18.2460844, 0, 0, 1, 12.25, 59, 79.12765957,,,,
3, 0.28, 0.636911741, 0, 0, 0, 0, 2, 1.978723404,,,,
```

<br>

**<a href="#directory-structure">`summary_classroom_infection_rate_allSim.csv`</a>** describes total number of classroom's infection probability on each day.<br>

```
daycount, 0, <=0.05, <=0.10, <=0.15, <=0.20, <=0.25, <=0.30,,,,
0, 1200, 400, 0, 0, 0, 0, 0,,,,
1, 1200, 400, 0, 0, 0, 0, 0,,,,
2, 1496, 104, 0, 0, 0, 0, 0,,,,
3, 1496, 104, 0, 0, 0, 0, 0,,,,
```

## Directory Structure
```
.
├── svis.exe
├── main.py
├── example_input
├── src
├── input
│   ├── config.ini
│   ├── simulation_calendar.csv
│   ├── agent_schedule
│   │   ├── agent_schedule_XXX.csv (You can change agent_schedule_XXX as you like.)
│   │   └── ...
│   └── classroom_schedule
│       ├── classroom_XXX.csv (You can change classroom_XXX as you like.)
│       └── ...
└── output
    ├── YYYYMMDD_HHMMSS
    │   ├── graph
    │   │   ├── summary_agent_status_count_sier_timeseries.png
    │   │   ├── summary_agent_status_count_pe_timeseries.png
    │   │   ├── summary_agent_status_count_I-perday-max_boxplot.png
    │   │   ├── summary_agent_status_count_I-perweek-max_boxplot.png
    │   │   └── summary_agent_status_count_I-per2week-max_boxplot.png
    │   ├── log
    │   │   ├── sim0000_agent_status_logger.csv
    │   │   ├── simXXXX_agent_status_logger.csv
    │   │   ├── ...
    │   │   ├── sim0000_agent_status_logger_count.csv
    │   │   ├── simXXXX_agent_status_logger_count.csv
    │   │   ├── ...
    │   │   ├── sim0000_classroom_infection_rate_logger.csv
    │   │   ├── simXXXX_classroom_infection_rate_logger.csv
    │   │   └── ...
    │   ├── summary
    │   │   ├── summary_agent_status_count_eachDay.csv
    │   │   ├── summary_agent_status_count_eachSim.csv
    │   │   ├── summary_agent_status_count-cumsum_eachDay.csv
    │   │   ├── summary_agent_status_count-cumsum_eachSim.csv
    │   │   ├── summary_classroom_infection_rate_allSim.csv
    │   └── input
    └── ...    
```
