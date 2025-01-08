# adding the links to the database by iterating the each row from the excel

import pandas as pd
import mysql.connector
from mysql.connector import Error
from openpyxl import load_workbook
from dotenv import load_dotenv
import os

load_dotenv()

# Database configuration details
db_config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', ''),
    'password': os.getenv('MYSQL_ROOT_PASSWORD', ''),
    'database': os.getenv('MYSQL_DB', 'default_db_name')
}

# Path to the Excel file containing college data
excel_file = r"C:\Users\thrived\Downloads\USA College ids.xlsx"

try:
    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file)
    
    # Select relevant columns: 'id', 'colleges', 'fb group link', 'watsup community link for each college'
    df1 = df.loc[:, ['id', 'colleges', 'fb group link', 'watsup community link for each college ']]
    
    # Establish a connection to the MySQL database
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        print("Connected to MySQL")
        cursor = conn.cursor()
        
        # Rename the DataFrame columns for easier reference
        df1.columns = ["id", "colleges", "facebook", "whatsapp"]
        
        # Loop through each row in the DataFrame
        for index, row in df1.iterrows():
            # SQL query to insert Facebook group link into the 'social_links' table
            sql1 = '''
                INSERT INTO social_links(
                college_name, label, link, college_id
                )
                values(%s, %s, %s, %s)
            '''
            values1 = (
                row["colleges"],           # College name
                "facebook group link",     # Label for the link
                row["facebook"],           # Facebook group link
                row["id"]                  # College ID
            )
            
            # SQL query to insert WhatsApp community link into the 'social_links' table
            sql2 = '''
                INSERT INTO social_links(
                college_name, label, link, college_id
                )
                values(%s, %s, %s, %s)
            '''
            values2 = (
                row["colleges"],           # College name
                "whatsapp community link", # Label for the link
                row["whatsapp"],           # WhatsApp community link
                row["id"]                  # College ID
            )
            
            try:
                # Execute the queries to insert the data
                cursor.execute(sql1, values1)
                cursor.execute(sql2, values2)
                
                # Commit the transaction to save changes to the database
                conn.commit()
            except Error as e:
                # Print any error that occurs and rollback the transaction
                print(f"Error: {e}")
                conn.rollback()
except Error as e:
    # Print the error message if the connection or execution fails
    print(e)
finally:
    # Ensure the database connection is closed properly
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed")