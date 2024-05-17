from typing import Union

import pandas as pd
import streamlit as st

from app_co2.buttons import (
    create_radio_buttons,
    create_table_aggregation_checkbox_gl,
    create_table_aggregation_checkbox_vu_wps,
)


def aggregate_table(
    df_filtered: pd.DataFrame,
    aggregation: dict,
    agg_cols_index: Union[list, str] = None,
    is_stacked: bool = True,
    period="year_month",
) -> pd.DataFrame:
    multi_index = get_multi_index(agg_cols_index, period=period)
    pivot_df = (
        df_filtered.groupby(
            multi_index,
            as_index=False,
        )
        .agg(aggregation)
        .reset_index(drop=True)
    )

    # Stack year_month columns
    if is_stacked:
        pivot_df = stack_pd_table(pivot_df, multi_index)

    pivot_df = pivot_df.fillna(0)
    return pivot_df


def get_multi_index(agg_cols_index: list, period="year_month") -> list:
    if agg_cols_index is not None:
        if isinstance(agg_cols_index, str):
            agg_cols_index = [agg_cols_index]
        multi_index = agg_cols_index + ["year_month"]
    else:
        multi_index = ["year_month"]

    if period == "year":
        multi_index[-1] = "year"

    return multi_index


def stack_pd_table(df: pd.DataFrame, multi_index: list) -> pd.DataFrame:
    if len(multi_index) > 1:
        df = df.set_index(multi_index).unstack(level=-1).reset_index()

        # Set new column names
        cols: list = df.columns
        df.columns = [cols[i][0] for i in range(len(multi_index) - 1)] + [
            cols[i][1] for i in range(len(multi_index) - 1, len(cols))
        ]
    else:
        df = df.transpose()
        df.columns = df.iloc[0]
        df = df[1:]
    return df


def create_budget_gl_dataframe(
    df_gl_report: pd.DataFrame, df_gl_bu: pd.DataFrame
) -> pd.DataFrame:
    grouped_cols = ["destination_country", "vehicle_type", "year_month"]
    df_gl_report = df_gl_report.copy()
    df_gl_report = (
        df_gl_report.groupby(grouped_cols)
        .agg(
            {
                "calculated_distance": "sum",
                "ton_km": "sum",
                "teu.km": "sum",
                "weight_ton": "sum",
                "co2": "sum",
            }
        )
        .reset_index()
    )
    df_budget = df_gl_report.merge(
        df_gl_bu,
        left_on=["destination_country", "year_month", "vehicle_type"],
        right_on=["country_code", "year_month", "vehicle_type"],
        how="left",
    )
    df_budget = df_budget[
        [
            "destination_country",
            "vehicle_type",
            "year_month",
            "calculated_distance",
            "BU km",
            "ton_km",
            "BU tonne.km",
            "teu.km",
            "BU TEU.km",
            "co2",
            "BU CO2",
        ]
    ]
    return df_budget


def create_st_table_gl(
    df_gl_report: pd.DataFrame, df_hl: pd.DataFrame, filters: dict
) -> pd.DataFrame:
    df_gl_report = df_gl_report.copy()
    df_hl = df_hl.copy()
    radio_button_configs = {
        "[Tonnes] CO2": {"co2": "sum"},
        "[KMs] Distance": {"calculated_distance": "sum"},
        "Tonne * KMs": {"ton_km": "sum"},
        "[KHLs] Sold": {"khl_sold": "sum"},
        "CO2 / KHL Sold": {"khl_sold": "sum"},
    }
    col1, col2 = st.beta_columns((6, 1))

    # Apply filters
    filters = {
        desired_filters: filters[desired_filters]
        for desired_filters in ["year", "month", "destination_country"]
    }

    for column, value in filters.items():
        if value:
            df_gl_report = df_gl_report[df_gl_report[column].isin(filters[column])]
            df_hl = df_hl[df_hl[column].isin(filters[column])]

    option = create_radio_buttons(col2, radio_button_configs, key="gl_table_general")

    agg = radio_button_configs[option]

    if option in ["[KMs] Distance", "[Tonnes] CO2", "Tonne * KMs"]:
        agg_cols_index = create_table_aggregation_checkbox_gl("gl_table_general", col2)
        agg_cols_index.append("year_month")
        df = df_gl_report.copy().groupby(agg_cols_index).agg(agg).reset_index()
        df = df.sort_values(by=agg_cols_index).round(decimals=2)
        df = stack_pd_table(df, agg_cols_index)
    elif option == "[KHLs] Sold":
        agg_cols_index = ["destination_country"]
        df = aggregate_table(df_hl, agg, agg_cols_index)

    elif option == "CO2 / KHL Sold":
        agg_cols_index = ["destination_country"]
        df_co2 = (
            df_gl_report.copy()
            .groupby(agg_cols_index + ["year_month"])
            .agg({"co2": "sum"})
            .reset_index()
        )
        df_co2 = stack_pd_table(df_co2, agg_cols_index + ["year_month"])
        df_khl = aggregate_table(df_hl, agg, agg_cols_index)
        df = df_co2.set_index("destination_country") / df_khl.set_index(
            "destination_country"
        )
        df = df.reset_index()

    col1.dataframe(df)
    return df


def create_st_table_gl_shipment(
    df_filtered: pd.DataFrame, co2_col: str, key: str
) -> pd.DataFrame:
    col1, col2 = st.beta_columns((6, 1))
    radio_button_configs = {
        "[Tonnes] CO2": {co2_col: "sum"},
        "[KMs] Distance": {"calculated_distance": "sum"},
        "[HLs] Transported": {"volume_hl": "sum"},
    }
    option = create_radio_buttons(col2, radio_button_configs, key=key)
    agg_cols_index = create_table_aggregation_checkbox_gl(key, col2)
    agg = radio_button_configs[option]
    df = aggregate_table(df_filtered, agg, agg_cols_index)

    col1.dataframe(df.round(decimals=2))
    return df


def create_st_table_kpi(
    df_filtered_vu_wps: pd.DataFrame, df_filtered_adt: pd.DataFrame
) -> pd.DataFrame:
    col1, col2 = st.beta_columns((6, 1))

    radio_button_configs = {
        "WPS": {"weight_ton": "sum", "kpi_weighting": "sum"},
        "VU": {"final_vu": "mean"},
        "ADT": {"calculated_distance": "sum", "kpi_weighting": "sum"},
        "Total Distance": {"calculated_distance": "sum"},
        "Number of Trips": {"kpi_weighting": "sum"},
    }

    option = create_radio_buttons(col2, radio_button_configs, key="gl_table")
    agg_cols_index = create_table_aggregation_checkbox_vu_wps(col2)
    agg = radio_button_configs[option]

    if option == "WPS":
        df = aggregate_table(df_filtered_vu_wps, agg, agg_cols_index, is_stacked=False)
        df["WPS"] = df["weight_ton"] / df["kpi_weighting"]
        df = df.drop(["weight_ton", "kpi_weighting"], axis=1)
        multi_index = get_multi_index(agg_cols_index)
        df = stack_pd_table(df, multi_index)
    elif option == "VU":
        df = aggregate_table(df_filtered_vu_wps, agg, agg_cols_index)
    elif option == "ADT":
        df = aggregate_table(df_filtered_adt, agg, agg_cols_index, is_stacked=False)
        df["ADT_KPI"] = df["calculated_distance"] / df["kpi_weighting"]
        df = df.drop(["calculated_distance", "kpi_weighting"], axis=1)
        multi_index = get_multi_index(agg_cols_index)
        df = stack_pd_table(df, multi_index)
    elif option in ["Total Distance", "Number of Trips"]:
        df = aggregate_table(df_filtered_adt, agg, agg_cols_index)
    col1.dataframe(df.round(decimals=4))
    return df


def create_actual_vs_optimum_table(
    model_vu_wps,
    model_adt,
) -> pd.DataFrame:
    df_report = pd.DataFrame()
    df_report["KPI"] = [
        "Number of trips",
        "Total Distance",
        "WPS",
        "VU",
    ]
    df_report["Data Source"] = [
        "ADT",
        "ADT",
        "WPS",
        "WPS",
    ]
    df_report["Actual"] = [
        model_adt.curr_n_trucks,
        model_adt.curr_distance,
        model_vu_wps.curr_wps,
        model_vu_wps.curr_vu,
    ]
    df_report["Optimum"] = [
        model_adt.min_n_trucks,
        model_adt.min_distance,
        model_vu_wps.max_wps,
        model_vu_wps.max_vu,
    ]

    df_report["ABI Budget"] = [
        model_adt.budget_n_trucks,
        model_adt.budget_dist,
        model_vu_wps.budget_wps,
        model_vu_wps.budget_vu,
    ]

    df_report["CO2 Actual"] = [
        model_adt.curr_co2,
        model_adt.curr_co2,
        model_vu_wps.curr_co2,
        model_vu_wps.curr_co2,
    ]

    df_report["CO2 Optimum"] = [
        model_adt.min_co2,
        model_adt.min_co2,
        model_vu_wps.min_co2,
        model_vu_wps.min_co2,
    ]
    return df_report


@st.cache(max_entries=1)
def create_overall_simulated_table(model_vu_wps, model_adt) -> pd.DataFrame:
    df_report = pd.DataFrame()
    df_report["KPI"] = [
        "Number of trips",
        "Total Distance",
        "WPS",
        "VU",
    ]

    df_report["Data Source"] = [
        "ADT",
        "ADT",
        "WPS",
        "WPS",
    ]

    df_report["Actual"] = [
        model_adt.curr_n_trucks,
        model_adt.curr_distance,
        model_vu_wps.curr_wps,
        model_vu_wps.curr_vu,
    ]

    bu_n_trucks, _, _, _, co2_n_trips = model_adt.simulate_n_trips(
        max(model_adt.budget_n_trucks, model_adt.min_n_trucks)
    )
    _, bu_wps, _, _, co2_wps = model_vu_wps.simulate_wps(model_vu_wps.budget_wps)
    _, _, bu_vu, _, co2_vu = model_vu_wps.simulate_vu(model_vu_wps.budget_vu)
    _, _, _, bu_dist, co2_dist = model_adt.simulate_dist(model_adt.budget_dist)

    df_report["Target Value"] = [bu_n_trucks, bu_dist, bu_wps, bu_vu]
    df_report["CO2 Gain"] = [
        model_adt.curr_co2 - co2_n_trips,
        model_adt.curr_co2 - co2_dist,
        model_vu_wps.curr_co2 - co2_wps,
        model_vu_wps.curr_co2 - co2_vu,
    ]
    return df_report


def create_simulation_table(n_trucks, wps, vu, dist, co2) -> pd.DataFrame:
    df_sim = pd.DataFrame()
    df_sim["KPI"] = ["Number of trips", "Total Distance", "WPS", "VU", "CO2"]
    df_sim["Simulated Values"] = [n_trucks, dist, wps, vu, co2]
    return df_sim
