# comparisons, distributions, drilldowns
import streamlit as st
from utils.viz import combo_chart, death_rate_during_peaks, hospitalization_growth_rate_chart, ranked_bar_chart, waves
from utils.prep import get_filtered_data

def write(df_raw, tables):
    """
    This page allows for more detailed comparisons between regions.
    """
    df = tables["full"]

    # --- Use cached helper to filter data ---
    selected_regions = st.session_state.get('regions', [])
    selected_date = st.session_state.get('selected_date')

    if not selected_regions or not selected_date:
        st.warning("Please select at least one region and a date in the sidebar.")
        return

    filtered_df, latest_data = get_filtered_data(df, selected_regions, selected_date)


    st.header("📍Regional Deep Dive")
    st.markdown("---")

    # --- Ranked bar chart ---
    st.info("""
    Previously, we explored overall trends in hospitalization rates across different regions using timeseries.

    Here, we dive deeper into regional comparisons through **ranked bar charts**.
    When the pandemic started in France in March 2020, the first regions most impacted were **Grand Est**, **Île-de-France**, and **Bourgogne-Franche-Comté**.

    ➡️ *Change the month and year below to see rankings over time.*
    """)
    st.altair_chart(ranked_bar_chart(df), use_container_width=True)

    # --- Combined hospitalization & critical care ---
    st.info("""
    After ranking hospitalization rates, we can analyze hospitalization and critical care rates together.

    **Critical care rates** indicate healthcare system stress. High rates may suggest hospitals are *overwhelmed*, impacting patient outcomes.
    Comparing hospitalization and critical care rates provides a more comprehensive view.

    ➡️ *Select a region from the dropdown below to see the combined chart.*
    """)
    all_regions = sorted(df["region_name"].dropna().unique())
    region = st.selectbox("Select a Region", all_regions, index=0)

    if region:
        chart_obj = combo_chart(df, region)
        st.altair_chart(chart_obj, use_container_width=True)
    else:
        st.warning("Please select a region to view the chart.")

    # --- Epidemic waves ---
    st.info("""
    Analyzing **epidemic waves** helps understand, anticipate, and control pandemic propagation. 
    It allows monitoring healthcare capacity, evaluating public health measures, understanding virus evolution, and predicting hospital needs.

    **First wave** peaked on 31 March 2020, followed by a small wave in June. 
    The **highest wave** peaked on 20 January 2022, corresponding to the Omicron variant.
    """)
    df_waves, fig_waves = waves(df)
    st.altair_chart(fig_waves, use_container_width=True)
    st.markdown("##### COVID-19 Epidemic Waves Table")
    st.dataframe(df_waves)

    # --- Death rate during peaks ---
    st.info("""
    During the **first waves (spring and autumn 2020)**, hospitalization surges were closely followed by increases in deaths due to limited treatments and ICU overload.
    The **highest death peak** occurred in summer 2021 (**Delta variant**), and during the **highest wave** (Omicron, early 2022), death rates were the highest, showing the variant's impact on hospitals.
    """)
    st.altair_chart(death_rate_during_peaks(df), use_container_width=True)

    # --- Hospitalization growth rate ---
    st.info("""
    The chart below shows **hospitalization growth rates** across regions over time.
    - **Positive growth rates** indicate rising hospitalizations, signaling increased pressure.
    - **Negative growth rates** indicate decreasing hospitalizations, suggesting easing pressure.

    During the **end of 2020**, growth rates were mostly positive, indicating rising hospitalizations, with periods of negative growth reflecting easing hospital pressure.
    
    ➡️ *Select other regions in the sidebar to see different hospitalization growth rate across several regions.*

    """)

    
     # Generate hospitalization growth rate chart
    chart = hospitalization_growth_rate_chart(filtered_df, selected_regions)
    st.altair_chart(chart, use_container_width=True)

