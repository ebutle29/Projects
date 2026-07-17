import streamlit as st
import pandas as pd

df = pd.read_csv(r"C:\Users\evanl\OneDrive\Documents\Personal Projects\advanced short track stats 2026.csv")

st.title("Advanced Short Track Stats 2026")

# Map abbreviated column names to full display names (per Lap Raptor glossary)
stat_names = {
    "Age": "Age",
    "Starts": "Starts",
    "Wins": "Wins",
    "Points": "Points",
    "GF Laps": "Green Flag Laps",
    "ASP": "Average Starting Position",
    "ARP": "Average Running Position",
    "wARP": "Weighted Average Running Position",
    "AFP": "Average Finish Position",
    "PFAE": "Positions Finished Above Expected",
    "Avg. PFAE": "Average Positions Finished Above Expected",
    "Succ%": "Success Rate",
    "PGAE": "Positions Gained Above Expected",
    "PGAE/100": "Positions Gained Above Expected per 100 Green Flag Laps",
    "PFARP": "Positions Finished Above Running Position",
    "wPFARP": "Weighted Positions Finished Above Running Position",
    "cPOMS": "Continuously Graded Percent of Max Speed",
    "GR": "Gain Rating",
    "LR": "Loss Rating",
    "GR-LR": "Net Rating",
    "SS": "Speed Score",
    "1st Seg. POMS": "First Segment Percent of Max Speed",
    "Last Seg. POMS": "Last Segment Percent of Max Speed",
    "ΔPOMS": "Change in Percent of Max Speed",
}

# Dropdown for driver selection, alphabetical order
drivers = sorted(df["Driver"].tolist())
selected_driver = st.selectbox("Select a driver", drivers)

# Dropdown for stat/column selection, showing full names
stat_columns = [col for col in df.columns if col not in ["Driver", "Car"]]
selected_stat = st.selectbox(
    "Select a stat",
    stat_columns,
    format_func=lambda col: stat_names.get(col, col)
)

# Show the selected driver's value for the selected stat
driver_row = df[df["Driver"] == selected_driver]
stat_value = driver_row[selected_stat].values[0]

st.subheader(f"{selected_driver} — {stat_names.get(selected_stat, selected_stat)}")
st.metric(label=stat_names.get(selected_stat, selected_stat), value=stat_value)

# Bar chart comparing all drivers on the selected stat, sorted high to low
st.subheader(f"All Drivers — {stat_names.get(selected_stat, selected_stat)}")
chart_data = df[["Driver", selected_stat]].sort_values(by=selected_stat, ascending=False)
st.bar_chart(chart_data.set_index("Driver"))

st.subheader("2026 Short Track Stats Data")
st.dataframe(df)

st.caption("Data courtesy of lapraptor.com For personal use only.")