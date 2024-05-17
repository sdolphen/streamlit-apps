import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from app_co2.buttons import (
    add_compare_by_radio_buttons,
    add_period_radio_buttons,
    add_stacked_radio_buttons,
)
from app_co2.tables import aggregate_table


def single_bar_chart_gl(df_filtered_kpi):
    if len(df_filtered_kpi.columns) == 2:
        x, y = df_filtered_kpi.columns
        color = None
    elif len(df_filtered_kpi.columns) == 3:
        color, x, y = df_filtered_kpi.columns
    else:
        raise ValueError

    fig_temp = px.bar(
        df_filtered_kpi,
        x=x,
        y=y,
        color=color,
        height=500,
        width=500,
    )

    fig_temp.update_xaxes(
        type="category",
        tickangle=45,
    )
    fig_temp.update_yaxes(nticks=25)
    fig_temp.update_layout(showlegend=False)
    return fig_temp


def gl_actual_bar_chart(df_filtered_gl):
    col1, col2 = st.beta_columns((6, 1))
    compare_by_configs = {
        "No Comparison": None,
        "Destination Countries": "destination_country",
        "Modalities": "vehicle_type",
    }
    compare_by = add_compare_by_radio_buttons(
        col2, compare_by_configs, "gl_compare_by_chart"
    )
    stacked = add_stacked_radio_buttons(col2, "gl_compare_stacked")
    period = add_period_radio_buttons(col2, "gl_period")
    kpis = {
        "[Tonnes] CO2": {"co2_abi": "sum"},
        "[KMs] Distance": {"calculated_distance": "sum"},
        "[HLs] Transported": {"volume_hl": "sum"},
    }
    fig = go.Figure(layout=go.Layout(height=600, width=1000))
    fig = make_subplots(
        rows=1,
        cols=3,
        start_cell="top-left",
        figure=fig,
        subplot_titles=tuple(kpis.keys()),
    )
    col = 1

    for kpi, agg in kpis.items():
        df_filtered_kpi = (
            aggregate_table(
                df_filtered_gl,
                agg,
                agg_cols_index=compare_by,
                is_stacked=False,
                period=period,
            )
            .reset_index(drop=True)
            .copy()
        )
        fig_single = single_bar_chart_gl(df_filtered_kpi)
        fig.add_traces(fig_single.data, 1, col)
        col = (col % 3) + 1
        fig.update_traces(showlegend=False)
        fig.update_traces(showlegend=True, row=1, col=1)
    if stacked == "relative":
        fig.update_layout(barmode="stack")
    fig.update_xaxes(
        type="category",
        tickangle=45,
    )
    col1.plotly_chart(fig)


def kpi_actual_bar_chart(df_filtered_vu_wps, df_filtered_adt):
    col1, col2 = st.beta_columns((6, 1))
    compare_by_configs = {
        "No Comparison": None,
        "Destination Countries": "destination_country",
        "Modalities": "vehicle_type",
        "Budget": "budget",
    }
    compare_by = add_compare_by_radio_buttons(
        col2, compare_by_configs, "kpi_compare_by_chart"
    )
    stacked = add_stacked_radio_buttons(col2, "kpi_compare_stacked")
    period = add_period_radio_buttons(col2, "kpi_period")
    kpis = {
        "ADT": {"calculated_distance": "sum", "kpi_weighting": "sum"},
        "WPS": {"weight_ton": "sum", "kpi_weighting": "sum"},
        "VU": {"final_vu": "mean"},
    }

    fig = go.Figure(layout=go.Layout(height=600, width=1000))
    fig = make_subplots(
        rows=1,
        cols=3,
        start_cell="top-left",
        figure=fig,
        subplot_titles=tuple(kpis.keys()),
    )
    if compare_by == "budget":
        budget_clicked = True
        compare_by = None
    else:
        budget_clicked = False

    for kpi, agg in kpis.items():
        if kpi == "ADT":
            df_filtered_kpi = aggregate_table(
                df_filtered_adt, agg, compare_by, is_stacked=False, period=period
            )
            df_filtered_kpi["ADT"] = (
                df_filtered_kpi["calculated_distance"]
                / df_filtered_kpi["kpi_weighting"]
            )
            df_filtered_kpi = df_filtered_kpi.drop(
                ["calculated_distance", "kpi_weighting"], axis=1
            )

            df_filtered_kpi = handle_budget_charts(
                budget_clicked,
                df_filtered_adt,
                df_filtered_kpi,
                period,
                "adt_bu",
                "ADT",
            )
            fig_single = single_bar_chart_gl(df_filtered_kpi)
            fig.add_traces(fig_single.data, 1, 1)

        elif kpi == "WPS":
            df_filtered_kpi = aggregate_table(
                df_filtered_vu_wps, agg, compare_by, is_stacked=False, period=period
            )
            df_filtered_kpi["WPS"] = (
                df_filtered_kpi["weight_ton"] / df_filtered_kpi["kpi_weighting"]
            )
            df_filtered_kpi = df_filtered_kpi.drop(
                ["weight_ton", "kpi_weighting"], axis=1
            )
            df_filtered_kpi = handle_budget_charts(
                budget_clicked,
                df_filtered_vu_wps,
                df_filtered_kpi,
                period,
                "wps_bu",
                "WPS",
            )
            fig_single = single_bar_chart_gl(df_filtered_kpi)
            fig.add_traces(fig_single.data, 1, 2)

        elif kpi == "VU":
            df_filtered_kpi = aggregate_table(
                df_filtered_vu_wps, agg, compare_by, is_stacked=False, period=period
            )
            df_filtered_kpi = handle_budget_charts(
                budget_clicked,
                df_filtered_vu_wps,
                df_filtered_kpi,
                period,
                "vu_bu",
                "final_vu",
            )
            fig_single = single_bar_chart_gl(df_filtered_kpi)
            fig.add_traces(fig_single.data, 1, 3)

        fig.update_traces(showlegend=False)
        fig.update_traces(showlegend=True, row=1, col=3)
    if stacked == "relative":
        fig.update_layout(barmode="stack")

    fig.update_xaxes(
        type="category",
        tickangle=45,
    )
    fig.update_layout(autosize=True)
    col1.plotly_chart(fig)


def handle_budget_charts(
    budget_clicked, df, df_filtered_kpi, period, kpi_name, kpi_rename
):
    if budget_clicked:
        df_filtered_kpi_bu = aggregate_table(
            df, {kpi_name: "mean"}, None, is_stacked=False, period=period
        )
        df_filtered_kpi_bu.insert(loc=0, column="legend", value="Budget")
        df_filtered_kpi_bu = df_filtered_kpi_bu.rename(columns={kpi_name: kpi_rename})
        df_filtered_kpi.insert(loc=0, column="legend", value="Actual")
        df_filtered_kpi = pd.concat([df_filtered_kpi, df_filtered_kpi_bu])
    return df_filtered_kpi


def simulated_kpi_line_charts(df_sim_vu_wps: pd.DataFrame, df_sim_adt: pd.DataFrame):
    fig = make_subplots(rows=2, cols=2, start_cell="bottom-left")
    fig = add_sim_charts(
        fig,
        df_sim_adt,
        "all_dist",
        "all_co2",
        "Total Distance in KMs",
        "Total CO2 in Tonnes",
        1,
        1,
    )
    fig = add_sim_charts(
        fig, df_sim_vu_wps, "all_wps", "all_co2", "Average WPS in Tonnes", "", 1, 2
    )
    fig = add_sim_charts(
        fig,
        df_sim_adt,
        "sim_n_trucks",
        "all_co2",
        "Total Number of Vehicles",
        "Total CO2 in Tonnes",
        2,
        1,
    )
    fig = add_sim_charts(
        fig, df_sim_vu_wps, "all_vu", "all_co2", "Average VU in %", "", 2, 2
    )
    fig.update_layout(height=700, width=1200)
    fig.update_yaxes(nticks=15)
    fig.update_xaxes(nticks=15)
    st.plotly_chart(fig)


def add_sim_charts(fig, df_sim, x, y, x_label, y_label, row, col):
    months = [1]  # df_sim.month.unique()
    for _ in months:
        df_sim_temp = df_sim.copy()
        fig.add_trace(
            go.Scatter(
                x=df_sim_temp[x],
                y=df_sim_temp[y],
                name="",
                line_shape="linear",
            ),
            row=row,
            col=col,
        )
        fig.add_annotation(
            x=df_sim_temp[x][0],
            y=df_sim_temp[y][0],
            text="Actual",
            showarrow=True,
            arrowhead=3,
            row=row,
            col=col,
        )
        if df_sim_temp.shape[0] > 1:
            fig.add_annotation(
                x=df_sim_temp[x].tail(1).values[0],
                y=df_sim_temp[y].tail(1).values[0],
                text="Optimal",
                showarrow=True,
                arrowhead=3,
                row=row,
                col=col,
            )
        x_range = [
            round(float(min(df_sim_temp[x].values)) * 0.998, 2),
            round(float(max(df_sim_temp[x].values)) * 1.002, 2),
        ]

        y_range = [
            round(float(min(df_sim_temp[y].values)) * 0.999, 2),
            round(float(max(df_sim_temp[y].values)) * 1.001, 2),
        ]
        fig.update_xaxes(
            title_text=x_label,
            range=x_range,
            row=row,
            col=col,
            tickangle=45,
        )
        fig.update_yaxes(title_text=y_label, range=y_range, row=row, col=col)

    fig.update_traces(
        mode="lines+markers",
        row=row,
        col=col,
        hovertemplate="<br>".join(
            [
                x_label + ": %{x}",
                "CO2: %{y}",
            ]
        ),
    )
    return fig


def driver_chart(df):
    col1, col2 = st.beta_columns((1, 1))

    colors = [
        "Non-satisfying KPI" if x > 0 else "Satisfying KPI" for x in df["CO2 Gain"]
    ]

    fig_abs = px.bar(
        df,
        x=df["KPI"],
        y=df["CO2 Gain"],
        color=colors,
        color_discrete_map={"Non-satisfying KPI": "red", "Satisfying KPI": "green"},
        height=500,
        width=500,
        title="Absolute CO2 Gain",
    )

    relative_diff = (df["Actual"] - df["Target Value"]) / (df["Target Value"])

    relative_diff[df["KPI"] == "VU"] = (
        df[df["KPI"] == "VU"]["Actual"] - df[df["KPI"] == "VU"]["Target Value"]
    )
    # relative_diff = relative_diff * [-1 if x in ['WPS' or 'VU'] else 1 for x in df['KPI']]

    fig_rel = px.bar(
        df,
        x=df["KPI"],
        y=relative_diff * 100,
        color=colors,
        color_discrete_map={"Non-satisfying KPI": "red", "Satisfying KPI": "green"},
        height=500,
        width=500,
        title="Relative deviation KPI budget",
        labels={"y": "% difference from target"},
    )

    # fig_temp.show()
    col1.plotly_chart(fig_abs)
    col2.plotly_chart(fig_rel)
