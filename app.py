import streamlit as st
import pandas as pd
from utils.io import load_data
from utils.prep import make_tables
from sections import intro, overview, deep_dives, conclusions

st.set_page_config(page_title="Data Storytelling Dashboard", layout="wide")

# --- 1. Load and Prepare Data (Cached) ---
@st.cache_data(show_spinner="Loading data...")
def get_data():
    """Loads and preprocesses the data."""
    df_raw = load_data()
    tables = make_tables(df_raw.copy()) 
    return df_raw, tables  

df_raw, tables = get_data()
# ---------- menu 

# --- 2. Sidebar / Filters ---
with st.sidebar:
    
    PAGES = {
        "Introduction": intro,
        "Dashboard Overview": overview,
        "Regional Deep Dive": deep_dives,
        "Conclusions": conclusions
    }
    
    st.header("Navigation")
    selection = st.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    
    st.header("Filters")
    all_regions = sorted([r for r in tables["full"]["region_name"].unique() if r])
    
    # Make widgets available to all pages via session state
    st.session_state.regions = st.multiselect(
        "Select Regions",
        all_regions,
        default = [region for region in all_regions if region in ['Grand Est', 'Île-de-France', 'Bretagne']]

    )

    # Convert to Python native datetime.date
    all_dates = sorted(pd.to_datetime(tables["full"]['jour'].dropna().unique()))
    min_date = all_dates[0].date()
    max_date = all_dates[-1].date()

    # Sidebar slider using native date
    selected_date = st.slider(
        "Select Date",
        min_value=min_date,
        max_value=max_date,
        value=max_date,
        format="DD/MM/YYYY"
    )

    # Store in session state if needed globally
    st.session_state.selected_date = selected_date


    
# --- 3. Display Selected Page ---
page.write(df_raw, tables)