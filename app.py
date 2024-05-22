from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import sqlite3
import openai  # Importing the OpenAI module

# Configure our API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to load OpenAI Model and provide SQL query as response to NLP query
def get_openai_response(question, prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt[0]},
                {"role": "user", "content": question}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Function to retrieve records from the employee table
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return []

# Function to create and populate the Employee database
def create_and_populate_database():
    # Connect to the new SQLite database
    conn = sqlite3.connect('EmployeeDatabase.db')
    cursor = conn.cursor()

    # Drop the existing Employee table if it exists
    cursor.execute('DROP TABLE IF EXISTS Employee')

    # Create the new Employee table with the specified structure
    cursor.execute('''
    CREATE TABLE Employee (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        Department TEXT NOT NULL,
        Expertise TEXT NOT NULL,
        Location TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    ''')

    # Insert 30 records into the Employee table with cities from around the world
    employees = [
        ('John', 'Doe', 'Legal', 'Criminal Law', 'New York', 'john.doe1@example.com'),
        ('Jane', 'Smith', 'Legal', 'Family Law', 'Tokyo', 'jane.smith2@example.com'),
        ('Emily', 'Johnson', 'Legal', 'Criminal Law', 'Sydney', 'emily.johnson3@example.com'),
        ('Michael', 'Brown', 'Legal', 'Corporate Law', 'Berlin', 'michael.brown4@example.com'),
        ('Chris', 'Davis', 'Legal', 'Civil Rights', 'Toronto', 'chris.davis5@example.com'),
        ('Jessica', 'Miller', 'Legal', 'Criminal Law', 'Paris', 'jessica.miller6@example.com'),
        ('Daniel', 'Wilson', 'Legal', 'Family Law', 'Dubai', 'daniel.wilson7@example.com'),
        ('Sarah', 'Moore', 'Legal', 'Corporate Law', 'Hong Kong', 'sarah.moore8@example.com'),
        ('David', 'Taylor', 'Legal', 'Civil Rights', 'San Francisco', 'david.taylor9@example.com'),
        ('Laura', 'Anderson', 'Legal', 'Criminal Law', 'Singapore', 'laura.anderson10@example.com'),
        ('James', 'Thomas', 'Legal', 'Family Law', 'Mumbai', 'james.thomas11@example.com'),
        ('Anna', 'Jackson', 'Legal', 'Corporate Law', 'São Paulo', 'anna.jackson12@example.com'),
        ('Robert', 'White', 'Legal', 'Civil Rights', 'Mexico City', 'robert.white13@example.com'),
        ('Patricia', 'Harris', 'Legal', 'Criminal Law', 'Moscow', 'patricia.harris14@example.com'),
        ('Linda', 'Martin', 'Legal', 'Family Law', 'Istanbul', 'linda.martin15@example.com'),
        ('Mark', 'Thompson', 'Legal', 'Corporate Law', 'Seoul', 'mark.thompson16@example.com'),
        ('Mary', 'Garcia', 'Legal', 'Civil Rights', 'Bangkok', 'mary.garcia17@example.com'),
        ('Charles', 'Martinez', 'Legal', 'Criminal Law', 'Buenos Aires', 'charles.martinez18@example.com'),
        ('Barbara', 'Robinson', 'Legal', 'Family Law', 'Rome', 'barbara.robinson19@example.com'),
        ('Joseph', 'Clark', 'Legal', 'Corporate Law', 'Cape Town', 'joseph.clark20@example.com'),
        ('Thomas', 'Rodriguez', 'Legal', 'Civil Rights', 'Jakarta', 'thomas.rodriguez21@example.com'),
        ('Susan', 'Lewis', 'Legal', 'Criminal Law', 'Kuala Lumpur', 'susan.lewis22@example.com'),
        ('Paul', 'Lee', 'Legal', 'Family Law', 'Shanghai', 'paul.lee23@example.com'),
        ('Nancy', 'Walker', 'Legal', 'Corporate Law', 'Beijing', 'nancy.walker24@example.com'),
        ('Steven', 'Hall', 'Legal', 'Civil Rights', 'Bangkok', 'steven.hall25@example.com'),
        ('Karen', 'Allen', 'Legal', 'Criminal Law', 'Lagos', 'karen.allen26@example.com'),
        ('Lisa', 'Young', 'Legal', 'Family Law', 'Nairobi', 'lisa.young27@example.com'),
        ('George', 'King', 'Legal', 'Corporate Law', 'Cairo', 'george.king28@example.com'),
        ('Betty', 'Wright', 'Legal', 'Civil Rights', 'Melbourne', 'betty.wright29@example.com'),
        ('Edward', 'Scott', 'Legal', 'Criminal Law', 'London', 'edward.scott30@example.com'),
    ]

    cursor.executemany('INSERT INTO Employee (FirstName, LastName, Department, Expertise, Location, email) VALUES (?, ?, ?, ?, ?, ?)', employees)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    st.success("Database 'EmployeeDatabase.db' with table 'Employee' has been created and populated with 30 records successfully.")

# Define your prompt
prompt = ["You are an expert in converting natural language questions to SQL query."
          "You speak any language. The SQL database has the name EMPLOYEE and has the following columns: FirstName, LastName, Department, Expertise, Location, email. \n\nFor example, \nExample 1 - How many employees are there?, the SQL command will be something like this: SELECT COUNT(*) FROM EMPLOYEE \nExample 2 - What is the name of the employee who has the email 'john.doe1@example.com'?, the SQL command will be something like this: SELECT FirstName, LastName FROM EMPLOYEE WHERE email = 'john.doe1@example.com'; \nExample 3 - Tell me all the employees who work in the Legal department. The SQL command will be something like this: SELECT FirstName, LastName FROM EMPLOYEE WHERE Department = 'Legal'; \n\n"
          "Now, you can ask me any question related to the EMPLOYEE table and I will convert it into SQL query for you."]

# Streamlit App
st.set_page_config(page_title="I can retrieve any SQL query", page_icon=":bar_chart:", layout="wide")
st.header("Semantic Search Bar to retrieve data from SQL Database. Works in any language!")

question = st.text_input("Input:", key="input")

submit = st.button("Ask the question")

# If the submit button is clicked
if submit:
    response = get_openai_response(question, prompt)
    if response:
        st.write(f"Generated SQL Query: {response}")
        data = read_sql_query(response, 'EmployeeDatabase.db')
        st.subheader("The response is:")
        for row in data:
            st.write(row)

# Button to create and populate the Employee database
if st.button('Create Employee Database'):
    create_and_populate_database()