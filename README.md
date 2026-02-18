# A New American Dream: Analyzing and Predicting Retirement Trends in America

Emma Smith

Dr. Bu Hyoung Lee

May 2026

DS796 Data Science Project

### Summary

This project explores retirement trends in America by utilizing
statistical methods and models with The University of Michigan's
Health and Retirement Study (HRS).

## Data

<details>
  <summary>Variables: Click to View Table</summary>

| **Variable Name**                                                      | **Description**                                                                                          | **Original Name**           | **Ref** |
|------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|-----------------------------|---------|
| Respondent Variables                                                   |                                                                                                          |                             |         |
| r_age_ss_payments                                                      | Age in months that Respondent started to receive Social Security payments                                | RASSAGEM                    | 1389    |
| r_birth_yr                                                             | Respondent Birth Year                                                                                    | RABYEAR                     | 120     |
| r_child_born                                                           | Number of children ever born                                                                             | RAEVBRN                     | 1774    |
| r_edu_high_deg                                                         | Respondent Highest Degree-Masked                                                                         | RAEDEGRM                    | 165     |
| r_edu_sum                                                              | Respondent Education Summary                                                                             | RAEDUC                      | 169     |
| r_edu_yrs                                                              | Respondent Years of Education                                                                            | RAEDYRS                     | 162     |
| r_gender                                                               | Respondent Gender                                                                                        | RAGENDER                    | 142     |
| r_ID                                                                   | 9-character version of combined household and person identifier that identifies each Respondent uniquely | RAHHIDPN                    | 60      |
| r_race                                                                 | Respondent Race-Masked                                                                                   | RARACEM                     | 144     |
|                                                                        |                                                                                                          |                             |         |
| Respondent Wave Variables                                              |                                                                                                          |                             |         |
| r{w}_age_yrs_mid                                                       | Respondent Age in years during midpoint of interview                                                     | Rw_AGEY_M                   | 140     |
| r{w}_has_partner                                                       | Respondent has Spouse or Partner                                                                         | RwMPART                     | 186     |
| r{w}_health_self_reported                                              | Respondent Self-Report of Health                                                                         | RwSHLT                      | 247     |
| r{w}_income                                                            | Respondent Income                                                                                        | RwIEARN                     | 1247    |
| r{w}_job_hours                                                         | Hours worked/week main job                                                                               | RwJHOURS                    | 1919    |
| r{w}_job_industry_1980; r{w}_job_industry_2002; r{w}_job_industry_2007 | Current Job Industry (1980 census; 2002 census; 2007 census)                                             | RwJCIND; RwJCINDB; RwJCINDC | 1978    |
| r{w}_job_physical                                                      | Current job requires physical effort                                                                     | RwJPHYS                     | 1943    |
| r{w}_job_stress                                                        | Current job requires much stress                                                                         | RwJSTRES                    | 1959    |
| r{w}_labor_status                                                      | Respondent Labor Force Status                                                                            | RwLBRF                      | 1897    |
| r{w}_retire_mon                                                        | Retirement Month                                                                                         | RwRETMON                    | 1782    |
| r{w}_retire_yr                                                         | Retirement Year                                                                                          | RwRETYR                     | 1782    |
| r{w}_urbanicity                                                        | Urbanicity                                                                                               | RwURBRUR                    | 158     |
|                                                                        |                                                                                                          |                             |         |
| Household Wave Variables                                               |                                                                                                          |                             |         |
| hh{w}_debt                                                             | Assets: Debts – Cross-wave                                                                               | HwADEBT                     | 1197    |
| hh{w}_wealth                                                           | Net Value of Total Wealth for Household (replace H with R for Respondent only)                           | HwATOTB                     | 1241    |
| hh{w}_single_or_couple                                                 | Household treated as a couple                                                                            | HwCPL                       | 96      |
| hh{w}_total_income                                                     | Respondent+Spouse Household income                                                                       | HwITOT                      | 1352    |
|                                                                        |                                                                                                          |                             |         |

</details>

## Code

<details> 
<summary>Installing Python Packages</summary>

``
pip install -r requirements.txt
``
</details>


#### References
* [RAND HRS Longitudinal File 2022](https://hrsdata.isr.umich.edu/data-products/rand-hrs-longitudinal-file-2022).
* [RAND HRS Longitudinal File 2022 Codebook](https://hrsdata.isr.umich.edu/sites/default/files/documentation/other/1758643082/randhrs1992_2022v1.pdf)
* The HRS (Health and Retirement Study) is sponsored by the National Institute on Aging (grant
number NIA U01AG009740) and is conducted by the University of Michigan.
* Health and Retirement Study, (RAND HRS Longitudinal File) public use dataset. Produced and
distributed by the University of Michigan with funding from the National Institute on Aging
(grant number NIA U01AG009740). Ann Arbor, MI, (2025).
* RAND HRS Longitudinal File. Produced by the RAND Center for the Study of Aging, with
funding from the National Institute on Aging and the Social Security Administration.
Santa Monica, CA (May 2025).