import pandas as pd
import streamlit as st

from app_co2.filters import download_link


def download_gl_buttons(
    df_filtered: pd.DataFrame, df_agg: pd.DataFrame, key: str
) -> pd.DataFrame:
    left, right, _ = st.beta_columns((1, 1, 3))
    with left:
        create_download_button(
            "Download Aggregated GL", df_agg, "aggregated_gl.csv", key=key
        )
    with right:
        create_download_button("Download Raw", df_filtered, "raw_gl.csv", key=key)


def download_static_gl_buttons(
    df_agg: pd.DataFrame, df_bu: pd.DataFrame, df_hl_bu: pd.DataFrame, key: str
) -> pd.DataFrame:
    left, middle, right, _ = st.beta_columns((1, 1, 1, 2))
    with left:
        create_download_button(
            "Download Aggregated GL", df_agg, "aggregated_gl.csv", key=key
        )
    with middle:
        create_download_button(
            "Download GL Budget", df_bu, "budget_gl_actuals.csv", key=key
        )
    with right:
        create_download_button(
            "Download HL Budget", df_hl_bu, "budget_hl_actuals.csv", key=key
        )


def download_sim_results_buttons(df_sim_vu_wps, df_sim_adt):
    left, right, _ = st.beta_columns((1, 1, 3))
    scope_cols = [
        "year",
        "month",
        "day",
        "destination_city",
        "origin_city",
        "destination_country",
        "charge_code_gl",
        "vehicle_type",
        "weight_ton",
        "calculated_distance",
        "co2_abi",
        "max_allowed_weight",
        "dist",
        "wps",
        "max_wps",
        "n_trucks",
        "min_n_trucks",
        "sim_n_trucks",
        "sim_wps",
        "sim_vu",
        "sim_dist",
    ]
    col_name_map = {
        "calculated_distance": "total_distance",
        "dist": "adt",
        "weight_ton": "total_weight",
        "sim_dist": "sim_total_distance",
    }
    with left:
        df_sim_vu_wps = df_sim_vu_wps.copy()[
            df_sim_vu_wps.n_trucks != df_sim_vu_wps.sim_n_trucks
        ][scope_cols].rename(columns=col_name_map)
        create_download_button(
            "Download Sim for VU and WPS",
            df_sim_vu_wps,
            "sim_vu_wps.csv",
            key="vu_wps_simulation",
        )
    with right:
        df_sim_adt = df_sim_adt.copy()[df_sim_adt.n_trucks != df_sim_adt.sim_n_trucks][
            scope_cols
        ].rename(columns=col_name_map)
        create_download_button(
            "Download Sim for ADT", df_sim_adt, "sim_adt.csv", key="adt_simulation"
        )


def create_download_button(
    button_name: str, df: pd.DataFrame, output_file_name: str, key: str = ""
) -> None:
    is_download_gl = st.button(button_name, key=key)
    download_link(is_download_gl, df.reset_index(), output_file_name, button_name)


def create_table_aggregation_checkbox_gl(key, col) -> list:
    col.write("Select aggregation level:")
    is_dest_country = col.checkbox("Destination Country", value=True, key=key)
    is_vec_type = col.checkbox("Vehicle Type", value=True, key=key)
    is_charge_code = col.checkbox("Charge Code GL", value=True, key=key)
    agg_cols = []

    if is_dest_country:
        agg_cols.append("destination_country")
    if is_vec_type:
        agg_cols.append("vehicle_type")
    if is_charge_code:
        agg_cols.append("charge_code_gl")
    return agg_cols


def create_table_aggregation_checkbox_vu_wps(col) -> list:
    col.write("Select aggregation level:")
    is_country = col.checkbox("Country", value=True)
    is_site = col.checkbox("Site", value=True)
    is_charge_code = col.checkbox("Charge Code", value=True)
    agg_cols = []

    if is_country:
        agg_cols.append("sql_file")
    if is_site:
        agg_cols.append("site")
    if is_charge_code:
        agg_cols.append("charge_code_multidrop")
    return agg_cols


def create_radio_buttons(
    col: st.beta_columns, radio_button_configs, key: str, name: str = ""
) -> str:
    return col.radio(name, tuple(radio_button_configs.keys()), key=key)


def add_output_radio_buttons(col: st.beta_columns) -> str:
    radio_button_configs = {
        "[Tonnes] CO2": {"co2_abi": "sum"},
        "[KMs] Distance": {"calculated_distance": "sum"},
        "[HLs] Transported": {"volume_hl": "sum"},
        "[HLs] Sold": {"hl_sold": "sum"},
        "Average CO2 / HL Sold": {"co2_per_hl_sold": "mean"},
        "Average DT": {"calculated_distance": "mean"},
        "Average VU": {"final_vu": "mean"},
        "Average WPS": {"weight_ton": "mean"},
    }
    option = create_radio_buttons(
        col, radio_button_configs, key="gl_monthly_chart", name="Output Metrics"
    )
    return radio_button_configs[option], option


def add_compare_by_radio_buttons(
    col: st.beta_columns, compare_by_configs: dict, key: str
) -> str:
    option = create_radio_buttons(
        col,
        compare_by_configs,
        key=key,
        name="Compare By",
    )
    return compare_by_configs[option]


def add_stacked_radio_buttons(col: st.beta_columns, key: str) -> str:
    radio_button_stack_configs = {
        "Stacked": "relative",
        "Unstacked": "group",
    }

    option = create_radio_buttons(
        col,
        radio_button_stack_configs,
        key=key,
        name="Stack / Unstack",
    )
    return radio_button_stack_configs[option]


def add_period_radio_buttons(col: st.beta_columns, key: str) -> str:
    radio_button_period_configs = {
        "Month": "year_month",
        "Year": "year",
    }

    option = create_radio_buttons(
        col,
        radio_button_period_configs,
        key=key,
        name="Monthly / Yearly",
    )
    return radio_button_period_configs[option]


def add_radio_buttons_for_kpi_simulations(model_vu_wps, model_adt, col):
    # Individual simulations with Slider
    selected_kpi = col.radio(
        "Which KPI do you want to simulate?",
        ("Number of Trips", "Total Distance", "WPS", "VU"),
    )

    if selected_kpi == "WPS":
        sim_wps = col.number_input(
            f"WPS: value < {model_vu_wps.max_wps}",
            value=model_vu_wps.curr_wps,
            step=0.001,
        )
        n_trucks, wps, vu, dist, co2 = model_vu_wps.simulate_wps(sim_wps)

    elif selected_kpi == "VU":
        sim_vu = (
            col.number_input(
                f"VU: value < {model_vu_wps.max_vu * 100} %",
                value=model_vu_wps.curr_vu * 100,
            )
            / 100
        )
        n_trucks, wps, vu, dist, co2 = model_vu_wps.simulate_vu(sim_vu)

    elif selected_kpi == "Total Distance":
        sim_dist = col.number_input(
            f"Total distance: value > {int(model_adt.min_distance)}",
            value=model_adt.curr_distance,
        )
        n_trucks, wps, vu, dist, co2 = model_adt.simulate_dist(sim_dist)

    elif selected_kpi == "Number of Trips":
        sim_trips = col.number_input(
            f"Number of Trips: value > {model_adt.min_n_trucks}",
            value=model_adt.curr_n_trucks,
        )
        n_trucks, wps, vu, dist, co2 = model_adt.simulate_n_trips(sim_trips)
    else:
        n_trucks, wps, vu, dist, co2 = 0, 0, 0, 0, 0

    return n_trucks, wps, vu, dist, co2
