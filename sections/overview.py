import streamlit as st
from utils.viz import bar_chart_death, line_chart, map_chart, map_chart2
from utils.prep import get_filtered_data

def write(df_raw, tables):
    """
    Writes the overview page of the Streamlit app.
    This page contains the main dashboard with KPIs and charts.
    """
    df = tables["full"]
    st.header("📶 Dashboard Overview")
    st.markdown("---")

    # --- Get selected regions and date from session state ---
    regions = st.session_state.get('regions', [])
    selected_date = st.session_state.get("selected_date")

    if not regions:
        st.warning("Please select at least one region in the sidebar to view the charts.")
        return

    # --- Filter data using cached function ---
    filtered_df, latest_data = get_filtered_data(df, regions, selected_date)

    # --- KPI Row ---
    st.subheader("📊 Key Performance Indicators (Based on Selected Date)")
    avg_hosp_rate = latest_data['tx_indic_7J_hosp'].mean()
    avg_dc_rate = latest_data['tx_indic_7J_DC'].mean()

    c1, c2, c3 = st.columns(3)
    c1.metric(
        "Average New Hospitalization Rate (7-day)", 
        f"{avg_hosp_rate:.2f}", 
        help=f"Average 7-day hospitalization rate for selected regions on {selected_date.strftime('%d/%m/%Y')}."
    )
    c2.metric("Number of Regions Selected", len(regions))
    c3.metric(
        "Average Death Rate (7-day)", 
        f"{avg_dc_rate:.2f}", 
        help=f"Average 7-day death rate for selected regions on {selected_date.strftime('%d/%m/%Y')}."
    )

    st.markdown("---")

    # --- Display aggregated chart by region ---
    by_region = df.groupby('region_name')['tx_indic_7J_hosp'].sum().reset_index()
    st.info(
        "While the national trend shows an overall pattern, the impact has been different depending on the regions. "
        "Regions like **Provence-Alpes-Côte d'Azur** and **Île-de-France** experienced higher hospitalization rates during certain waves, while others like **Bretagne** had lower rates. "
        "This regional variation highlights the importance of localized responses to the pandemic."
    )

    st.subheader("Hospitalizations rate by region (accumulated)")
    st.bar_chart(by_region.set_index('region_name')['tx_indic_7J_hosp'])

    # --- Line chart over time ---
    st.info(
        "The pandemic spread differently across regions. Certain regions experienced spikes in new hospitalizations, "
        "reflecting localized outbreaks. **Grand Est** and **Île-de-France** were particularly affected during the initial waves, "
        "while **Bretagne** saw more moderate increases.  \n\n"
        "➡️ *Other regions can be compared in the following chart by selecting them from the sidebar.*"
    )

    line_chart_obj = line_chart(filtered_df, regions, title="New Hospitalizations by Region Over Time")
    st.altair_chart(line_chart_obj, use_container_width=True)

    # --- Maps ---
    st.info(
        "By analyzing the hospitalization and death rates across regions, we can identify areas that were more severely impacted by COVID-19.  \n\n"
        "- **Hospitalization Rate**: Indicates the overall burden on hospitals in each region.  \n"
        "- **Death Rate**: Highlights regions with higher COVID-19 mortality."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Map 1: Hospitalization Rate in France**")
        st.altair_chart(map_chart(df), use_container_width=False)

    with col2:
        st.markdown("**Map 2: Death Rate in France**")
        st.altair_chart(map_chart2(df), use_container_width=False)

    st.markdown("⚠️ Note: DOM-TOM regions are not shown on the map due to the lack of a suitable GeoJSON file.")

    # --- Death comparison ---
    st.info(
        "The death rate is a critical indicator of the pandemic's severity in different regions. "
        "Regions like **Île-de-France** and **Grand Est** exhibited higher death rates, correlating with their elevated hospitalization rates.  \n\n"
        "➡️ *Other regions can be compared in the following chart by selecting them from the sidebar.*"
    )

    bar_chart_obj = bar_chart_death(filtered_df, selected_date)
    st.altair_chart(bar_chart_obj, use_container_width=True)
