# School-Virus-Infection-Simulator
## Overview
School-Virus-Infection-Simulator (SVIS) is a tool to simulate the spread of virus infection at a school.<br>
SVIS simulates students' behavior based on their lesson schedule, classrooms volume, classrooms air change rate, and infectability of the virus.<br>
***You can run SVIS by its executable file on Windows.***

## Usage
`python main.py` or run `svis.exe`

## Requirements

When you run `main.py`, you need Python 3.9.7 and requirements as below.

```
matplotlib==3.4.3
numpy==1.21.2
pandas==1.3.2
```

## Infection Model
SVIS is based on Susceptible-Exposed-Infectious-Removed Agent Based Model.<br>
Students change their status as below.<br>
Susceptible ➡ Exposed ➡ Infecting Exposed ➡ Infectious ➡ Removed<br>
Susceptible students become Exposed according to <a href="#infection-probability">infection probability</a>.<br>
Exposed students become Infecting Exposed, Infectious, and Removed after <a href="#configini">a certain period</a>.<br>
Infecting Exposed students infect Susceptible according to <a href="#infection-probability">infection probability</a>.<br>
Infectious students take the day off school.<br>
SVIS picks one student randomly and makes him or her as Infecting Exposed at day 0.

## Output

SVIS outputs following graphs and csv files to <a href="#directory-structure">`output/YYYYMMDD_HHMMSS/graph`</a> and <a href="#directory-structure">`output/YYYYMMDD_HHMMSS/log`</a>.<br>

***

### Graphs

**<a href="#directory-structure">`agent_status_logger_summary_count_sier.png`</a>** describes the daily number of each status student.<br>
The filled area shows the standard deviation, and the line shows the average.<br>
<img src="https://user-images.githubusercontent.com/89981267/132156495-ad67de5a-18a3-4235-b74d-32c58653e196.png" width="500"><br>
<br>

**<a href="#directory-structure">`agent_status_logger_summary_count_pe.png`</a>** describes the daily number of newly infected students.<br>
<img src="https://user-images.githubusercontent.com/89981267/132156452-e1d802d0-6800-4d84-bdef-535e69619cae.png" width="500"><br>
<br>

**<a href="#directory-structure">`agent_status_logger_summary_count_i_boxplot.png`</a>** describes the total number of infected students.<br>
<img src="https://user-images.githubusercontent.com/89981267/132156454-5e8c5237-d388-48d5-8287-57d01123ff11.png" width="500"><br>

***

### CSV Files

#### Students Status

S: Susceptible.<br>
P_E: P_E is a student who becomes Exposed on that day. P_E becomes E (Exposed) the next day.<br>
E: Exposed.<br>
I_E: Infecting Exposed.<br>
I: Infectious.<br>
R: Removed.<br>
<br>

**<a href="#directory-structure">`simXXX_agent_status_logger.csv`</a>** describes each student's status.<br>
XXX is the sequential number of simulations.<br>

```
daycount, step, agent000, agent001, agent002, agent003,	agent004
0, 0, I_E, S, S, S, S
0, 1, I_E, S, S, S, S
0, 2, I_E, S, S, S, S
0, 3, I_E, S, P_E, S, S
1, 0, I_E, S, E, S, S
```

<br>

**<a href="#directory-structure">`simXXX_agent_status_logger_count.csv`</a>** describes the number of each status student on each day and lesson.<br>

```
daycount,step,S,P_E,E,I_E,I,R
0, 0, 99, 0, 0, 1, 0, 0
0, 1, 96, 3, 0, 1, 0, 0
0, 2, 96, 3, 0, 1, 0, 0
0, 3, 93, 6, 0, 1, 0, 0
1, 0, 92, 1, 6, 1, 0, 0
```

<br>

**<a href="#directory-structure">`simXXX_classroom_infection_rate_logger.csv`</a>** describes the infection_rate of each classroom.<br>

```
daycount, step, lesson0-0_classroom, lesson0-1_classroom, lesson0-2_classroom, lesson0-3_classroom, lesson1-0_classroom, lesson1-1_classroom, lesson1-2_classroom, lesson1-3_classroom
0, 0, classroom0, classroom1, classroom2, classroom3, -, -, -, -
0, 1, 0, 0.01488806, 0, 0, classroom0, classroom1, classroom2, classroom3
0, 2, -, -, -, -, -, -, -, -
0, 3, -, -, -, -, -, -, -, -
1, 0, classroom0, classroom1, classroom2, classroom3, -, -, -, -
1, 1, 0, 0.01488806, 0, 0, classroom0, classroom1, classroom2, classroom3
1, 2, -, -, -, -, -, -, -, -
1, 3, -, -, -, -, -, -, -, -
```

## Infection Probability
Infection probability is calculated based on Wells-Riley Equation (Riley, 1978; Dai, 2020).<br>
<a href="https://www.codecogs.com/eqnedit.php?latex=P=1-e^{-Iqpt/Q}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P=1-e^{-Iqpt/Q}" title="P=1-e^{-Iqpt/Q}" /></a><br>
*P* is the probability of infection.<br>
*I* is the number of source patients (Infecting Exposed stundents).<br>
*q* is the quantum generation rate produced by one infector (quantum/h).<br>
*p* is the pulmonary ventilation rate of each susceptible per hour (m3/h).<br>
*Q* is the room ventilation rate (m3/h).<br>
*t* is the exposure time (h).<br>

## Directory Structure
```
.
├── svis.exe
├── main.py
├── example_input
├── scr
├── input
│   ├── config.ini
│   ├── simulation_calendar.csv
│   ├── agent_schedule
│   │   ├── agent_schedule_XXX.csv
│   │   └── ...
│   └── classroom_schedule
│       ├── classroom_XXX.csv
│       └── ...
└── output
    ├── YYYYMMDD_HHMMSS
    │   ├── graph
    │   │   ├── agent_status_logger_summary_count_sier.png
    │   │   ├── agent_status_logger_summary_count_pe.png
    │   │   └── agent_status_logger_summary_count_i_boxplot.png
    │   ├── log
    │   │   ├── sim000_agent_status_logger.csv
    │   │   ├── simXXX_agent_status_logger.csv
    │   │   ├── ...
    │   │   ├── sim000_agent_status_logger_count.csv
    │   │   ├── simXXX_agent_status_logger_count.csv
    │   │   ├── ...
    │   │   ├── sim000_classroom_infection_rate_logger.csv
    │   │   ├── simXXX_classroom_infection_rate_logger.csv
    │   │   └── ...
    │   └── input
    └── ...    
```
        
## Setting

SVIS refers to the following <a href="#configini">config.ini</a> and <a href="#schedule-files">schedule files</a> in <a href="#directory-structure">`input`</a>.<br>

### Config.ini

[SIMULATION]

- `calendar_path`: calendar file path

When calendar_path is None or empty, SVIS creates agent schedules <a href="#schedule-files">(schedule files)</a> automatically based on [GENERATE] section parameters.

- `output_root_dir`: root directory path of outputs
- `simulation_count`: number of simulations
- `random_seed`: random seed of simulations

[AGENT]

- `mask`: students wear masks or don't (True/False)

When both the infectors and susceptibles wear masks, the ventilation rate increases to 4 times equivalently (Dai, 2020).

[CLASSROOM]

- `classoom_volume`: classroom volume (m3)
- `classroom_ach`: air change rate of classroom <br> The air change rate is a measurement of how much fresh/clean air replaces indoor air in one hour (Liu, 2020)
- `lesson_time`: lesson time (min)

[INFECTION]

- `pulmonary_ventilation_rate`: pulmonary ventilation rate (m3/h) <br> *p*=0.3 m3/h when people sitting or doing light activityindoor (Davies, 2013).
- `quantum_generation_rate`:  <a href="#quantum-generation-rate-dai-2020-fisk-2014">quantum generation rate (quantum/h)</a>
- `exposed_limit_days`: days of being exposed status
- `infecting_exposed_limit_days`: days of being infecting exposed status
- `infected_limit_days`: days of being infected status

#### Example parameters of [INFECTION] section as below.
"At least 10 days* have passed since symptom onset" and "At least 24 hours have passed since resolution of fever without the use of fever-reducing medications" and "Other symptoms have improved." (CDC, 2020).<br>
➡　infected_limit_days = 14<br>
"infectiousness was shown to peak at 2 days before to 1 day after symptom onset (He, 2020)."<br>
➡　infecting_exposed_limit_days = 2<br>
The time from exposure to COVID-19 to the moment when symptoms begin is, on average, 5-6 days (WHO, 2020).<br>
➡　exposed_limit_days + infecting_exposed_limit_days = 5<br>

```
exposed_limit_days = 3
infecting_exposed_limit_days = 2
infected_limit_days = 14
```


[GENERATE]

- `agent_num`: num of students
- `classroom_num`: num of classrooms per lesson
- `lesson_days`: days of lessons
- `lesson_num`: num of lessons per day
- `generate_seed`: random seed of generating schedule

#### Example of createing agetnt schedules <a href="#schedule-files">(schedule files)</a> automaticaly based on [GENERATE] section parameters.
```
[SIMULATION]
calendar_path = 
output_root_dir = output
simulation_count = 100
random_seed = None

[AGENT]
mask = False

[CLASSROOM]
classroom_volume = 400
classroom_ach = 4
lesson_time = 100

[INFECTION]
pulmonary_ventilation_rate = 0.3
quantum_generation_rate = 48
exposed_limit_days = 3
infecting_exposed_limit_days = 2
infected_limit_days = 14

[GENERATE]
agent_num = 100
classroom_num = 4
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
random_seed = None

[AGENT]
mask = False

[CLASSROOM]
classroom_volume = 400
classroom_ach = 4
lesson_time = 100

[INFECTION]
pulmonary_ventilation_rate = 0.3
quantum_generation_rate = 48
exposed_limit_days = 3
infecting_exposed_limit_days = 2
infected_limit_days = 14

[GENERATE]
agent_num = 
classroom_num = 
lesson_days = 
lesson_num = 
generate_seed = 
```

#### Quantum Generation Rate (Dai, 2020; Fisk, 2014)
| Disease | Quantum generation rate |
----|---- 
| Tuberculosis |1-50 / h|
| MERS |6-140 / h|
| SARS |10-300 / h|
| Influenza |15-500 / h|
| Measles |570-500 / h|
| COVID-19 |14-48 / h|

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
You can change `agent_schedule_` as you like.<br>

```
step, agent000, agent001, agent002, agent003, agent004
0, lesson0-3, lesson0-1, lesson0-0, lesson0-2, lesson0-1
1, lesson1-1, lesson1-0, lesson1-3, lesson1-1, lesson1-2
2, lesson2-1, lesson2-1, lesson2-2, lesson2-1, lesson2-3
3, lesson3-3, lesson3-0, lesson3-2, lesson3-0, lesson3-0
```

<br>

**<a href="#directory-structure">`classroom_XXX.csv`</a>**  describes lessons' schedules of classrooms, classroom volume, and classroom's air change rate (ach).<br>
You can change `classroom_` as you like.<br>

```
lesson, classroom, volume, ach
lesson0-0, classroom0, 400, 10
lesson0-1, classroom1, 400, 10
lesson0-2, classroom2, 400, 10
lesson0-3, classroom3, 400, 10
lesson1-0, classroom0, 400, 10
lesson1-1, classroom1, 400, 10
lesson1-2, classroom2, 400, 10
lesson1-3, classroom3, 400, 10
```

## Example of Schedule Files
An example of schedule files is in <a href="#directory-structure">example_input</a>.<br>
The example simulates  students' behavior from April 10 for 110 days in a Japanese school.<br>
Japanese schools are off from the day of 19 to the day of 27, called Golden Week.<br>
The number of students is 200.<br>
Forty-eight days later, some classroom volumes change large.<br>
The result shows that the number of Exposed students decreases suddenly on the day of 19 at the start of Golden Week.<br>
Then, no newly infected students apppears after Golden Week because exposed_limit_days + infecting_exposed_limit_days = 5 < Golden Week = 9.<br>
Please note that exposed_limit_days, infecting_exposed_limit_days, and infected_limit_days are constant and not probabilistic under this version SVIS.<br>
<br>

**<a href="#directory-structure">`agent_status_logger_summary_count_sier.png`</a>** describes the daily number of each status student.<br>

<img src="https://user-images.githubusercontent.com/89981267/132248366-3cee0731-3186-48d5-ae82-6577f7f0cf9f.png" width="500"><br>

## References

[1] Centers for Disease Control and Prevention (CDC) (2020). Ending Home Isolation for Persons with COVID-19 Not in Healthcare Settings. https://www.cdc.gov/coronavirus/2019-ncov/hcp/disposition-in-home-patients.html (Last Updated: Feb. 18, 2021).<br>
[2] Dai, H., Zhao, B. (2020). Association of the infection probability of COVID-19 with ventilation rates in confined spaces. Building Simulation, 13, 1321–1327. doi: 10.1007/s12273-020-0703-5.<br>
[3] Davies A, Thompson K.A., Giri K., Kafatos G., Walker J., Bennett A. (2013). Testing the efficacy of homemade masks: would they protect in an influenza pandemic? Disaster Medicine and Public Health Preparedness. 7, 413–418. doi: 10.1017/dmp.2013.43.<br>
[4] Fisk, W., Seppanen, O., Faulkner, D., & Huang, J. (2004). Economic benefits of an economizer system: Energy savings and reduced sick leave. Lawrence Berkeley National Laboratory. Retrieved from https://escholarship.org/uc/item/4wz9x840<br>
[5] He, X., Eric H. Y. L., Peng, W., Xilong D., Jian W., Xinxin H., Yiu C. L., et al. (2020). Temporal dynamics in viral shedding and transmissibility of COVID-19. Nature medicine. 26, 672-675.
[6] Liu Y, .Ning Z., Chen Y., Guo M., Liu Y., et al. (2020). Aerodynamic analysis of SARS-CoV-2 in two Wuhan hospitals. Nature. 582, 557–560. doi: 10.1038/s41586-020-2271-3.<br>
[7] Riley E. C., Murphy G., Riley R. L. (1978). Airborne spread of measles in a suburban elementary school. American Journal of Epidemiology. 107, 421–432. doi: 10.1093/oxfordjournals.aje.a112560.<br>
[8] World Health Organization (WHO) (2020). Coronavirus disease (COVID-19). https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19 (Last Updated: Oct. 12, 2020).<br>

## Author
 
* Satoshi Takahashi, Kanto Gakuin University, satotaka@kanto-gakuin.ac.jp, ORCID: 0000-0002-1067-6704
* Masaki Kitazawa, Kitazawa Tech and Rikkyo University, masaki.kitazawa@rikkyo.ac.jp, ORCID: 0000-0002-6352-0164
* Atsushi Yoshikawa, Tokyo Institute of Technology and Rikkyo University, at_sushi_bar@dis.titech.ac.jp, ORCID: 0000-0001-7020-508

## License

"School-Virus-Infection-Simulator" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
