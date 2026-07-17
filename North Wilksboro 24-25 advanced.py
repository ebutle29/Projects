import streamlit as st
import pandas as pd

df = pd.read_csv(r"C:\Users\evanl\OneDrive\Documents\Personal Projects\North Wilksboro Advanced Stats 2024-25.csv")

st.title("Advanced North Wilksboro Stats 2024-25")

# Map abbreviated column names to full display names (per Lap Raptor glossary)
stat_names = {
    "Start": "Starting Position",
    "Finish": "Finishing Position",
    "Finish Status": "Finish Status",
    "ARP": "Average Running Position",
    "wARP": "Weighted Average Running Position",
    "GF Laps": "Green Flag Laps",
    "SS": "Speed Score",
    "GR": "Gain Rating",
    "LR": "Loss Rating",
    "GR-LR": "Net Rating",
    "POMS": "Percent of Max Speed",
    "cPOMS": "Continuously Graded Percent of Max Speed",
    "PGAE": "Positions Gained Above Expected",
    "PFARP": "Positions Finished Above Running Position",
    "wPFARP": "Weighted Positions Finished Above Running Position",
    "1st Seg. POMS": "First Segment Percent of Max Speed",
    "Last Seg. POMS": "Last Segment Percent of Max Speed",
    "ΔPOMS": "Change in Percent of Max Speed",
    "ARS": "Average Restart Speed",
}

# Dropdown for race selection
races = sorted(df["Race"].unique().tolist())
selected_race = st.selectbox("Select a race", races)

# Filter to the selected race, then build the driver dropdown from just that race
race_df = df[df["Race"] == selected_race]
drivers = sorted(race_df["Driver"].tolist())
selected_driver = st.selectbox("Select a driver", drivers)

# Dropdown for stat/column selection, showing full names (numeric stats only)
exclude_cols = ["Race", "Driver", "Car"]
stat_columns = [col for col in race_df.columns if col not in exclude_cols]
selected_stat = st.selectbox(
    "Select a stat",
    stat_columns,
    format_func=lambda col: stat_names.get(col, col)
)

# Show the selected driver's value for the selected stat (within the selected race)
driver_row = race_df[race_df["Driver"] == selected_driver]
stat_value = driver_row[selected_stat].values[0]

st.subheader(f"{selected_driver} — {stat_names.get(selected_stat, selected_stat)} ({selected_race})")
st.metric(label=stat_names.get(selected_stat, selected_stat), value=stat_value)

# Bar chart comparing all drivers on the selected stat, sorted high to low
# Skip the chart for non-numeric columns like Finish Status
if pd.api.types.is_numeric_dtype(race_df[selected_stat]):
    st.subheader(f"All Drivers — {stat_names.get(selected_stat, selected_stat)} ({selected_race})")
    chart_data = race_df[["Driver", selected_stat]].sort_values(by=selected_stat, ascending=False)
    st.bar_chart(chart_data.set_index("Driver"))
else:
    st.info(f"'{stat_names.get(selected_stat, selected_stat)}' is not a numeric stat, so no chart is shown.")

st.subheader(f"{selected_race} — North Wilksboro Advanced Stats Data")
st.dataframe(race_df)

st.caption("Data courtesy of lapraptor.com. For personal use only.")