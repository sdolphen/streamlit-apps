import logging
import os

import streamlit as st

from co2 import settings as s
from co2.interface import AzureInterface

interface = AzureInterface()
azure_logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
azure_logger.setLevel(logging.WARNING)


@st.cache(ttl=900)
def load_data_gl():
    return interface.read_csv(os.path.join(s.DATA_TRANSFORMED, "all_countries_gl.csv"))


@st.cache(ttl=900)
def load_data_gl_report():
    return interface.read_csv(os.path.join(s.DATA_TRANSFORMED, "gl_final_report.csv"))


@st.cache(ttl=900)
def load_data_adt():
    return interface.read_csv(os.path.join(s.DATA_TRANSFORMED, "all_countries_adt.csv"))


@st.cache(ttl=900)
def load_data_vu_wps():
    return interface.read_csv(
        os.path.join(s.DATA_TRANSFORMED, "all_countries_vu_wps.csv")
    )


@st.cache(ttl=900)
def load_static_gl_data():
    return interface.read_csv(os.path.join(s.DATA_TRANSFORMED, "gl_static.csv"))


@st.cache(ttl=900)
def load_data_hl():
    return interface.read_csv(os.path.join(s.DATA_TRANSFORMED, "hl_sold.csv"))


@st.cache(ttl=900)
def load_data_gl_bu():
    return interface.read_csv(os.path.join(s.DATA_TRANSFORMED, "bu_gl.csv"))


@st.cache(ttl=900)
def load_data_champions():
    return interface.read_csv(os.path.join(s.DATA_TRANSFORMED, "champions.csv"))


@st.cache(ttl=900)
def load_data_hl_bu():
    return interface.read_csv(os.path.join(s.DATA_TRANSFORMED, "bu_hl_sold.csv"))


@st.cache(ttl=900)
def load_wh_util_data():
    return interface.read_csv(os.path.join(s.DATA_TRANSFORMED, "wh_util.csv"))


@st.cache(ttl=900)
def load_modality_emissions():
    return interface.read_json(
        os.path.join(s.DATA_TRANSFORMED, "modality_emission.json")
    )


@st.cache(ttl=900)
def load_logo():
    return interface.read_image(os.path.join(s.DATA_TRANSFORMED, "abi-logo.png"))
