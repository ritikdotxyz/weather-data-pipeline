from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Weather Analytics",
)


@st.cache_resource
def get_connection():
    return duckdb.connect("weather_data.duckdb", read_only=True)


con = get_connection()


@st.cache_data(ttl=300)
def load_data():
    daily = con.execute("""
        SELECT *
        FROM prod.fct_daily_weather
    """).df()

    monthly = con.execute("""
        SELECT *
        FROM prod.fct_monthly_weather
    """).df()

    stations = con.execute("""
        SELECT * 
        FROM prod.dim_stations
    """).df()

    return daily, monthly, stations


def sidebar():
    with st.sidebar:
        st.title("Weather Data Analytics")

        page = st.radio(
            "Navigation",
            ["Daily", "Monthly", "Station"],
            label_visibility="collapsed",
        )

    return page


def daily_dashboard(daily):
    st.title("Daily Weather Dashboard")

    if daily.empty:
        st.warning("No daily weather records available.")
        return

    daily = daily.copy()
    daily["date"] = pd.to_datetime(daily["date"], errors="coerce")
    daily = daily.dropna(subset=["date"])

    st.subheader("1. Temperature Observation Distribution")

    col1, col2 = st.columns(2)

    with col1:
        if "has_temperature_observations" in daily.columns:
            distribution = (
                daily["has_temperature_observations"]
                .fillna(False)
                .map({True: "Has Temperature", False: "No Temperature"})
                .value_counts()
                .rename_axis("Observation")
                .reset_index(name="Records")
            )

            fig = px.pie(
                distribution,
                names="Observation",
                values="Records",
                title="Temperature Observation Distribution (All Years)",
                hole=0.4,
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        total_records = len(daily)

        st.metric("Total Daily Records", f"{total_records:,}")

        if "has_temperature_observations" in daily.columns:
            temperature_records = (
                daily["has_temperature_observations"].fillna(False).sum()
            )
            st.metric("Records With Temperature", f"{temperature_records:,}")

    st.subheader("2. Temperature Analysis")

    if "mean_temperature" in daily.columns:
        temp = daily.dropna(subset=["mean_temperature"])

        if not temp.empty:
            fig = px.line(
                temp,
                x="date",
                y="mean_temperature",
                title="Mean Temperature Over All Years",
                labels={
                    "date": "Date",
                    "mean_temperature": "Mean Temperature",
                },
            )
            st.plotly_chart(fig, use_container_width=True)


def monthly_dashboard(monthly):
    st.title("Monthly Weather Dashboard")

    if monthly.empty:
        st.warning("No monthly weather records available.")
        return

    monthly = monthly.copy()
    monthly["observation_month"] = pd.to_datetime(
        monthly["observation_month"], errors="coerce"
    )
    monthly = monthly.dropna(subset=["observation_month"])

    st.subheader("1. Weather Observation Distribution")

    col1, col2 = st.columns(2)

    with col1:
        if "daily_records" in monthly.columns:
            distribution = (
                monthly.groupby(monthly["observation_month"].dt.year)[
                    "daily_records"
                ]
                .sum()
                .reset_index()
            )
            distribution.columns = ["Year", "Records"]

            fig = px.pie(
                distribution,
                names="Year",
                values="Records",
                title="Distribution of Daily Records by Year",
                hole=0.4,
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.metric("Station-Month Records", f"{len(monthly):,}")

        if "avg_mean_temperature" in monthly.columns:
            st.metric(
                "Overall Average Temperature",
                f"{monthly['avg_mean_temperature'].mean():.2f}",
            )
    st.subheader("2. Monthly Temperature Analysis")

    if "avg_mean_temperature" in monthly.columns:
        temp = monthly.dropna(subset=["avg_mean_temperature"])

        if not temp.empty:
            fig = px.line(
                temp,
                x="observation_month",
                y="avg_mean_temperature",
                title="Average Monthly Temperature Over All Years",
                labels={
                    "observation_month": "Month",
                    "avg_mean_temperature": "Average Temperature",
                },
            )
            st.plotly_chart(fig, use_container_width=True)


def stations_dashboard(stations):
    st.title("Weather Stations")

    if stations.empty:
        st.warning("No station records are available.")
        return

    stations = stations.copy()

    c1, c2 = st.columns(2)
    c1.metric(
        "Total Stations",
        f"{stations['station_id'].nunique():,}",
    )

    stations_with_coordinates = (
        stations[["latitude", "longitude"]].notna().all(axis=1).sum()
    )

    c2.metric(
        "Stations with Coordinates",
        f"{stations_with_coordinates:,}",
    )

    st.subheader("Weather Station Locations")
    map_data = stations.dropna(subset=["latitude", "longitude"])

    if not map_data.empty:
        st.map(
            map_data,
            latitude="latitude",
            longitude="longitude",
        )
    else:
        st.info("No valid station coordinates are available.")

    with st.expander("View station records"):
        st.dataframe(stations, use_container_width=True, hide_index=True)


def main():
    selected_page = sidebar()

    try:
        daily, monthly, stations = load_data()
    except Exception as exc:
        st.error("Could not load the dbt models. ")
        st.exception(exc)
        st.stop()

    if selected_page == "Daily":
        daily_dashboard(daily)
    elif selected_page == "Monthly":
        monthly_dashboard(monthly)
    elif selected_page == "Station":
        stations_dashboard(stations)


if __name__ == "__main__":
    main()
