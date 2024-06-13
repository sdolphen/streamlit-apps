import streamlit as st
import pandas as pd
from pathlib import Path
import base64

# Set Streamlit to wide mode
#st.set_page_config(layout="wide")
st.set_page_config(
page_title= "Career path",
page_icon="./icons/datarootsicon.ico"
)

# Function to convert image to bytes
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

# Sidebar content
def cs_sidebar():
    st.sidebar.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=170 height=32>](https://streamlit.io/)'''.format(img_to_bytes("dataroots-logo.png")), unsafe_allow_html=True)
    st.sidebar.header('Career path')
    st.sidebar.markdown(''' Career paths are journeys that our team members can follow within a specific role to progress and advance in their careers. These paths outline the various stages, skills, and experiences required for advancement within a particular role. Career paths provide a structured framework for our team members to plan and navigate their professional development journey, from entry-level positions to more senior or specialized roles.  ''', unsafe_allow_html=True)
    st.sidebar.markdown('__First, complete your own skill matrix evaluation__')
    st.sidebar.code('skillmatrix_dsu.xlsx')
    st.sidebar.markdown('__Instructions to use the app__')
    st.sidebar.markdown('You can visualize the progress you have made for every career path you want to explore. Please start by uploading your own skill matrix file.')
    st.sidebar.markdown('When the file is successfully uploaded, you can select the career path you want to explore to analyze your own skill progression.')
    st.sidebar.markdown('<small>Learn more about [career path levels](https://docs.streamlit.io/library/advanced-features/prerelease#beta-and-experimental-features)</small>', unsafe_allow_html=True)
    st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)
    st.sidebar.markdown('''<small>[Career path sheet](https://github.com/daniellewisDL/streamlit-cheat-sheet)  | June 2024 | [Dataroots](https://dataroots.io/)</small>''', unsafe_allow_html=True)

# Function to read and validate the uploaded file
def read_uploaded_file(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, sheet_name='Sheet1')
        necessary_columns = ['dummy', 'topic', 'domain', 'subdomain']
        if all(col in df.columns for col in necessary_columns):
            return df
        else:
            st.error("Necessary columns ('dummy', 'topic', 'domain', 'subdomain') not found in the uploaded file.")
            return None
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
        return None

# Function to display filtered columns
def display_filtered_columns(df, domain_prefix, display_name):
    dummy_column = pd.to_numeric(df['dummy'], errors='coerce')
    topic_column = df['topic']
    domain_column = df['domain']
    subdomain_column = df['subdomain']

    filtered_columns = df[[col for col in df.columns if col.startswith(domain_prefix)]]
    filtered_columns = filtered_columns.copy()
    filtered_columns.insert(0, 'dummy', dummy_column)
    filtered_columns.insert(0, 'topic', topic_column)
    filtered_columns.insert(0, 'subdomain', subdomain_column)

    consulting_df = filtered_columns[domain_column == 'Consulting'].reset_index(drop=True)
    bu_skills_df = filtered_columns[domain_column == 'BU Skills'].reset_index(drop=True)

    consulting_df.columns = ['subdomain', 'topic', 'dummy'] + [col[len(domain_prefix):] for col in consulting_df.columns[3:]]
    bu_skills_df.columns = ['subdomain', 'topic', 'dummy'] + [col[len(domain_prefix):] for col in bu_skills_df.columns[3:]]

    def apply_conditional_color(row):
        dummy_value = row['dummy']
        return ['background-color: lightgreen' if isinstance(cell_value, (int, float)) and cell_value <= dummy_value else '' for cell_value in row]

    def add_level_prefix(val):
        try:
            return f"Level {int(val)}"
        except ValueError:
            return val

    consulting_df_styled = consulting_df.style.apply(apply_conditional_color, axis=1).format(add_level_prefix)
    bu_skills_df_styled = bu_skills_df.style.apply(apply_conditional_color, axis=1).format(add_level_prefix)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write(f"{display_name} - BU Skills (left) and Consulting Skills (right)")
    col4, col5 = st.columns(2)
    with col5:
        st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
        st.dataframe(consulting_df_styled, height=min(400, 30 * len(consulting_df)))
        st.markdown("</div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
        st.dataframe(bu_skills_df_styled, height=min(400, 30 * len(bu_skills_df)))
        st.markdown("</div>", unsafe_allow_html=True)

# Main function to run the app
def main():
    cs_sidebar()

    st.title("Career Path Analyzer")
    st.write("Let's take a closer look at your skillmatrix and the most interesting domains to focus on in the future")

    st.markdown("""
        <style>
        .stButton>button {
            background-color: grey;
            color: white;
        }
        .dataframe-container {
            display: flex;
            justify-content: center;
        }
        .dataframe-container .stDataFrame {
            width: 45%;
            margin: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    file = st.file_uploader("Upload Your Personal Career Path Excel file", type=['xlsx'])

    if file is not None:
        df = read_uploaded_file(file)
        if df is not None:
            st.write("Your career path is successfully uploaded!")

            st.markdown("<br><br>", unsafe_allow_html=True)
            st.write("Let's now choose one of the career tracks in our unit to analyze our current skill progression")

            col1, col2, col3 = st.columns(3)
            with col1:
                ae_button = st.button("Analytics Engineer")
            with col2:
                ds_button = st.button("Data Strategy")
            with col3:
                at_button = st.button("Analytics Translator")

            if ae_button:
                display_filtered_columns(df, 'AE', 'Analytics Engineer')
            elif ds_button:
                display_filtered_columns(df, 'DS', 'Data Strategy')
            elif at_button:
                display_filtered_columns(df, 'AT', 'Analytics Translator')

if __name__ == '__main__':
    main()
