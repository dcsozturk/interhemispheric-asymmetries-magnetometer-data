import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(page_title="Interhemispheric Asymmetries", layout="wide")

# Title
st.title("Interhemispheric Asymmetries - Magnetometer Data Analysis")
st.markdown("Analysis of Northern vs Southern hemisphere magnetometer measurements")

# Load data
@st.cache_data
def load_data():
    # Replace with your actual data file path in the repo
    df = pd.read_csv("./data/mag_asymmetry_database.csv")
    
    # Convert time columns to datetime
    time_cols = ['dB_peak_time', 'n_peak_times', 's_peak_times', 'dJr_peak_time']
    for col in time_cols:
        df[col] = pd.to_datetime(df[col], format='%m/%d/%y %H:%M', errors='coerce')
    
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
df_filtered = df
# dB_height filter
st.sidebar.subheader("dB Height Range")
min_height = float(df['dB_height'].min())
max_height = float(df['dB_height'].max())
height_range = st.sidebar.slider(
    "Select dB_height range",
    min_height, max_height, (min_height, max_height)
)
df_filtered = df_filtered[
    (df_filtered['dB_height'] >= height_range[0]) & 
    (df_filtered['dB_height'] <= height_range[1])
]

# dt filter
st.sidebar.subheader("dt Parameter")
dt_values = sorted(df['dt'].dropna().unique())
selected_dt = st.sidebar.multiselect(
    "Select dt values (leave empty for all)",
    options=dt_values,
    default=[]
)
if selected_dt:
    df_filtered = df_filtered[df_filtered['dt'].isin(selected_dt)]

# Display filtered data info
st.sidebar.markdown(f"**Showing {len(df_filtered)} of {len(df)} records**")

# Main content
tab1 = st.tabs(["Data Table"])

with tab1:
    st.header("Filtered Data Table")
    st.dataframe(df_filtered, use_container_width=True)
    
    # Download button
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="filtered_magnetometer_data.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("**Data Source:** Interhemispheric Asymmetries - Magnetometer Data")
