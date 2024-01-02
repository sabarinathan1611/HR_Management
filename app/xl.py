import pandas as pd
import sqlite3
import os 

def createXL():
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    saveFolder = os.path.join(APP_ROOT, 'static', 'Test.xlsx')

    sqlite_file = '/home/harish/Documents/HR_Management/app/database.db'    # name of the SQLite database file

    # Check if the SQLite file exists
    if not os.path.isfile(sqlite_file):
        print("SQLite file does not exist.")
        return

    # Connect to the SQLite database
    conn = sqlite3.connect(sqlite_file)

    # Read SQLite query results into a pandas DataFrame
    xl = pd.read_sql_query("SELECT * FROM shift_time", conn)

    # Save the DataFrame to an Excel file
    xl.to_excel(saveFolder, index=False)

    # Close the SQLite connection
    conn.close()

createXL()
