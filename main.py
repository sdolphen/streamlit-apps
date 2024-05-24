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
    cs_body()

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

    

##########################
# Main body of cheat sheet
##########################

def cs_body():

    col1, col2 = st.columns(2)

    #######################################
    # COLUMN 1
    #######################################
    
    # Display text

    col1.subheader('Display text')
    col1.code('''
    Dear data strategist

    We believe that building and nurturing our coaching culture is the most effective way to help you develop as a professional, 
    one who provides excellent services to our clients and works closely with other colleagues.
    ''')

    col1.code('''Navigating the data career landscape can be challenging, with numerous specializations and skill sets required to advance. Our innovative application is designed to help you
     identify the key areas you need to focus on to level up in your chosen data career path.

How It Works
Input Your Current Levels: Begin by inputting your current proficiency levels across various critical aspects of your data career, such as data analysis, machine learning, data visualization, and more.

Select Your Career Path: Choose your desired career path from a list of options, including roles like Data Scientist, Data Analyst, Data Engineer, and Data Strategist.

Get Tailored Feedback: Based on your inputs, our application analyzes the data and provides you with a detailed report highlighting the specific areas you need to improve on. 
This personalized feedback is aimed at helping you upgrade your total level and achieve your career goals efficiently.''')

    #######################################
    # COLUMN 2
    #######################################

    # Optimize performance

    col2.subheader('Optimize performance')
    col2.write('write instead of markdown is also an option, maybe the best one?')
    col2.code('''
    you can also add some code below to combine both, maybe to display 
    the results this way?
    ''')
    


    return None



## APPLICATION FOR INPUT/OUTPUT 




import streamlit as st
import pandas as pd

# Function to load Excel data from a single sheet
@st.cache
def load_excel_data(file_path):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, 'Sheet1')  # Adjust sheet name as necessary
    return df

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
            if level == 3:  # Adjust to the lowest level you want to reach
                break
    return level, non_empty_cells

st.title("Data Career Path Level Up")

# Input for file path
file_path = st.text_input("Enter the path to your Excel file:")

if file_path:
    try:
        # Load Excel data
        df = load_excel_data(file_path)

        # Select only the columns of interest
        ae_columns = df.filter(like='AE', axis=1)
        ds_columns = df.filter(like='DS', axis=1)

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