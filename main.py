import streamlit as st
from pathlib import Path
import base64

# Initial page config

st.set_page_config(
     page_title='Streamlit cheat sheet',
     layout="wide",
     initial_sidebar_state="expanded",
)

def main():
    cs_sidebar()
    get_level_and_values()

    return None

# Thanks to streamlitopedia for the following code snippet

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

# sidebar

def cs_sidebar():

    st.sidebar.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=170 height=32>](https://streamlit.io/)'''.format(img_to_bytes("dataroots-logo.png")), unsafe_allow_html=True)
    st.sidebar.header('Career path')

    st.sidebar.markdown(''' Explore career path insights here ''', unsafe_allow_html=True)

    st.sidebar.markdown('__Line1__')

    st.sidebar.code('text 1')

    st.sidebar.markdown('__Instructions to use the app__')
    st.sidebar.markdown('You should start by copying your levels on different career path topics')

    st.sidebar.markdown('__Info 1__')


    st.sidebar.markdown('__Info 2__')
    st.sidebar.markdown('<small>Learn more about [career path levels](https://docs.streamlit.io/library/advanced-features/prerelease#beta-and-experimental-features)</small>', unsafe_allow_html=True)

    st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)
    st.sidebar.markdown('''<small>[Career path sheet](https://github.com/daniellewisDL/streamlit-cheat-sheet)  | June 2024 | [Dataroots](https://dataroots.io/)</small>''', unsafe_allow_html=True)

    return None

    




## APPLICATION FOR INPUT/OUTPUT 


import streamlit as st
import pandas as pd
import subprocess

# Function to check installed packages
def check_installed_packages():
    installed_packages = subprocess.check_output(['pip', 'freeze']).decode('utf-8')
    return installed_packages

# Function to check if a column is fully completed (i.e., all cells are empty)
def is_column_completed(column):
    return column.isna().all()

# Function to get the level and non-empty cells for a group of columns
def get_level_and_values(columns):
    level = 0
    non_empty_cells = []
    for col_name, col_data in columns.items():
        if not is_column_completed(col_data):
            level += 1
            non_empty_cells.extend(col_data.dropna().tolist())
            break  # Stop at the first non-empty column
    return level, non_empty_cells

st.title("Data Career Path Level Up")

# Display installed packages
st.write("Installed Packages:")
st.text(check_installed_packages())

# File uploader
file = st.file_uploader("Upload Excel file", type=['xlsx'])

if file is not None:
    try:
        # Load Excel data
        df = pd.read_excel(file, engine='openpyxl')

        # Debug: Display the loaded dataframe
        st.write("Loaded DataFrame:")
        st.write(df)

        # Select only the columns of interest
        ae_columns = df.filter(like='AE', axis=1)
        ds_columns = df.filter(like='DS', axis=1)

        # Debug: Display the filtered columns
        st.write("AE Columns:")
        st.write(ae_columns)
        st.write("DS Columns:")
        st.write(ds_columns)

        # Get level and non-empty cells for AE and DS columns
        ae_level, ae_values = get_level_and_values(ae_columns)
        ds_level, ds_values = get_level_and_values(ds_columns)

        # Display results
        st.subheader("Results for AE")
        st.write(f"Level: {ae_level}")
        st.write("Non-empty cells:")
        for value in ae_values:
            st.write(value)

        st.subheader("Results for DS")
        st.write(f"Level: {ds_level}")
        st.write("Non-empty cells:")
        for value in ds_values:
            st.write(value)
    except Exception as e:
        st.error(f"An error occurred: {e}")



# Run main()

if __name__ == '__main__':
    main()