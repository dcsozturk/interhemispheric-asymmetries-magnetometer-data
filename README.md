# Interhemispheric Asymmetries - Magnetometer Data Analysis

Interactive Streamlit app for analyzing interhemispheric asymmetries in magnetometer data.

## Features

- **N vs S Hemisphere Comparison**: Compare northern and southern hemisphere magnitudes and current densities
- **MLT & SME Analysis**: Explore relationships between MLT hours, SME, and dB height
- **Time Series Visualization**: Track measurements over time
- **Interactive Filters**: Filter by time range, dB height, and dt parameter
- **Data Export**: Download filtered data as CSV


### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Usage

1. **Filter your data** using the sidebar:
   - Select time range
   - Adjust dB height range
   - Choose specific dt values

2. **Explore visualizations** across 4 tabs:
   - N vs S Comparison
   - MLT & SME Analysis
   - Time Series
   - Data Table

3. **Download filtered data** from the Data Table tab

## Data Format

The app expects a CSV with these columns:
- Time columns: `dB_peak_time`, `n_peak_times`, `s_peak_times`, `dJr_peak_time`
- Measurements: `dB_height`, `n_mag`, `s_mag`, `n_Jr`, `s_Jr`
- Parameters: `sme`, `mlt_hr`, `dt`, `component`, `sites`
- Coordinates: `n_sza`, `s_sza`

Missing values are handled automatically and shown as gaps in plots.

## License

MIT
