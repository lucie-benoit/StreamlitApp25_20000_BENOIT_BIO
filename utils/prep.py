# cleaning, normalization, feature engineerin
import streamlit as st
import pandas as pd 

@st.cache_data
def get_filtered_data(df, regions, selected_date):
    filtered_df = df[df['region_name'].isin(regions)].copy()
    filtered_df['jour'] = pd.to_datetime(filtered_df['jour'])
    date_filtered_df = filtered_df[filtered_df['jour'].dt.date == selected_date]

    if date_filtered_df.empty:
        # fallback to latest available per region
        latest_data = filtered_df.loc[filtered_df.groupby('region_name')['jour'].idxmax()]
    else:
        latest_data = date_filtered_df

    return filtered_df, latest_data

def show_data_quality(df):
    missing = (df.isnull() | (df == '')).sum()
    missing = missing[missing > 0]

    if not missing.empty:
        st.warning("⚠️Some columns contain missing or empty values:")
        st.dataframe(missing.to_frame("Missing Count"))
    else:
        st.success("No missing or empty values.")

    dup_count = df.duplicated().sum()
    if dup_count > 0:
        st.warning(f"⚠️ {dup_count} duplicate rows found.")
    else:
        st.success("No duplicate rows.")

def cleaning(df):
    """
    Clean the DataFrame by removing duplicates and missing values.
    """
    print('Missing values remaining:', df.isnull().sum().sum())
    print('Duplicate rows remaining:', df.duplicated().sum())
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Remove rows with missing values
    df = df.dropna()
    
    # Convert date column to datetime format
    df['jour'] = pd.to_datetime(df['jour'], format='%Y-%m-%d')
    
    # Verify no missing values and no duplicates remain
    print('Missing values remaining:', df.isnull().sum().sum())
    print('Duplicate rows remaining:', df.duplicated().sum())
    return df

def validate_data(df):
    # Check numeric columns
    assert df['tx_indic_7J_hosp'].min() >= 0, "Hospitalization column has negative numbers!"

    # Check date column
    assert df['jour'].notnull().all(), "Missing dates found!"

    # Check categories
    valid_categories = ['A', 'B', 'C']
    if 'category' in df.columns:
        if not df['category'].isin(valid_categories).all():
            st.warning("Unknown categories found in data")
    
    return df


def exploration(df):
	print(df.info())
	print(df.describe())

#no normalization needed for this dataset 
#because rates are already standardized (per 100,000 inhabitants)

def feature_engineering(df):
    # create a new column to add region names to the region codes
    
    region_names = {
        1 : 'Guadeloupe',
        2: 'Martinique',
        3: 'Guyane',
        4: 'La Réunion',
        6: 'Mayotte',
        11: 'Île-de-France',
        24: 'Centre-Val de Loire',
        27: 'Bourgogne-Franche-Comté',
        28: 'Normandie',
        32: 'Hauts-de-France',
        44: 'Grand Est',
        52: 'Pays de la Loire',
        53: 'Bretagne',
        75: 'Nouvelle-Aquitaine',
        76: 'Occitanie',
        84: 'Auvergne-Rhône-Alpes',
        93: 'Provence-Alpes-Côte d\'Azur',
        94: 'Corse'
    }
    # Ensure region codes are int for mapping
    df['reg'] = df['reg'].astype(int)
    df['region_name'] = df['reg'].map(region_names)

    # Create a new column to calculate the growth rate of hospitalizations per week
    # Use groupby to avoid cross-region calculation if needed
    # Ensure 'jour' is a datetime column
    df['jour'] = pd.to_datetime(df['jour'])

    # Sort the DataFrame by region and date (important for accurate pct_change)
    df = df.sort_values(['reg', 'jour'])

    # Calculate the weekly growth rate of hospitalization rate (7-day difference)
    df['hosp_growth_rate'] = df.groupby('reg')['tx_indic_7J_hosp'].pct_change(periods=7)

    # Replace infinite values with NA (occurs when previous value is zero)
    df['hosp_growth_rate'] = df['hosp_growth_rate'].replace([float('inf'), -float('inf')], pd.NA)


    return df

def make_tables(df):
    """
    Prepare cleaned DataFrame and aggregated tables for the dashboard:
    - full: cleaned & feature-engineered df
    - timeseries: hospitalization per day
    - by_region: hospitalization per region
    """
    # Step 1: Clean and feature engineer
    df_clean = cleaning(df)
    df_feature = feature_engineering(df_clean)
    df_validate = validate_data(df_feature)

    # Timeseries table
    timeseries = df_validate.groupby('jour')['tx_indic_7J_hosp'].sum().reset_index()

    # By region table
    by_region = df_validate.groupby('region_name')['tx_indic_7J_hosp'].sum().reset_index()

    # Return dictionary
    return {
        "full": df_validate,
        "timeseries": timeseries,
        "by_region": by_region
    }

