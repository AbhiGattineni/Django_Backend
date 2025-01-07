import pandas as pd
import mysql.connector
from mysql.connector import Error
from openpyxl import load_workbook


db_config = {
    'host': 'database.ctnj0eswvoik.us-west-2.rds.amazonaws.com',
    'user': 'admin',
    'password': 'AbhishekAWS1234',
    'database': 'MYBLOG'
}

excel_file = r"C:\Users\thrived\Downloads\USA College ids.xlsx"

try:
    df = pd.read_excel(excel_file)
    df1 = df.loc[:,['id','colleges','fb group link','watsup community link for each college ']]
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        print("Connected to MySQL")
        cursor = conn.cursor()
        df1.columns = ["id","colleges","facebook","whatsapp"]
        for index, row in df1.iterrows():
            sql1 = '''
                INSERT INTO social_links(
                college_name, label, link, college_id
                )
                values(%s,%s,%s,%s)
            '''
            values1 = (
                row["colleges"],
                "facebook group link",
                row["facebook"],
                row["id"]
            )
            sql2 = '''
                INSERT INTO social_links(
                college_name, label, link, college_id
                )
                values(%s,%s,%s,%s)
            '''
            values2 = (
                row["colleges"],
                "whatsapp community link",
                row["whatsapp"],
                row["id"]
            )

            try:
                cursor.execute(sql1, values1)
                cursor.execute(sql2, values2)
                conn.commit()
            except Error as e:
                print(f"Error: {e}")
                conn.rollback()
except Error:
    print(Error)
finally:
     if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed")