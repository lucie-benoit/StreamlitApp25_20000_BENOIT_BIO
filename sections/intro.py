# sections/intro.py
import streamlit as st
from utils.prep import show_data_quality, cleaning, feature_engineering, validate_data
st.set_page_config(page_title="Data Storytelling Dashboard", layout="wide")
def write(df_raw, tables):
    df = tables["full"]
    st.title("🔍 Data Storytelling : How did COVID-19 hit France ?")

    st.caption(
        'Source: [Données hospitalières relatives à l\'épidémie de COVID-19](https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/) — Portal: [Data.gouv](https://www.data.gouv.fr/datasets) - [Licence Ouverte / Open Licence](https://www.etalab.gouv.fr/licence-ouverte-open-licence)'
    )

    # --- Dashboard Sections ---
    st.info(
        """
        The COVID-19 pandemic has put French hospital systems under immense strain. 
        
        **But has this impact been uniform across the country? How has it evolved over the course of the waves?**

        From the first sudden surge in spring 2020 to the later waves driven by new variants, hospitals faced unprecedented challenges—overcrowded ICUs, exhausted medical staff, 
        and regional disparities in resources. 
        
        **Understanding how different regions were affected, and how the pressure on healthcare evolved over time, reveals not only the severity of the crisis but also the resilience and adaptability of the French healthcare system.** """
    )
    st.markdown("Use the navigation panel on the left to explore different sections and select specific regions or timeframes.")
    st.markdown("---")

    # --- Understanding and Objectives ---
    st.header("📑 Understanding the Objectives")
    st.info(
        """
        This interactive dashboard explores and analyzes COVID-19 trends across French regions (2020–2023).  

        **Goals:**
        - Provide a clear overview of the pandemic's impact on the healthcare system.
        - Compare national trajectories with regional variations in hospitalization, death, and critical care rates.
        - Explore epidemic waves, identify underlying factors, and support public health policy decisions.

        The following chart shows the **overall trend in hospital admissions** across France over time.
        """
    )

    # Timeseries chart
    st.subheader("Hospitalization Rates Over Time (Accumulated)")
    timeseries = df.groupby('jour')['tx_indic_7J_hosp'].sum().reset_index()
    st.line_chart(timeseries.set_index('jour')['tx_indic_7J_hosp'])  # type: ignore  

    st.info(
        """
        #### Why This Matters
        COVID-19 reshaped healthcare systems across France. Regional hospitalization patterns reveal where resources were most strained — and where resilience emerged.

        #### Data Context
        This dashboard uses official French regional data (2020–2023):
        - Hospitalization rates (`tx_indic_7J_hosp`)
        - Critical care rates (`tx_indic_7J_SC`)
        - Death rates (`tx_indic_7J_DC`)

        ➡️ Select a region on the sidebar to explore its evolution over time.
        """
    )

    st.markdown(
        """
        - Only hospitalizations with SARS-CoV-2 infection (**PourAvec = 0**) are represented.  
        - Rates are calculated per 100,000 inhabitants and include:
            - New hospitalization rate  
            - Death rate  
            - New critical care rate  
            - Intensive care rate  
            - Overall hospitalization rate
        """
    )
    st.markdown("---")

    # --- Data Quality & Caveats ---
    st.header("📈 Data Quality & Caveats")
    st.info(
        """
        - **Source:** Official French government open data portal  
        - **Coverage:** March 2020 – June 2023  
        - **Limitations:** Some missing values and data gaps
        """
    )

    # Missing values analysis
    st.subheader("Missing Values: Raw Data")
    show_data_quality(df_raw)
    st.markdown(
        "Some death values are missing because deaths are classified depending on hospitalization type (0, 1, or 2). "
        "All hospitalizations from types 1 and 2 were regrouped under type 0."
    )

    st.subheader("Missing Values: After Cleaning")
    df_cleaned = cleaning(df_raw.copy())
    show_data_quality(df_cleaned)

    # Feature engineering
    df_clean = cleaning(df_raw.copy())
    df_features = feature_engineering(df_clean)
    df_validated = validate_data(df_features)

    st.markdown("---")
    st.header("ℹ️ Feature Engineering")
    st.info(
        """
        Key feature engineering steps:
        - **Region Names:** Mapped region codes to human-readable names.
        - **Growth Rate Calculation:** Added weekly hospitalization growth rate column.
        """
    )

    st.subheader("Missing Values: After Feature Engineering")
    df_fe = feature_engineering(df_cleaned.copy())
    show_data_quality(df_fe)
    st.markdown(
        "Some hospitalization growth rate values are missing when the previous week's hospitalization rate is zero, making the percentage change undefined."
    )

    st.subheader("Data Overview (After Cleaning)")
    st.dataframe(df_validated.head(20))
