# School-Virus-Infection-Simulator
        
## Setting

SVIS refers to the following **<a href="#configini">`config.ini`</a>** and **<a href="#schedule-files">`schedule files`</a>** in input folder.<br>

### Config.ini

[SIMULATION]

- `calendar_path`: calendar file path

When calendar_path is None or empty, SVIS creates agent schedules <a href="#schedule-files">(schedule files)</a> automatically based on [GENERATE] section parameters.

- `output_root_dir`: root directory path of outputs
- `simulation_count`: number of simulations
- `lesson_time`: lesson time (min)
- `random_seed`: random seed of simulations

[AGENT]

- `mask`: students wear masks or don't (True/False). When `mask` is True, SVIS uses [INFECTION] `exhalation_filtration_efficiency` and `respiration_filtration_efficiency`.

[INFECTION]

- `pulmonary_ventilation_rate`: pulmonary ventilation rate (m3/h) <br>
- `quantum_generation_rate`:  <a href="#quantum-generation-rate-dai-2020-fisk-2004">quantum generation rate (quantum/h)</a>
- `exhalation_filtration_efficiency`:  exhalation filtration efficiency. When `mask` is False, `exhalation_filtration_efficiency` becomes zero.
- `respiration_filtration_efficiency`:  respiration filtration efficiency. When `mask` is False, `respiration_filtration_efficiency` becomes zero.
- `asymptomatic_rate`: Infectious-exposed students become Asymptomatic with `asymptomatic_rate`.
- `exposed_limit_days`: days of being Exposed status
- `infecting_exposed_limit_days`: days of being Infectious-exposed status
- `infected_limit_days`: days of being Infectious status
- `infected_asymptomatic_limit_days`: days of being Asymptomatic status


#### Example parameters of [INFECTION] section as below.
```
pulmonary_ventilation_rate = 0.54
quantum_generation_rate = 48
exhalation_filtration_efficiency = 0.5
respiration_filtration_efficiency = 0.5
asymptomatic_rate = 0.3
exposed_limit_days = 3
infecting_exposed_limit_days = 2
infected_limit_days = 14
infected_asymptomatic_limit_days = 8
```
Buonanno estimated the pulmonary ventilation rate of sedentary activities 0.54(m3/h) (Buonanno, 2020; Adams, 1983).<br>
&emsp;➡&emsp;pulmonary_ventilation_rate = 0.54<br>
Dai calculated the quanta generation rate of COVID-19 as 14-48 in 2020 (Dai, 2020). We adopt 48 as 𝑞 because the Delta variant is spreading worldwide, and the infectability is estimated to be stronger than the original (CDC, 2021a).<br>
&emsp;➡&emsp;quantum_generation_rate = 48<br>
Dai estimates the exhalation filtration efficiency and the respiration filtration efficiency as 0.5 when all students wear a mask (Dai, 2020).<br>
&emsp;➡&emsp;exhalation_filtration_efficiency = 0.5<br>
&emsp;➡&emsp;respiration_filtration_efficiency = 0.5<br>
We consider the CDC estimate of the percentage of infections that are asymptomatic as 30% as the current best (CDC, 2021c).<br>
&emsp;➡&emsp;asymptomatic_rate = 0.3<br>
CDC says "isolation, and pre-cautions can be discontinued 10 days after symptom onset and after resolution of fever for at least 24 hours and improvement of other symptoms" (CDC, 2021b). Then, we roughly estimated 14 as infected days.<br>
&emsp;➡&emsp;infected_limit_days = 14<br>
Dai estimates that infectability is a peek at two days before to one day after symptom onset and WHO states "the time from exposure to COVID-19 to the moment when symptoms begin is, on average, 5 to 6 days." Hence, we adopted three days and two days as exposed days and infectious-exposed days (WHO, 2021; He, 2020). <br>
&emsp;➡&emsp;exposed_limit_days = 3<br>
&emsp;➡&emsp;infecting_exposed_limit_days = 2<br>
Bullard estimates that SARS-CoV-2 infected Vero cell infectivity is only observed eight days after symptom onset (Bullard, 2020); hence, we adopted eight days as asymptomatic days.<br>
&emsp;➡&emsp;infected_asymptomatic_limit_days = 8<br>

#### Quantum Generation Rate (Dai, 2020; Fisk, 2004)
| Disease | Quantum generation rate |
----|---- 
| Tuberculosis |1-50 / h|
| MERS |6-140 / h|
| SARS |10-300 / h|
| Influenza |15-500 / h|
| Measles |570-5600 / h|
| COVID-19 |14-48 / h|

[GENERATE]

- `agent_num`: num of students
- `classroom_num`: num of classrooms per lesson
- `classoom_volume`: classroom volume (m3)
- `classroom_ach`: air change rate of classroom <br> The air change rate is a measurement of how much fresh/clean air replaces indoor air in one hour.
- `lesson_days`: days of lessons
- `lesson_num`: num of lessons per day
- `generate_seed`: random seed of generating schedule

#### Example of creating agent schedules <a href="#schedule-files">(schedule files)</a> automatically based on [GENERATE] section parameters.
```
[SIMULATION]
calendar_path = 
output_root_dir = output
simulation_count = 100
lesson_time = 100
random_seed = None

[AGENT]
mask = True

[INFECTION]
pulmonary_ventilation_rate = 0.54
quantum_generation_rate = 48
exhalation_filtration_efficiency = 0.5
respiration_filtration_efficiency = 0.5
asymptomatic_rate = 0.3
exposed_limit_days = 3
infecting_exposed_limit_days = 2
infected_limit_days = 14
infected_asymptomatic_limit_days = 8

[GENERATE]
agent_num = 100
classroom_num = 4
classroom_volume = 180
classroom_ach = 3
lesson_days = 100
lesson_num = 4
generate_seed = None
```

#### Example of using <a href="#schedule-files">schedule files</a>.
```
[SIMULATION]
calendar_path = simulation_calendar.csv
output_root_dir = output
simulation_count = 100
lesson_time = 100
random_seed = None

[AGENT]
mask = True

[INFECTION]
pulmonary_ventilation_rate = 0.54
quantum_generation_rate = 48
exhalation_filtration_efficiency = 0.5
respiration_filtration_efficiency = 0.5
asymptomatic_rate = 0.3
exposed_limit_days = 3
infecting_exposed_limit_days = 2
infected_limit_days = 14
infected_asymptomatic_limit_days = 8

[GENERATE]
agent_num = 100
classroom_num = 4
classroom_volume = 180
classroom_ach = 3
lesson_days = 100
lesson_num = 4
generate_seed = None
```

### Schedule Files

**<a href="#directory-structure">`simulation_calendar.csv`</a>** describes schedules of students and classrooms.<br>

```
daycount, agent_schedule, classroom_schedule
0, agent_schedule_mon.csv, classroom_mon.csv
1, agent_schedule_tue.csv, classroom_tue.csv
2, agent_schedule_wed.csv, classroom_wed.csv
3, agent_schedule_thu.csv, classroom_thu.csv
4, agent_schedule_fri.csv, classroom_fri.csv
5, , 
6, , 
7, agent_schedule_mon.csv, classroom_mon.csv
8, agent_schedule_tue.csv, classroom_tue.csv
```

<br>

**<a href="#directory-structure">`agent_schedule_XXX.csv`</a>** describes schedules of students.<br>
You can change `agent_schedule_XXX` as you like.<br>

```
step, agent000, agent001, agent002, agent003, agent004
0, lesson0-3, lesson0-1, lesson0-0, lesson0-2, lesson0-1
1, lesson1-1, lesson1-0, lesson1-3, lesson1-1, lesson1-2
2, lesson2-1, lesson2-1, lesson2-2, lesson2-1, lesson2-3
3, lesson3-3, lesson3-0, lesson3-2, lesson3-0, lesson3-0
```

<br>

**<a href="#directory-structure">`classroom_XXX.csv`</a>**  describes lessons' schedules of classrooms, classroom volume, and classroom's air change rate (ach).<br>
You can change `classroom_XXX` as you like.<br>

```
lesson, classroom, volume, ach
lesson0-0, classroom0, 180, 3
lesson0-1, classroom1, 180, 3
lesson0-2, classroom2, 180, 3
lesson0-3, classroom3, 180, 3
lesson1-0, classroom0, 180, 3
lesson1-1, classroom1, 180, 3
lesson1-2, classroom2, 180, 3
lesson1-3, classroom3, 180, 3
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
