# School-Virus-Infection-Simulator
## Overview
School-Virus-Infection-Simulator (SVIS) is a tool to simulate the spread of infection at a school considering the students' lesson schedules, classroom volume, air circulation rates in classrooms, and infectability of the students.<br>
See <a href="https://www.researchgate.net/publication/355140672_School_Virus_Infection_Simulator_for_Customizing_School_Schedules_During_COVID-19">School Virus Infection Simulator for Customizing School Schedules During COVID-19</a>.<br>
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
Students' status consists of susceptible, exposed, infectious-exposed, infectious, asymptomatic, and recovered.<br>
Susceptible students become exposed according to <a href="#infection-probability">the infection probability</a>.<br>
Exposed students become infectious-exposed after <a href="readme/README_SETTING.md#configini">a certain period</a>.<br>
Infectious-exposed students become infectious or asymptomatic, <a href="readme/README_SETTING.md#configini">probabilistically</a>, after <a href="readme/README_SETTING.md#configini">a certain period</a>.<br>
Infectious and asymptomatic students recover after <a href="readme/README_SETTING.md#configini">a certain period</a>.<br>
Infectious-exposed and asymptomatic students infect susceptible students according to <a href="#infection-probability">infection probability</a>.<br>
Infectious components are the students who develop symptoms and take the day off.<br>
Asymptomatic students do not develop symptoms and continue school.<br>
SVIS generates students from one to <a href="readme/README_SETTING.md#configini">agent_num</a>(number of students) and makes student one as infectious-exposed on day 0.<br>
<br>
<img src="https://user-images.githubusercontent.com/89981267/138493715-a6b62088-a2de-47db-b275-7d2a4d23b332.png" width="500"><br>

## Output

SVIS outputs following graphs and csv files to output/YYYYMMDD_HHMMSS/graph, output/YYYYMMDD_HHMMSS/log, and output/YYYYMMDD_HHMMSS/summary.<br>
See <a href="readme/README_OUTPUT.md">README_OUTPUT.md</a>.<br>

## Setting

SVIS refers to the following config.ini and schedule files in input folder.<br>
See <a href="readme/README_SETTING.md">README_SETTING.md</a>.<br>

## Infection Probability
Infection probability is calculated based on Wells-Riley Equation (Riley, 1978; Dai, 2020).<br><br>
<img src="https://latex.codecogs.com/gif.latex?P=1-e^{-Iqpt(1-n_{I})(1-n_{S})/Q}" title="P=1-e^{-Iqpt(1-n_{I})(1-n_{S})/Q}" /><br><br>
*P* is the probability of infection.<br>
*I* is the number of source patients (Infectious students).<br>
*q* is the quantum generation rate produced by one infector (quantum/h).<br>
*p* is the pulmonary ventilation rate of each susceptible per hour (m3/h).<br>
*Q* is the room ventilation rate (m3/h).<br>
*t* is the exposure time (h).<br>
<img src="https://latex.codecogs.com/gif.latex?n_{I}" title="n_{I}" /> is the exhalation filtration efficiency.<br>
<img src="https://latex.codecogs.com/gif.latex?n_{S}" title="n_{S}" /> is the respiration filtration efficiency.<br>

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

## Example of Schedule Files
Examples of schedule files is in example_input folder.<br>

### Classroom Type
Self-contained: Students take the same lesson in the same classroom.<br>
Departmentalized: Students take individual lessons in different classrooms.<br>

### Schedule Type
|  | P100_Ba | P50_HD_2G-1 | P50_D_2G-1 | P50_Ds_2G-1 | P50_W_2G-1 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| Number of groups |1|2|2|2|2|
| Number of face-to-face lesson groups <br> at one time |1|1|1|1|1|
| A continuous period <br> of face-to-face lesson <br> for each group |Always|A half-day|One day|Two and a half days|One week|
| A continuous period <br> of not going to a school <br> for each group |No|A half-day|One day|Two and a half days|One week|
| Percentage of face-to-face lessons |100%|50%|50%|50%|50%|

### Correspondence Table between UNESCO's Sample Schedules and Example (UNESCO, 2020)
<img src="https://user-images.githubusercontent.com/89981267/138521876-266b6bbf-aad1-45f3-900b-a7d2e89eae6b.png" width="500"><br>

### Result of Example

#### Legends

S: Susceptible.<br>
P_E: P_E is a student who becomes Exposed on that day. P_E becomes E (Exposed) the next day.<br>
E: Exposed.<br>
I_E: Infectious-exposed.<br>
I_A: Asymptomatic.<br>
I: Infectious.<br>
R: Removed.<br>

#### Base Pattern
Schedule files are generated based on input/config.ini.<br>
<img src="https://user-images.githubusercontent.com/89981267/138511531-fdcc2b1d-cff6-4b80-9a79-0e2ae7760fcf.png" width="250"><br>

#### Departmentalized
<img src="https://user-images.githubusercontent.com/89981267/138541121-d6c2ca75-9533-4d1b-ac8c-b9c977192dd0.png" width="700"><br>

#### Self-contained
<img src="https://user-images.githubusercontent.com/89981267/138541147-9e2bc778-7560-45a8-b9d8-f843b1327d3f.png" width="700"><br>


## References
(Adams, 1983) W. C. Adams. 1993. Measurement of breathing rate and volume in routinely performed daily activities. Final Report Contract A033-205 (1993).<br>
(Bullard, 2020) Jared Bullard, Kerry Dust, Duane Funk, James E. Strong, David Alexander, Lauren Garnett, Carl Boodman, Alexander Bello, Adam Hedley, Zachary Schiffman, et al. 2020. Predicting infectious severe acute respiratory syndrome coronavirus 2 from diagnostic samples. Clinical infectious diseases 71, 10 (2020), 2663–2666.<br>
(Buonanno, 2020) Giorgio Buonanno, Lidia Morawska, and Luca Stabile. 2020. Quantitative assessment of the risk of airborne transmission of SARS-CoV-2 infection: prospective and retrospective applications. Environment international 145 (2020), 106112.<br>
(CDC, 2021a) Centers for Disease Control and Prevention. 2021. Delta Variant: What We Know About the Science. Accessed Sep. 21, 2021. https://www.cdc.gov/coronavirus/2019-ncov/variants/delta-variant.html<br>
(CDC, 2021b) Centers for Disease Control and Prevention. 2021. Ending Home Isolation for Persons with COVID-19 Not in Healthcare Settings. Accessed Sep. 21, 2021. https://www.cdc.gov/coronavirus/2019-ncov/hcp/disposition-in-home-patients.html<br>
(CDC, 2021c) Centers for Disease Control and Prevention. 2021. Transmission of SARS-CoV-2: implications for infection prevention precautions. Accessed Sep. 21, 2021. https://www.cdc.gov/coronavirus/2019-ncov/hcp/planning-scenarios.html<br>
(Dai, 2020) Hui Dai and Bin Zhao. 2020. Association of the infection probability of COVID-19 with ventilation rates in confined spaces. Building Simulation 13 (2020), 1321–1327. https://doi.org/10.1007/s12273-020-0703-5<br>
(Fisk, 2004) William J. Fisk, Olli Seppanen, David Faulkner, and Joe Huang. 2004. Economic benefits of an economizer system: Energy savings and reduced sick leave. Lawrence Berkeley National Laboratory. Retrieved from https://escholarship.org/uc/item/4wz9x840<br>
(He, 2020) Xi He, Eric H. Y. Lau, Peng Wu, and et al. 2020. Temporal dynamics in viral shedding and transmissibility of COVID-19. Nature Medicine 26 (2020), 672–675. https://doi.org/10.1038/s41586-020-2271-3<br>
(Riley, 1978) E. C. Riley, G. Murphy, and R. L. Riley. 1978. Airborne spread of measles in a suburban elementary school. American Journal of Epidemiology 107 (1978), 421–432. https://doi.org/10.1093/oxfordjournals.aje.a112560<br>
(UNESCO, 2020) UNESCO. 2020. COVID-19 response–hybrid learning, Hybrid learning as a key element in ensuring continued learning. Accessed Sep. 21, 2021. https://en.unesco.org/sites/default/files/unesco-covid-19-response-toolkit-hybrid-learning.pdf<br>
(WHO, 2021) World Health Organization. 2020. Coronavirus disease (COVID-19). Accessed Sep. 21, 2021. https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19<br>



## Author
 
* Satoshi Takahashi, Kanto Gakuin University, satotaka@kanto-gakuin.ac.jp, ORCID: 0000-0002-1067-6704
* Masaki Kitazawa, Kitazawa Tech and Rikkyo University, masaki.kitazawa@rikkyo.ac.jp, ORCID: 0000-0002-6352-0164
* Atsushi Yoshikawa, Tokyo Institute of Technology and Rikkyo University, at_sushi_bar@dis.titech.ac.jp, ORCID: 0000-0001-7020-508

## License

"School-Virus-Infection-Simulator" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
