import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import snowflake.connector

def files_load():
    # Title and description of the app
    st.title("Simple Web Application")
    st.write("Welcome to this Streamlit web app! Here you can upload files, input data, and visualize results.")

    # Text Input
    user_name = st.text_input("Enter your name:", "")
    if user_name:
        st.write(f"Hello, **{user_name}**! 👋")

    # File Upload (CSV File)
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Load the file as a Pandas DataFrame
        data = pd.read_csv(uploaded_file)
        st.write("### Uploaded Data:")
        st.dataframe(data)

        # Visualize the data (Example: Plot the first two numeric columns)
        st.write("### Data Visualization:")
        if len(data.columns) >= 2:
            col1, col2 = data.columns[:2]
            fig, ax = plt.subplots()
            ax.plot(data[col1], data[col2], marker="o")
            ax.set_title("Line Plot")
            ax.set_xlabel(col1)
            ax.set_ylabel(col2)
            st.pyplot(fig)
        else:
            st.write("The file does not have enough numeric columns to plot.")
# Establish a connection to Snowflake
def connect_to_snowflake():
    try:
        conn = snowflake.connector.connect(
            user='GoodJob',
            password='GoodJob@1234',
            account='yqb72852',  # e.g., 'xyz12345.us-east-1'
            warehouse='CORTEX_ANALYST_WH',
            database='CORTEX_ANALYST_DEMO',
            schema='REVENUE_TIMESERIES',
            role='CORTEX_USER_ROLE'  # Specify the role here
        )
        return conn
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
        return None

# Execute a query
def execute_query(query):
    conn = connect_to_snowflake()
    if conn:
        try:
            cur = conn.cursor()
            st.write(query)
            cur.execute(query)
            results = cur.fetchall()
            # Convert to DataFrame for better visualization
            #columns = [desc[0] for desc in cur.description]  # Column names
            #df = pd.DataFrame(results, columns=columns)
            df = pd.DataFrame(results)
            cur.close()
            return df
        except Exception as e:
            st.warning(f"Error executing query: {e}")
        finally:
            conn.close()
        return st.write("Query Not executed!")
def Query_search():
        #st.write("Enter your Snowflake SQL query:")
        # User input for Snowflake query
        query = st.chat_input("Enter your Snowflake SQL query:")
        #query = st.text_area("Enter your Snowflake SQL query:", "select * from REVENUE_TIMESERIES.REGION_DIM")
        if query:
            input_string = query
            if input_string.strip() != "":
                st.write("Your question: ")
                st.write(query)
                # Run the query and fetch data from Snowflake
                data = execute_query(query)
            
                # Show results in a table if data exists
                if data is not None:
                    with st.chat_message("assistant"):
                        st.write("Query Results:")
                        st.write(data)
            else:
                st.warning("Please enter a valid query.")
        else:
            if query is not None: 
                st.warning("Please enter a valid query.")

def Question_Ask():
    #st.write("Ask your question:")
    # User input for questions
    question = st.chat_input("Ask your question:") 
    if question:
        input_string = question
        if input_string.strip() != "":
            st.write("Your question: ")
            st.write(question)
            # Run the question and fetch data from Snowflake
            data = get_snowflake_answer(question)
        
            # Show results in a table if data exists
            if data is not None:
                with st.chat_message("assistant"):
                    st.write("Query Results:")
                    st.write(data)
        else:
            st.warning("Please enter a valid question.")
    else:
        if question is not None: 
            st.warning("Please enter a valid question.")

# Function to connect to Snowflake and fetch data
def get_snowflake_answer(question):
    conn = connect_to_snowflake()
    if conn:
     try:
         prompt = question  
         query = f"""Select 
                 snowflake.cortex.complete(
                 'mistral-large2',
                 '{prompt}'
                  ) as answer
                  from REVENUE_TIMESERIES.REGION_DIM"""
         cur = conn.cursor()
         cur.execute(query)
         results = cur.fetchall()
         # Convert to DataFrame for better visualization
         #columns = [desc[0] for desc in cur.description]  # Column names
         #df = pd.DataFrame(results, columns=columns)
         df = pd.DataFrame(results)
         cur.close()
         return df
     except Exception as e:
         st.error(f"Error: {str(e)}")
         return None
     #return st.write("Query Not executed!")

# Streamlit UI
def main():
    st.title("Snowflake Query with Streamlit")
    
    # Options for the dropdown
    options = ["Query Search", "Question Ask","File Load"]
    
    # Create a dropdown box
    selected_option = st.selectbox("Choose an option:", options)
    
    with st.chat_message("assistant"):
        st.write("Hello 👋")
        # Display the selected option
        st.write(f"You selected: {selected_option}")
        
    # Call the function based on the selected option
    if selected_option == "Query Search":
        Query_search()
    elif selected_option == "Question Ask": 
        Question_Ask()
    elif selected_option == "File Load": 
        files_load()
    elif selected_option == "Use Teplete document": 
        files_load()      
          
# Sidebar Example
st.sidebar.title("Sidebar Options")
option = st.sidebar.selectbox("Choose an option:", ["Home", "About"])

if option == "Home":
    st.sidebar.write("You're on the Home page!")
    main()
elif option == "About":
    st.sidebar.write("This is a simple web app built with Streamlit.")