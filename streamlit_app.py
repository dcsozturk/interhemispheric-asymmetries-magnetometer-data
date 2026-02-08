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
tab1, tab2, tab3 = st.tabs(["N vs S Comparison", "MLT & SME Analysis", "Data Table"])

with tab1:
    st.header("Northern vs Southern Hemisphere Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # N vs S magnitude comparison
        fig1 = px.scatter(
            df_filtered.dropna(subset=['n_mag', 's_mag']),
            x='n_mag', y='s_mag',
            color='sme',
            title='Northern vs Southern Magnitude',
            labels={'n_mag': 'Northern Magnitude', 's_mag': 'Southern Magnitude'},
            hover_data=['dB_peak_time', 'dB_height', 'dt']
        )
        fig1.add_trace(go.Scatter(
            x=[df_filtered['n_mag'].min(), df_filtered['n_mag'].max()],
            y=[df_filtered['n_mag'].min(), df_filtered['n_mag'].max()],
            mode='lines',
            name='1:1 line',
            line=dict(dash='dash', color='gray')
        ))
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # N vs S current density comparison
        fig2 = px.scatter(
            df_filtered.dropna(subset=['n_Jr', 's_Jr']),
            x='n_Jr', y='s_Jr',
            color='sme',
            title='Northern vs Southern Current Density (Jr)',
            labels={'n_Jr': 'Northern Jr', 's_Jr': 'Southern Jr'},
            hover_data=['dB_peak_time', 'dB_height', 'dt']
        )
        fig2.add_trace(go.Scatter(
            x=[df_filtered['n_Jr'].min(), df_filtered['n_Jr'].max()],
            y=[df_filtered['n_Jr'].min(), df_filtered['n_Jr'].max()],
            mode='lines',
            name='1:1 line',
            line=dict(dash='dash', color='gray')
        ))
        st.plotly_chart(fig2, use_container_width=True)
    
    # Asymmetry metrics
    st.subheader("Asymmetry Metrics")
    col3, col4 = st.columns(2)
    
    with col3:
        df_filtered['mag_asymmetry'] = df_filtered['n_mag'] - df_filtered['s_mag']
        fig3 = px.histogram(
            df_filtered.dropna(subset=['mag_asymmetry']),
            x='mag_asymmetry',
            title='Magnitude Asymmetry Distribution (N - S)',
            labels={'mag_asymmetry': 'Magnitude Asymmetry'}
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        df_filtered['Jr_asymmetry'] = df_filtered['n_Jr'] - df_filtered['s_Jr']
        fig4 = px.histogram(
            df_filtered.dropna(subset=['Jr_asymmetry']),
            x='Jr_asymmetry',
            title='Current Density Asymmetry Distribution (N - S)',
            labels={'Jr_asymmetry': 'Jr Asymmetry'}
        )
        st.plotly_chart(fig4, use_container_width=True)

with tab2:
    st.header("MLT and SME Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # MLT_hr analysis
        fig5 = px.scatter(
            df_filtered.dropna(subset=['mlt_hr', 'dB_height']),
            x='mlt_hr', y='dB_height',
            color='sme',
            title='dB Height vs MLT Hour',
            labels={'mlt_hr': 'MLT Hour', 'dB_height': 'dB Height'},
            hover_data=['dB_peak_time', 'n_mag', 's_mag']
        )
        st.plotly_chart(fig5, use_container_width=True)
        
        # MLT distribution
        fig7 = px.histogram(
            df_filtered.dropna(subset=['mlt_hr']),
            x='mlt_hr',
            nbins=24,
            title='MLT Hour Distribution',
            labels={'mlt_hr': 'MLT Hour'}
        )
        st.plotly_chart(fig7, use_container_width=True)
    
    with col2:
        # SME analysis
        fig6 = px.scatter(
            df_filtered.dropna(subset=['sme', 'dB_height']),
            x='sme', y='dB_height',
            color='mlt_hr',
            title='dB Height vs SME',
            labels={'sme': 'SME', 'dB_height': 'dB Height'},
            hover_data=['dB_peak_time', 'n_mag', 's_mag']
        )
        st.plotly_chart(fig6, use_container_width=True)
        
        # SME distribution
        fig8 = px.histogram(
            df_filtered.dropna(subset=['sme']),
            x='sme',
            title='SME Distribution',
            labels={'sme': 'SME'}
        )
        st.plotly_chart(fig8, use_container_width=True)

with tab3:
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
