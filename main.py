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
#button first
#df second
#add visuals (heatmap+)
#focus on progression
import streamlit as st
import pandas as pd
import subprocess

# Function to check installed packages
def check_installed_packages():
    installed_packages = subprocess.check_output(['pip', 'freeze']).decode('utf-8')
    return installed_packages

# Function to apply colors based on a dummy cell value
def apply_color_logic(cell_value, dummy_value):
    if pd.isna(cell_value):
        return ''
    elif cell_value <= dummy_value:
        return 'background-color: lightgreen'
    else:
        return ''

st.title("Data Career Path Level Up")

# Display installed packages
st.write("Installed Packages:")
st.text(check_installed_packages())

# File uploader
file = st.file_uploader("Upload Your Personal Career Path Excel file", type=['xlsx'])

if file is not None:
    try:
        # Load Excel data from the specified sheet
        df = pd.read_excel(file, sheet_name='Sheet1')

        # Select only the columns of interest
        ae_columns = df.filter(like='AE', axis=1)
        ds_columns = df.filter(like='DS', axis=1)
        at_columns = df.filter(like='AT', axis=1)

        # Get the 'dummy' column
        dummy_column = df['dummy']

        # Display domain buttons
        st.subheader("Select Domain to Display:")
        selected_domain = st.radio("For which domain do you want to improve?", ['AE', 'DS', 'AT'])

        # Display the filtered columns with conditional colors
        if selected_domain == 'AE':
            st.write("AE Columns:")
            dummy_value = st.number_input("Enter the dummy value:", value=0)
            for col in ae_columns.columns:
                ae_columns[col] = ae_columns[col].apply(lambda x: apply_color_logic(x, dummy_value))
            st.dataframe(ae_columns)
        elif selected_domain == 'DS':
            st.write("DS Columns:")
            dummy_value = st.number_input("Enter the dummy value:", value=0)
            for col in ds_columns.columns:
                ds_columns[col] = ds_columns[col].apply(lambda x: apply_color_logic(x, dummy_value))
            st.dataframe(ds_columns)
        elif selected_domain == 'AT':
            st.write("AT Columns:")
            dummy_value = st.number_input("Enter the dummy value:", value=0)
            for col in at_columns.columns:
                at_columns[col] = at_columns[col].apply(lambda x: apply_color_logic(x, dummy_value))
            st.dataframe(at_columns)
    except Exception as e:
        st.error(f"An error occurred: {e}")




        # remove info over current and next level!!
        #suggestive

        # Display results based on the selected domain
#        if selected_domain == 'AE':
#            st.subheader("On which domains do you need to improve to level up for the AE track?")
#            st.write(f"My current level: {ae_level}")
#            st.write("The following areas you should try to improve to level up again!:")
#            for value in ae_values:
#                st.write(value)
#        elif selected_domain == 'DS':
#            st.subheader("On which domains do you need to improve to level up for the DS track")
#            st.write(f"My current level: {ds_level}")
#            st.write("The following areas you should try to improve to level up again:")
#           for value in ds_values:
#                st.write(value)
#        elif selected_domain == 'AT':
#            st.subheader("On which domains do you need to improve to level up for the AT track")
#            st.write(f"My current level: {at_level}")
#            st.write("The following areas you should try to improve to level up again:")
#            for value in at_values:
#                st.write(value)
#    except Exception as e:
#        st.error(f"An error occurred: {e}")
    #add dynamic or simply space between the two parts, frames?


# Run main()

