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

        # Extract the 'dummy' column and convert to numeric if it exists
        if 'dummy' in df.columns:
            dummy_column = pd.to_numeric(df['dummy'], errors='coerce')

            # Display domain buttons
            st.subheader("Select Domain to Display:")
            ae_button = st.button("AE")
            ds_button = st.button("DS")
            at_button = st.button("AT")

            def display_filtered_columns(domain_prefix):
                # Filter columns based on the selected domain prefix
                filtered_columns = df[[col for col in df.columns if col.startswith(domain_prefix)]]

                # Add the 'dummy' column to the filtered DataFrame and move it to the beginning
                filtered_columns = filtered_columns.copy()
                filtered_columns.insert(0, 'dummy', dummy_column)

                # Rename columns by removing the domain prefix
                filtered_columns.columns = ['dummy'] + [col[len(domain_prefix):] for col in filtered_columns.columns[1:]]

                # Display the filtered columns with conditional colors
                if not filtered_columns.empty:
                    st.write(f"{domain_prefix} Columns with conditional background color:")

                    # Define a function to apply conditional formatting
                    def apply_conditional_color(row):
                        dummy_value = row['dummy']
                        return ['background-color: lightgreen' if cell_value <= dummy_value else '' for cell_value in row]

                    # Apply conditional formatting using the function
                    styled_df = filtered_columns.style.apply(apply_conditional_color, axis=1)

                    # Add 'Level ' prefix to each cell value
                    def add_level_prefix(val):
                        try:
                            return f"Level {int(val)}"
                        except ValueError:
                            return val

                    styled_df = styled_df.format(add_level_prefix)

                    st.write(styled_df)
                else:
                    st.write(f"No {domain_prefix} columns found.")

            # Display the DataFrame based on the button clicked
            if ae_button:
                display_filtered_columns('AE')
            elif ds_button:
                display_filtered_columns('DS')
            elif at_button:
                display_filtered_columns('AT')
        else:
            st.write("No 'dummy' column found in the original DataFrame.")
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


if __name__ == '__main__':
    main()
