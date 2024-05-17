import base64
from datetime import datetime

import pandas as pd
import streamlit as st

time_filters = {"year": "years", "month": "months"}


geo_filters = {
    "origin_country": "origin countries",
    "destination_country": "destination countries",
    "origin_city": "origin cities",
    "destination_city": "destination cities",
    "plant": "plants",
    "destination_loc_id": "destination ids",
    "site": "sites",
}

transport_filters = {
    "carrier_name": "carriers",
    "vehicle_type": "vehicle types",
    "charge_code_gl": "charge codes",
}

all_filters = {**time_filters, **transport_filters, **geo_filters}


def filter_df(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    df_filtered = df.copy()
    for column, value in filters.items():
        if value:
            df_filtered = df_filtered[df[column].isin(filters[column])]
    return df_filtered


def download_link(is_download: bool, df: pd.DataFrame, f_name: str, button_text: str):
    if is_download:
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(
            csv.encode()
        ).decode()  # some strings <-> bytes conversions necessary here
        link = f'<a href="data:file/csv;base64,{b64}" download="{f_name}">{button_text}</a>'
        return st.markdown(link, unsafe_allow_html=True)
    return None


def aggregate_co2(df_filtered: pd.DataFrame) -> pd.Series:
    return df_filtered.groupby("month").sum()[["co2_abi"]]


def add_filters(df: pd.DataFrame):
    filters = {}
    initial_options = {column: df[column].unique() for column in all_filters.keys()}
    now = datetime.now()
    st.sidebar.subheader("Time Filters")
    for column in time_filters.keys():
        if column == "year":
            default_value = now.year
        elif column == "month":
            default_value = max(1, now.month - 1)
        else:
            default_value = None

        filters[column] = st.sidebar.multiselect(
            "Select {}:".format(time_filters[column]),
            options=sorted(initial_options[column]),
            default=default_value,
        )

    st.sidebar.subheader("Geo Filters")
    for column in geo_filters.keys():
        filters[column] = st.sidebar.multiselect(
            "Select {}:".format(geo_filters[column]), options=initial_options[column]
        )

    st.sidebar.subheader("Transport Filters")
    for column in transport_filters.keys():
        filters[column] = st.sidebar.multiselect(
            "Select {}:".format(transport_filters[column]),
            options=initial_options[column],
        )
    return filters
