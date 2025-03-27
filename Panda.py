import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


# Read the CSV file into a DataFrame
df = pd.read_csv('/home/sameer/Pictures/new_data.csv')

# Fill any missing values in the DataFrame with zeros
df.fillna(0, inplace=True)

try:
    # Connect to the MariaDB database using SQLAlchemy
    # SQLAlchemy connection string for MariaDB
    connection_string = "mysql+mysqlconnector://leela:leela@localhost/ai_db"
    engine = create_engine(connection_string)

    # Create a connection object from the engine
    connection = engine.connect()

    # Create a cursor object to execute SQL queries
    cursor = connection.connection.cursor()

    # Create the table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS leela (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        age INT,
        jan INT,
        feb INT,
        mar INT,
        apr INT
    );
    """
    cursor.execute(create_table_query)
    print("Table `leela` checked/created.")

    # Insert data into the table
    insert_query = """
    INSERT IGNORE INTO leela (name, age, jan, feb, mar, apr) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    data = [tuple(x) for x in df[['name', 'age', 'jan', 'feb', 'mar', 'apr']].values]
    cursor.executemany(insert_query, data)
    print(f"Inserted {len(data)} rows into the `leela` table.")

    # Commit the changes
    connection.commit()

    # Fetch data into a pandas DataFrame, excluding the 'id' column
    query = "SELECT name, age, jan, feb, mar, apr FROM leela"
    df_new = pd.read_sql(query, engine)

    # Print the first few rows of the DataFrame, excluding 'id'
    print("Data retrieved from the database:")
    display(df_new)  # `display()` is preferred in Jupyter to display DataFrames

    # Create a Pie Chart for Age Distribution
    age_counts = df_new['age'].value_counts()

    # Plot the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Age Distribution')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

    # Create a Pie Chart for Monthly Data (Sum of jan, feb, mar, apr)
    monthly_totals = df_new[['jan', 'feb', 'mar', 'apr']].sum()

    # Plot the pie chart for monthly data
    plt.figure(figsize=(8, 8))
    plt.pie(monthly_totals, labels=monthly_totals.index, autopct='%1.1f%%', startangle=90)
    plt.title('Monthly Data Distribution (jan - apr)')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

    # Hello World 
    # Hello World 2 

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # Close the cursor and connection if they were initialized
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'connection' in locals() and connection:
        connection.close()
    print("CSV data inserted successfully and connection closed.")