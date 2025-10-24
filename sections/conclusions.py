# insights, implications, next steps
import streamlit as st

st.set_page_config(page_title="Data Storytelling Dashboard", layout="wide")

def write(df_raw, tables):
    """
    Writes the conclusions page of the Streamlit app.
    """
    st.header("🎯 Key Insights & Next Steps")
    st.markdown("---")

    st.info("""
    ### Key Insights

    1. **Regional Disparities:**  
       Hospitalization and death rates vary significantly across French regions. **Île-de-France** and **Grand Est** experienced higher peaks, while regions like **Bretagne** had comparatively moderate rates. This highlights the need for region-specific health strategies.

    2. **Distinct Wave Patterns:**  
       Multiple waves of COVID-19 affected France at different times. Peaks correspond with major outbreaks, demonstrating how viral variants and public health measures shaped the pandemic trajectory.

    3. **Impact on Healthcare Systems:**  
       Hospitalization surges closely aligned with ICU occupancy and critical care pressures. Regions with sustained high hospitalization rates faced greater strain on healthcare resources.

   """)

    st.markdown("---")
    
    st.info("""
    ### Next Steps & Recommendations

    1. **Correlation Analysis:**  
       Explore how hospitalization rates relate to vaccination coverage, mobility patterns, or socio-economic factors to identify drivers of regional variation.

    2. **Predictive Modeling:**  
       Develop time-series models to forecast hospitalizations, deaths, or ICU occupancy. This can inform early-warning systems for future waves or other health crises.

    3. **Policy Simulation & Scenario Planning:**  
       Simulate interventions such as vaccination campaigns, lockdown measures, or hospital capacity expansions to evaluate their potential effectiveness.

    """)

    st.markdown("---")
    st.success("This dashboard provides a foundation for understanding the pandemic's impact on France's healthcare system and supports evidence-based decision-making for future health crises.")
