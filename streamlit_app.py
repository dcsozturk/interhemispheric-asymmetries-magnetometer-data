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
st.markdown("Accompanying data set for: A Comparative Study of Ground Magnetic Variability Between High-Latitude Conjugate Chains to Characterize Interhemispheric Asymmetry During Geomagnetic Activity")
st.markdown("Authors: Gabrielle M. Nowak (University of Alaska Fairbanks) (corr-auth), Dogacan S. Ozturk (University of Alaska Fairbanks), Zhonghua Xu (The University of Texas at Arlington), Hyomin Kim (New Jersey Institute of Technology), Mark J. Engebretson (Department of Physics, Augsburg University), Anna Willer (Technical University of Denmark) ")
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
st.markdown("Since 2008, the PG array—deployed as Autonomous Adaptive Low-Power Instrument ")
st.markdown("Platforms (AAL-PIPs)—has served as the foundation for several NSF-funded efforts")
st.markdown("(e.g., NSF PLR-0839858, 1243398, 1543364, 1744828, 1744861, 1745041, NSF MRI-0922979,")
st.markdown("NSFGEO–NERC-2027168, 2027190, 2027210), focused on SWMI-G coupling and hemispheric comparison.")
st.markdown("These stations have demonstrated exceptional durability in harsh polar conditions, with minimal")
st.markdown("logistical overhead. One site (PG1) has been in continuous operation and returning data for 17 years")
st.markdown("with no maintenance visits (PG1 deployment in January 2008). Each PG node includes")
st.markdown("a 1-Hz fluxgate magnetometer, and select sites are equipped with 10-Hz induction magnetometers and ")
st.markdown("dual-frequency GPS receivers to support TEC and scintillation measurements.")
