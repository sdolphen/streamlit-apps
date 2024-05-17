import app_co2.session
from app_co2.buttons import (
    add_radio_buttons_for_kpi_simulations,
    create_download_button,
    download_gl_buttons,
    download_sim_results_buttons,
    download_static_gl_buttons,
)
from app_co2.filters import add_filters, filter_df
from app_co2.graphs import (
    driver_chart,
    gl_actual_bar_chart,
    kpi_actual_bar_chart,
    simulated_kpi_line_charts,
)
from app_co2.tables import (
    create_actual_vs_optimum_table,
    create_budget_gl_dataframe,
    create_overall_simulated_table,
    create_simulation_table,
    create_st_table_gl,
    create_st_table_gl_shipment,
    create_st_table_kpi,
)
from app_co2.utils import *
from co2.model.modality import ModalityModel
from co2.model.transport_kpis import TransportKPIsModel
from co2.model.wh_util import WarehouseUtilisationModel


def actual_tab():
    st.title("Green Logistics Report")
    df_gl = load_data_gl()
    df_gl_report = load_data_gl_report()
    df_vu_wps = load_data_vu_wps()
    df_adt = load_data_adt()
    df_hl = load_data_hl()
    df_gl_bu = load_data_gl_bu()
    df_hl_bu = load_data_hl_bu()

    # Filters -----------------------------------------------------------------------
    filters = add_filters(df_gl)
    df_filtered_gl = filter_df(df_gl, filters)
    df_filtered_vu_wps = filter_df(df_vu_wps, filters)
    df_filtered_adt = filter_df(df_adt, filters)

    # General DataFrame table ----------
    st.header("GL General Report")
    """
    This table includes all trips that are used to report the Green Logistics KPI, it thus doesn't take into account 
    the filters on the left
    """
    df_agg_gl = create_st_table_gl(df_gl_report, df_hl, filters)
    df_bu_gl = create_budget_gl_dataframe(df_gl_report, df_gl_bu)
    download_static_gl_buttons(df_agg_gl, df_bu_gl, df_hl_bu, "gl_table_general")

    # Dynamic DataFrame table --------------------------------------------------------
    st.header("GL Shipment Level Report")
    """
    This table only takes into account the filters defined on the left. It thus doesn't take into account the default
    filters applied for the Green Logistics KPI. Instead of HL sold, this table reports HL transported because HL 
    sold is only defined at a country level and cannot be filtered down to shipment level
    """
    df_agg_gl_shipment = create_st_table_gl_shipment(
        df_filtered_gl, "co2_abi", "gl_table_shipment"
    )
    download_gl_buttons(df_filtered_gl, df_agg_gl_shipment, "gl_table_shipment")

    # KPIs table ---------------------------------------------------------------
    st.header("KPIs Table")
    """
    Analyse every KPI for which the relationship with the Green Logistics KPI has been modelled
    """
    df_agg_kpi = create_st_table_kpi(df_filtered_vu_wps, df_filtered_adt)
    create_download_button("Download Aggregated KPI", df_agg_kpi, "aggregated_kpi.csv")

    # Main line chart ---------------------------------------------------------------
    st.header("Visualisations")
    """
    You can analyse metrics included in the model.   
    By using the buttons in the top right corner, you can
    - Rescale the axes
    - Zoom in on part of the chart
    - Take snapshots
    """
    st.subheader("GL KPI Visualisations per Month")
    """
    Analyse the metrics used to calculate the GL KPI and compare them per country or modality
    """
    gl_actual_bar_chart(df_filtered_gl)

    st.subheader("ADT, VU and WPS KPI Visualisations per Month")
    """
    Analyse the KPIs impacting CO2 emission and compare them per country or modality but also per 
    budget to quickly identify under performing ones
    """
    kpi_actual_bar_chart(df_filtered_vu_wps, df_filtered_adt)


def simulated_tab():
    st.title("Driver Model")
    sess = app_co2.session.get(driver_model_started=False)
    df_vu_wps = load_data_vu_wps()
    df_adt = load_data_adt()
    df_wh_util = load_wh_util_data()

    # Filters -----------------------------------------------------------------------
    filters = add_filters(df_vu_wps)

    df_filtered_vu_wps = filter_df(df_vu_wps, filters)
    df_filtered_adt = filter_df(df_adt, filters)

    start_sim = st.button("Start Driver Model!")
    """
    The main principle behind the model is merging trucks according to predefined business constraints
    """

    if start_sim or sess.driver_model_started:
        sess.driver_model_started = True
        model_vu_wps = TransportKPIsModel(df_filtered_vu_wps)
        model_adt = TransportKPIsModel(df_filtered_adt)

        col1, _ = st.beta_columns([1, 3])
        n_truck_offset = col1.number_input(
            "Select number of truck offset:",
            value=max(1, (model_vu_wps.curr_n_trucks - model_vu_wps.min_n_trucks) // 5),
        )

        # ALL Scenarios
        df_sim_vu_wps = model_vu_wps.run_all_kpi_scenarios(n_truck_offset)
        df_sim_adt = model_adt.run_all_kpi_scenarios(n_truck_offset)

        st.header("Simulation Scenarios")
        """
        In these charts you see the impact every KPI has on CO2 emission.   
        For each KPI, only those trips are taken into account that are relevant to report this KPI   
        You see two points marked on the charts:   
        - ** Actual **: the current performance for that KPI
        - ** Optimal **: the lowest CO2 emission feasible according to the model by merging trucks   
        
        Every point in between indicates a situation using x trucks less where x is defined by the _Truck Offeset_ 
        selected at the top of this page
        """
        simulated_kpi_line_charts(df_sim_vu_wps, df_sim_adt)

        st.header("Download Simulation Results")
        """
        You can download the merged trucks raw data using the following buttons   
        """
        download_sim_results_buttons(
            model_vu_wps.df_optimal_simulation, model_adt.df_optimal_simulation
        )

        # Actual vs Optimal
        st.header("Actual vs Optimal")
        """
        For every relevant KPI impacting CO2, you get the following information   
        - ** Data Source **: the set of trips used to calculate the values for this KPI
        - ** Actual **: the current value for that KPI
        - ** Optimum **: the optimal value for that KPI when optimizing the model to minimize CO2
        - ** ABI Budget **: the value set forward by management
        - ** CO2 Actual **: the current CO2 emission for the set of trips included   
        - ** CO2 Optimum **: the CO2 emission if you would achieve the _Optimum_ value for this KPI
        """
        df_actual_vs_optimum = create_actual_vs_optimum_table(model_vu_wps, model_adt)
        st.dataframe(df_actual_vs_optimum)

        # CO2 Drivers table
        st.header("CO2 Drivers - Transport KPIs")
        """
        For every relevant KPI impacting CO2, you get the following information   
        - ** Data Source **: same as before, the set of trips included in the calculation of this KPI
        - ** Target Value **: if the management budget is achievable, this will be the target value, if not,
         the optimal model value is chosen
        - ** CO2 Gain **: How much CO2 would you save by focussing on improving this *one* KPI and achieving its
         target value
        """

        df_report = create_overall_simulated_table(model_vu_wps, model_adt)
        st.dataframe(df_report)
        driver_chart(df_report)

        # Individual Simulations
        st.header("Transport KPI Simulations")
        """
        In this section you can define your own simulation selecting a scenario between the actual one and the optimal one.   
        The value in the table might not match 100% with the value defined by you because the model will always 
        round to an integer amount of trucks.   
        The value of all other KPIs will adjust itself based on the value you defined for one specific KPI.
        """
        col1, _, col2 = st.beta_columns([1, 1, 5])
        n_trucks, wps, vu, dist, co2 = add_radio_buttons_for_kpi_simulations(
            model_vu_wps, model_adt, col1
        )
        df_sim = create_simulation_table(n_trucks, wps, vu, dist, co2)
        col2.dataframe(df_sim)

        # WH KPIs
        st.header("WH KPI Simulations")
        """
        In this section you can simulate the CO2 impact of the warehouse utilization. 
        
        Note that you can only apply ** Year, Month ** and ** Plant ** filters to this simulation
        """
        wh_util_filters = {
            desired_filters: filters[desired_filters]
            for desired_filters in ["year", "month", "plant"]
        }
        col1, _ = st.beta_columns([1, 4])
        target = col1.number_input(
            "Enter simulated WH capacity in %",
            min_value=0.0,
            max_value=100.0,
            value=85.0,
            step=0.01,
            key="wh_util",
        )
        df_filtered_wh_util = filter_df(df_wh_util, wh_util_filters)
        wh_model = WarehouseUtilisationModel(df_filtered_wh_util)
        df_wh_util_report = wh_model.compute_sim_co2(target)
        scope_columns = [
            "year",
            "month",
            "plant",
            "target_wu",
            "t1_wu_ac",
            "target_co2_deviation",
            "target_sim_deviation",
        ]
        st.dataframe(df_wh_util_report[scope_columns])
        create_download_button(
            "Download WH Util Full Data",
            df_wh_util_report,
            "wh_utilization.csv",
            "wh_utilization",
        )


def modality_model_tab():
    df_gl = load_data_gl()
    modality_emissions = load_modality_emissions()

    # Filters -----------------------------------------------------------------------
    filters = add_filters(df_gl)
    df_filtered_gl = filter_df(df_gl, filters)

    # Modality TransportKPIsModel
    st.header("Modality Scenarios")
    """
    For the trips that match the filter on the left, change the fuel type for a specific kind of transport fuel   
    **Note:**   
    - Fuel types are replaced randomly selecting trips to select fuel types completely. A median over different 
    random selections is reported.   
    - Make sure that the proportions with which you want to change one fuel type by the others add up to 100%
    - Depending on the scope of the filters, this calculation might take a while
    """
    col1, col2, col3, col4 = st.beta_columns([1, 1, 1, 1])
    all_vehicle_types = list(modality_emissions.keys())
    selected_vehicle_type = col1.selectbox(
        "Which modality type you would like to create a scenario?", all_vehicle_types
    )

    selectbox_dict = {
        vehicle_type: col2.checkbox(vehicle_type, key=vehicle_type)
        for vehicle_type in all_vehicle_types
    }

    new_modality_scenario_dict = {
        vehicle_type: col3.number_input(
            vehicle_type,
            min_value=0.0,
            max_value=100.0,
            value=100.0,
            step=0.01,
            key=vehicle_type,
        )
        / 100.0
        for vehicle_type, is_selected in selectbox_dict.items()
        if is_selected
    }

    if sum(new_modality_scenario_dict.values()) == 1.0:
        st.header("Change in CO2")
        col1, col2, _ = st.beta_columns([2, 2, 1])
        modality_model = ModalityModel(
            df_filtered_gl, selected_vehicle_type, modality_emissions
        )
        df_report = modality_model.run_model(new_modality_scenario_dict)
        col2.markdown(
            f"- Total current CO2: **{round(df_report.current_co2.sum(),2 )}** Tonnes"
        )
        col2.markdown(
            f"- Total new CO2: **{round(df_report.new_co2.sum(), 2)} ** Tonnes"
        )
        col2.markdown(
            f"- CO2 Savings: **{round(df_report.current_co2.sum() - df_report.new_co2.sum(), 2)} ** Tonnes"
        )
        col1.dataframe(df_report.round(2).fillna("-"))
    else:
        col4.warning("The sum of the values should be 100%!")


def champions_tab():
    df_champions = load_data_champions()
    st.title("Champions Table")
    """
    This table displays all the current actions planned or taking place to reduce CO2 emission
    """
    st.dataframe(df_champions.fillna("-"))


def app():
    st.set_page_config(layout="wide")
    logo = load_logo()
    st.sidebar.image(logo)
    st.sidebar.subheader("Navigation")

    option = st.sidebar.radio(
        "",
        (
            "Green Logistics",
            "Driver Model",
            "Modality Model",
            "Champions",
        ),
    )
    if option == "Green Logistics":
        actual_tab()
    elif option == "Driver Model":
        simulated_tab()
    elif option == "Modality Model":
        modality_model_tab()
    elif option == "Champions":
        champions_tab()


if __name__ == "__main__":
    app()
