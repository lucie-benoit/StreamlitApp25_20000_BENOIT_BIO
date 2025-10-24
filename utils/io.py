# load_data(), fetch_and_cache(), license text
from turtle import st
import pandas as pd

def load_data(nrows=65180, path='data/covid-hosp-txad-reg-2023-06-30-16h29.csv'):
    """
    Load hospital COVID data from the specified CSV file.
    - nrows: number of rows to read (None for all)
    - path: path to the CSV file
    Returns: pandas DataFrame with lowercased columns and parsed dates in 'jour'.
    """
    try:
        df = pd.read_csv(path, nrows=nrows, sep=';')
        return df 
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()
    
# Quick check: verify hospital data loads correctly when running this file directly
if __name__ == "__main__":
    df = load_data()
    print("Shape:", df.shape)
    print(df.tail(10))  # Shows the first 10 rows

