from turtle import st
import altair as alt
import pandas as pd
from scipy.signal import find_peaks

def line_chart(df, regions, title):
    """
    Generate a line chart showing hospitalization trends for selected regions.
    
    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
        regions (list): A list of region names to display on the chart.
        title (str): The title of the chart.
    """
    #Filter the DataFrame to include only the selected regions
    df_filtered = df[df['region_name'].isin(regions)]

    #Create the Altair chart
    chart = alt.Chart(df_filtered).mark_line().encode(
        x=alt.X('jour:T', title='Date'),
        y=alt.Y('tx_indic_7J_hosp:Q', title='New Hospitalization Rate (7d)'),
        color=alt.Color('region_name:N', title='Region'),
        tooltip=[
            alt.Tooltip('jour:T', title='Date'),
            alt.Tooltip('region_name:N', title='Region'),
            alt.Tooltip('tx_indic_7J_hosp:Q', title='Hospitalization Rate (7d)')
        ]
    ).properties(
        title=title,
        width=800,
        height=500
    ).interactive()

    return chart

def bar_chart_death(df, selected_date):
    """
    Static death rate bar chart filtered by selected regions and selected date.
    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
        selected_date: selected date from the slidebar 
    """
    import altair as alt
    import pandas as pd

    df = df.copy()
    df['jour'] = pd.to_datetime(df['jour'])

    # Filter based on date only (match datetime.date from slider)
    df_filtered = df[df['jour'].dt.date == selected_date]

    # Handle no data case
    if df_filtered.empty:
        return alt.Chart(pd.DataFrame({'region_name': [], 'tx_indic_7J_DC': []})).mark_bar()

    bars = (
        alt.Chart(df_filtered)
        .mark_bar()
        .encode(
            x=alt.X('region_name:N', title='Region', sort='-y'),
            y=alt.Y('tx_indic_7J_DC:Q', title='Death Rate (7-day avg)'),
            color=alt.Color('tx_indic_7J_DC:Q', scale=alt.Scale(scheme='reds'), title='Death Rate'),
            tooltip=[
                alt.Tooltip('region_name:N', title='Region'),
                alt.Tooltip('tx_indic_7J_DC:Q', title='Death Rate', format='.2f'),
                alt.Tooltip('jour:T', title='Date')
            ]
        )
        .properties(
            width=700,
            height=400,
            title=f"Death Rate by Selected Regions on {selected_date.strftime('%d %b %Y')}"
        )
    )

    return bars



def ranked_bar_chart(df):
    """
    Generate an interactive ranked bar chart of regions by mean hospitalization rate,
    filterable by month and year.
    
    Args:
        df (pd.DataFrame): The input DataFrame containing the data. 
    """
    
    # Fix and Data Preparation 
    df_copy = df.copy() 
    df_copy['date'] = pd.to_datetime(df_copy['jour'])
    df_copy['year'] = df_copy['date'].dt.year
    df_copy['month'] = df_copy['date'].dt.month

    # Aggregate Data
    df_agg = df_copy.groupby(['region_name', 'year', 'month'])['tx_indic_7J_hosp'].mean().reset_index()

    # Create Selections of Month and Year
    
    available_years = sorted(df_agg['year'].unique())
    available_months = sorted(df_agg['month'].unique())
    
    month_map = {
        1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril', 5: 'Mai', 6: 'Juin',
        7: 'Juillet', 8: 'Août', 9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
    }
    df_agg['month_name'] = df_agg['month'].map(month_map)
    month_dropdown_options = [month_map[m] for m in available_months]

    max_date = df_copy['date'].max()
    default_year =  2020
    default_month_name = month_map[3]

    
    year_param = alt.param(
        name="year_selection",  
        value=default_year,     
        bind=alt.binding_select(options=available_years, name='Year: ')
    )

    month_param = alt.param(
        name="month_selection",
        value=default_month_name, 
        bind=alt.binding_select(options=month_dropdown_options, name='Month: ')
    )


    # Create the Ranked Bar Chart
    chart = (
        alt.Chart(df_agg)
        .mark_bar()
        .encode(
            x=alt.X('tx_indic_7J_hosp:Q', title="Hospitalization rate (mean 7d)"),
            y=alt.Y('region_name:N', title='Region', sort='-x'),
            color=alt.Color('tx_indic_7J_hosp:Q', scale=alt.Scale(scheme='reds'), title='Mean rate'),
            tooltip=[
                alt.Tooltip('region_name:N', title='Region'),
                alt.Tooltip('year:O', title='Year'),
                alt.Tooltip('month_name:N', title='Mois'),
                alt.Tooltip('tx_indic_7J_hosp:Q', title='Mean rate', format='.2f')
            ]
        )
        
        .add_params(year_param, month_param) 
        
        .transform_filter(
            (alt.datum.year == year_param) & 
            (alt.datum.month_name == month_param)
        )
        
        .properties(
            title="Ranked mean hospitalization rates by region (per month/year)"
        )
        .interactive()
    )

    return chart

def map_chart(df): 
    """ Generate a map chart visualizing hospitalization rates geographically. 
    Args: df (pd.DataFrame): The input DataFrame containing the data. """ 

    # URL to a GeoJSON file with French region boundaries 
    url_regions = 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson' 
    
    # Load the GeoJSON data 
    regions_geo = alt.Data(url=url_regions, format=alt.DataFormat(property='features')) 
    
    # Calculate the mean hospitalization rate per region 
    # We use the mean to have a single value for each region on the map
    mean_hospitalization_rate_by_region = df.groupby('region_name')['tx_indic_7J_hosp'].mean().reset_index()
    
    # Create the map chart
    chart = alt.Chart(regions_geo).mark_geoshape(
        stroke='white'
    ).encode(
        color=alt.Color('tx_indic_7J_hosp:Q', title='Mean Hospitalization Rate', scale=alt.Scale(scheme='reds')),
        tooltip=[
            alt.Tooltip('properties.nom:N', title='Region'),
            alt.Tooltip('tx_indic_7J_hosp:Q', title='Mean Rate', format='.2f')
        ]
    ).transform_lookup(
        lookup='properties.nom',
        from_=alt.LookupData(data=mean_hospitalization_rate_by_region, key='region_name', fields=['tx_indic_7J_hosp'])
    ).properties(
        title='Mean Hospitalization Rate by Region 03/2020 - 06/2023'
    ).project(
        type='mercator'
    ).properties(
        width=700,
        height=500
    )

    return chart

def map_chart2(df): 
    """ Generate a map chart visualizing death rates geographically. 
    Args: df (pd.DataFrame): The input DataFrame containing the data. """ 

    # URL to a GeoJSON file with French region boundaries 
    url_regions = 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson' 
    
    # Load the GeoJSON data 
    regions_geo = alt.Data(url=url_regions, format=alt.DataFormat(property='features')) 
    
    # Calculate the mean hospitalization rate per region 
    # We use the mean to have a single value for each region on the map
    mean_hospitalization_rate_by_region = df.groupby('region_name')['tx_indic_7J_DC'].mean().reset_index()
    
    # Create the map chart
    chart = alt.Chart(regions_geo).mark_geoshape(
        stroke='white'
    ).encode(
        color=alt.Color('tx_indic_7J_DC:Q', title='Mean Death Rate', scale=alt.Scale(scheme='reds')),
        tooltip=[
            alt.Tooltip('properties.nom:N', title='Region'),
            alt.Tooltip('tx_indic_7J_DC:Q', title='Mean Rate', format='.2f')
        ]
    ).transform_lookup(
        lookup='properties.nom',
        from_=alt.LookupData(data=mean_hospitalization_rate_by_region, key='region_name', fields=['tx_indic_7J_DC'])
    ).properties(
        title='Mean Death Rate by Region 03/2020 - 06/2023'
    ).project(
        type='mercator'
    ).properties(
        width=600,
        height=500
    )

    return chart

def combo_chart(df, region):
    """
    Generate a combined line chart showing hospitalization and critical care rates 
    over time for a single region.
    
    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
        region (str): The name of the region to display.
    """
    import altair as alt

    # Filter the DataFrame for the selected region
    df_region = df[df['region_name'] == region]

    # Define a mapping from column names to display names
    indicator_mapping = {
        "tx_indic_7J_hosp": "Hospitalizations",
        "tx_indic_7J_SC": "Critical care"
    }

    # Define the color scale (must match display names)
    color_scale = alt.Scale(
        domain=list(indicator_mapping.values()),
        range=["#2326ce", "#cb8f28"]  # Blue and Orange
    )

    # Create the combo chart
    chart = (
        alt.Chart(df_region)
        .transform_fold(
            list(indicator_mapping.keys()),
            as_=["Indicator", "Value"]
        )
        # Replace indicator codes with readable names
        .transform_calculate(
            Indicator=(
                "datum.Indicator == 'tx_indic_7J_hosp' ? 'Hospitalizations' : "
                "datum.Indicator == 'tx_indic_7J_SC' ? 'Critical care' : datum.Indicator"
            )
        )
        .mark_line()
        .encode(
            x=alt.X("jour:T", title="Date"),
            y=alt.Y("Value:Q", title="Rate (per 100k)"),
            color=alt.Color("Indicator:N", scale=color_scale, title="Indicator"),
            tooltip=["jour:T", "Indicator:N", alt.Tooltip("Value:Q", format=".2f")]
        )
        .properties(
            title=f"Evolution of Hospitalizations vs Critical Care — {region}",
            width=700,
            height=400
        )
        .interactive()
    )

    return chart

def waves(df):
    """
    Computes a smoothed national hospitalization rate, detects peaks and waves, produces a table of peaks, 
    and plots the chart.    
    Args:
        df (pd.DataFrame): The input DataFrame containing the data."""

    # Aggregate daily hospitalization rates to national mean
    df_national = df.groupby('jour')['tx_indic_7J_hosp'].mean().reset_index()
    df_national.rename(columns={'tx_indic_7J_hosp': 'tx_moyen_national_hosp_7j'}, inplace=True)
    df_national = df_national.sort_values(by='jour')

    # Smooth the national mean series using rolling window
    df_national['tx_lisse'] = df_national['tx_moyen_national_hosp_7j'].rolling(window=7, center=True, min_periods=1).mean()

    # Detect peaks corresponding to epidemic waves
    peaks, _ = find_peaks(df_national['tx_lisse'], prominence=0.5, distance=60)

    # Create a table of detected waves
    df_waves = df_national.iloc[peaks][['jour', 'tx_lisse']].copy()
    df_waves.rename(columns={'jour': 'Date_of_peak', 'tx_lisse': 'Value_of_peak_Smoothed_Average_Rate'}, inplace=True)
    df_waves['Waves'] = [f"Wave {i+1}" for i in range(len(df_waves))]
    df_waves['Date_of_peak'] = pd.to_datetime(df_waves['Date_of_peak'])
    
    # Prepare peaks DataFrame for plotting
    df_peaks = df_national.iloc[peaks].copy()
    df_peaks['Waves'] = [f"Wave {i+1}" for i in range(len(peaks))]

    # Altair plot 
    base = alt.Chart(df_national).encode(
        x=alt.X('jour:T', title='Date')
    )

    # Add a raw national mean line (red, semi-transparent)
    raw_line = base.mark_line(opacity=0.5, color='red').encode(
        y=alt.Y('tx_moyen_national_hosp_7j:Q', title='Mean hospitalization rate (7d)'),
        tooltip=[
            alt.Tooltip('jour:T', title='Date'),
            alt.Tooltip('tx_moyen_national_hosp_7j:Q', title='Mean Rate (7d)')
        ]
    )

    # Line for smoothed rate
    smooth_line = base.mark_line(color='blue').encode(
        y='tx_lisse:Q',
        tooltip=[
            alt.Tooltip('jour:T', title='Date'),
            alt.Tooltip('tx_lisse:Q', title='Smoothed Rate')
        ]
    )

    # Points for peaks in red
    peak_points = alt.Chart(df_peaks).mark_point(filled=True, size=100, color='red').encode(
        x='jour:T',
        y='tx_lisse:Q',
        tooltip=[
            alt.Tooltip('Waves', title='Wave'),
            alt.Tooltip('jour:T', title='Peak Date'),
            alt.Tooltip('tx_lisse:Q', title='Peak Value')
        ]
    )

    # Text labels for peaks
    text_labels = alt.Chart(df_peaks).mark_text(
        align='center',
        dy=-15,
        fontSize=10
    ).encode(
        x='jour:T',
        y='tx_lisse:Q',
        text='Waves'
    )

    # Combine all layers
    chart = (raw_line + smooth_line + peak_points + text_labels).properties(
        title="National epidemic waves in France (based on the Mean National Hospitalization Rate)",
        width=800,
        height=500
    ).interactive()

    return df_waves, chart

def death_rate_during_peaks(df):
    """
    Generate a line chart showing the variation of death rates during peak hospitalization periods using the peaks table from the waves function.   
    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
    """
    # Get the waves data from waves function 
    df_waves, _ = waves(df)

    # Prepare the main DataFrame
    df_copy = df.copy()
    df_copy['date'] = pd.to_datetime(df_copy['jour'])
    df_copy = df_copy.sort_values(by='date')

    # Create the Altair chart
    chart = alt.Chart(df_copy).mark_line().encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('tx_indic_7J_DC:Q', title='Death Rate (7d)'),
        tooltip=['date:T', 'tx_indic_7J_DC:Q']
    ).properties(
        title='Death Rate Variation During Peak Hospitalization Periods'
    ).interactive()

    # Add red lines for each peak and annotate with wave information
    for _, row in df_waves.iterrows():
        peak_date = pd.to_datetime(row['Date_of_peak'])
        wave_label = row['Waves']

        # Vertical line
        vline = alt.Chart(pd.DataFrame({'date': [peak_date]})).mark_rule(color='red', strokeDash=[4, 4]).encode(
            x='date:T'
        )

        # Text annotation
        text = alt.Chart(pd.DataFrame({'date': [peak_date], 'label': [wave_label]})).mark_text(
            align='left',
            baseline='bottom',
            dy=-10,
            color='red'
        ).encode(
            x='date:T',
            text='label:N'
        )

        chart += vline + text

    return chart

def hospitalization_growth_rate_chart(df, regions):
    """
    Generate a line chart showing the hospitalization growth rate trends for selected regions,
    with a horizontal red line at 0 to highlight positive vs negative growth.
    
    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
        regions (list): A list of region names to display on the chart.
    """
    # Filter the DataFrame to include only the selected regions
    df_filtered = df[df['region_name'].isin(regions)]

    # Base line chart for growth rates
    growth_line = alt.Chart(df_filtered).mark_line().encode(
        x=alt.X('jour:T', title='Date'),
        y=alt.Y('hosp_growth_rate:Q', title='Hospitalization Growth Rate'),
        color=alt.Color('region_name:N', title='Region'),
        tooltip=[
            alt.Tooltip('jour:T', title='Date'),
            alt.Tooltip('region_name:N', title='Region'),
            alt.Tooltip('hosp_growth_rate:Q', title='Growth Rate', format='.4f')
        ]
    )

    # Dotted horizontal line at y=0
    zero_line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(
        color='red',
        strokeWidth=2,
        strokeDash=[5, 5]  # dotted pattern: 5px dash, 5px gap
    ).encode(
        y='y:Q'
    )

    # Combine layers
    chart = (growth_line + zero_line).properties(
        title='Hospitalization Growth Rate Trends by Region',
        width=800,
        height=500
    ).interactive()

    return chart
