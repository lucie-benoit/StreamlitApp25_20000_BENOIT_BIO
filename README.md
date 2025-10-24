\# COVID-19 Data Storytelling Dashboard – France



This interactive \*\*Streamlit dashboard\*\* explores COVID-19 hospitalization, critical care, and death trends across French regions from \*\*March 2020 to June 2023\*\*.  

It allows users to visualize epidemic waves, compare regional impacts, and understand healthcare pressures over time. The dashboard is designed to support data-driven insights for public health and policymaking.



---



\## Table of Contents

\- \[Installation](#installation)

\- \[Usage](#usage)

\- \[Data](#data)

\- \[Features](#features)

\- \[Structure](#structure)

\- \[Acknowledgements](#acknowledgements)



---



\## Installation


1\. Clone the repository:

```bash

git clone https://github.com/username/project.git

2.Navigate to the project folder:

cd project

3.Install dependencies:

pip install -r requirements.txt

4.Run the Streamlit app:

streamlit run app.py

---

Usage

Use the sidebar controls to select regions, dates, and metrics.

Navigate through sections using the radio button panel:



* Introduction: Overview of the data, context, objectives, and data quality checks.
* Dashboard Overview: KPIs, trends over time, and geographical distributions.
* Regional Deep Dive: Detailed comparisons between regions, epidemic wave analysis, and hospitalization growth rates.
* Conclusions: Key insights and actionable next steps.

---

Data


The dashboard uses official French government COVID-19 datasets from data.gouv.fr :

* Hospitalization rates (tx\_indic\_7J\_hosp)
* Critical care rates (tx\_indic\_7J\_SC)
* Death rates

Coverage: March 2020 – June 2023.


---


Notes:


* Only hospitalizations with SARS-CoV-2 infection (PourAvec = 0) are included.
* Rates are normalized per 100,000 inhabitants.

---


Features


Interactive Timeseries: Visualize hospitalizations, critical care, and death trends over time.


Regional Comparison: Compare metrics across regions with line charts, bar charts, and maps.


Epidemic Wave Analysis: Identify peaks and track waves using smoothed metrics.


Hospital Pressure Indicators: Early warning metrics based on growth rates.


Data Quality \& Feature Engineering: Transparency on cleaning steps, missing values, and derived features.