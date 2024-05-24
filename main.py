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

# Function to load Excel data from multiple sheets @st.cache
def load_excel_data(file_path):
    xls = pd.ExcelFile(file_path)
    sheet1 = pd.read_excel(xls, 'Sheet1')  # Adjust sheet names as necessary
    sheet2 = pd.read_excel(xls, 'Sheet2')
    return sheet1, sheet2

# Function to save the modified Excel data to multiple sheets
def save_excel_data(file_path, df1, df2):
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df1.to_excel(writer, index=False, sheet_name='Sheet1')
        df2.to_excel(writer, index=False, sheet_name='Sheet2')

# Load Excel data
excel_file = 'careerpathmodel.xlsx'  # path to your Excel file
df1, df2 = load_excel_data(excel_file)

st.title("Data Career Path Level Up")

# Display the data and take inputs for Sheet1
st.header("Input Parameters from Excel - Sheet1")
input_data1 = df1['Input Column'].values.tolist()  # Adjust column name as necessary
new_input_data1 = []

for i, val in enumerate(input_data1):
    new_val = st.number_input(f'Sheet1 Input {i+1}', value=val, min_value=0, max_value=5)
    new_input_data1.append(new_val)

# Update the DataFrame with new input values for Sheet1
df1['Input Column'] = new_input_data1

# Process the data and calculate results for Sheet1 (example logic)
st.header("Processed Results - Sheet1")
df1['Result Column'] = df1['Input Column'] * 2  # Replace with actual calculation logic

# Display the data and take inputs for Sheet2
st.header("Input Parameters from Excel - Sheet2")
input_data2 = df2['Input Column'].values.tolist()  # Adjust column name as necessary
new_input_data2 = []

for i, val in enumerate(input_data2):
    new_val = st.number_input(f'Sheet2 Input {i+1}', value=val, min_value=0, max_value=5)
    new_input_data2.append(new_val)

# Update the DataFrame with new input values for Sheet2
df2['Input Column'] = new_input_data2

# Process the data and calculate results for Sheet2 (example logic)
st.header("Processed Results - Sheet2")
df2['Result Column'] = df2['Input Column'] * 2  # Replace with actual calculation logic

# Display the results for both sheets
st.subheader("Results for Sheet1")
st.dataframe(df1)

st.subheader("Results for Sheet2")
st.dataframe(df2)

# Save the updated data to a new Excel file
if st.button('Save Results'):
    save_excel_data('updated_data.xlsx', df1, df2)
    st.success('Results saved to updated_data.xlsx')


# Run main()

if __name__ == '__main__':
    main()