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

# Set Streamlit to wide mode
#st.set_page_config(layout="wide")

# Function to check installed packages
def check_installed_packages():
    installed_packages = subprocess.check_output(['pip', 'freeze']).decode('utf-8')
    return installed_packages

st.title("Data Career Path Level Up")

# Display installed packages
st.write("Installed Packages:")
st.text(check_installed_packages())

# Custom CSS to style the buttons and center the DataFrame
st.markdown("""
    <style>
    .stButton>button {
        background-color: grey;
        color: white;
        margin-right: 10px;
    }
    .dataframe-container {
        display: flex;
        justify-content: space-around;
    }
    .dataframe-container .stDataFrame {
        width: 45%;
        margin: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# File uploader
file = st.file_uploader("Upload Your Personal Career Path Excel file", type=['xlsx'])

if file is not None:
    try:
        # Load Excel data from the specified sheet
        df = pd.read_excel(file, sheet_name='Sheet1')

        # Check for necessary columns
        if all(col in df.columns for col in ['dummy', 'topic', 'domain', 'subdomain']):
            dummy_column = pd.to_numeric(df['dummy'], errors='coerce')
            topic_column = df['topic']
            domain_column = df['domain']
            subdomain_column = df['subdomain']

            # Create three columns for the buttons to be placed next to each other
            col1, col2, col3 = st.columns(3)

            with col1:
                ae_button = st.button("Analytics Engineer")
            with col2:
                ds_button = st.button("Data Strategy")
            with col3:
                at_button = st.button("Analytics Translator")

            def display_filtered_columns(domain_prefix, display_name):
                # Filter columns based on the selected domain prefix
                filtered_columns = df[[col for col in df.columns if col.startswith(domain_prefix)]]

                # Add the 'subdomain', 'topic', and 'dummy' columns to the filtered DataFrame
                filtered_columns = filtered_columns.copy()
                filtered_columns.insert(0, 'dummy', dummy_column)
                filtered_columns.insert(0, 'topic', topic_column)
                filtered_columns.insert(0, 'subdomain', subdomain_column)

                # Split the DataFrame based on the 'domain' column
                consulting_df = filtered_columns[domain_column == 'Consulting'].reset_index(drop=True)
                bu_skills_df = filtered_columns[domain_column == 'BU Skills'].reset_index(drop=True)

                # Apply conditional coloring function
                def apply_conditional_color(val, dummy_val):
                    return 'background-color: lightgreen' if val <= dummy_val else ''

                # Apply the coloring to both dataframes
                consulting_df_styled = consulting_df.style.applymap(lambda val: apply_conditional_color(val, consulting_df['dummy']), subset=pd.IndexSlice[:, 3:])
                bu_skills_df_styled = bu_skills_df.style.applymap(lambda val: apply_conditional_color(val, bu_skills_df['dummy']), subset=pd.IndexSlice[:, 3:])

                # Add 'Level ' prefix to all cells
                consulting_df_styled = consulting_df_styled.format(lambda val: f'Level {val}' if isinstance(val, (int, float)) else val)
                bu_skills_df_styled = bu_skills_df_styled.format(lambda val: f'Level {val}' if isinstance(val, (int, float)) else val)

                # Display the DataFrames side by side
                st.markdown(f"### {display_name}")
                col4, col5 = st.columns(2)
                with col4:
                    st.dataframe(consulting_df_styled)
                with col5:
                    st.dataframe(bu_skills_df_styled)

            if ae_button:
                display_filtered_columns('AE', 'Analytics Engineer')
            if ds_button:
                display_filtered











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


if __name__ == '__main__':
    main()
