import os
import psycopg2
from dotenv import load_dotenv

load_dotenv('.env')

# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="postgres",  
        port=os.getenv("DATABASE_PORT")
    )
    cursor = connection.cursor()
    print("Connected to the database successfully!")

except (Exception, psycopg2.Error) as error:
    print(f"Error connecting to PostgreSQL database: {error}")

# Function to create a table and load data from a CSV file
def create_table_and_load_data(filename, restaurant_table_name, restaurant_columns, user_table_name, user_columns):
    if cursor is None or connection is None:
        print("Connection to the database was not established. Exiting.")
        return

    # Drop restaurant table if it exists
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {restaurant_table_name}")
        connection.commit()
        print(f"Table '{restaurant_table_name}' dropped successfully (if it existed).")
    except (Exception, psycopg2.Error) as error:
        print(f"Error dropping restaurant table: {error}")
        connection.rollback()

    # Creating restaurant_info table
    try:
        column_definitions = ", ".join(restaurant_columns)
        cursor.execute(f"CREATE TABLE {restaurant_table_name} ({column_definitions})")
        connection.commit()
        print(f"Table '{restaurant_table_name}' created successfully!")
    except (Exception, psycopg2.Error) as error:
        print(f"Error creating restaurant table: {error}")

    column_names = [col.split()[0] for col in restaurant_columns]  # Extract first element (column name)

    # Load data using copy_expert
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            cursor.copy_expert(
                f"COPY {restaurant_table_name} ({','.join(column_names)}) FROM STDIN WITH (FORMAT csv, HEADER true, DELIMITER ',')",
                f
            )
        connection.commit()
        print("Data loaded successfully!")
    except (Exception, psycopg2.Error) as error:
        print("Error while loading data:", error)
        connection.rollback()  # Rollback changes on error

    # Drop users table if it exists
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {user_table_name}")
        connection.commit()
        print(f"Table '{user_table_name}' dropped successfully (if it existed).")
    except (Exception, psycopg2.Error) as error:
        print(f"Error dropping Users table: {error}")
        connection.rollback()
    
    # Creating Users table
    try:
        column_definitions = ", ".join(user_columns)
        cursor.execute(f"CREATE TABLE {user_table_name} ({column_definitions})")
        connection.commit()
        print(f"Table '{user_table_name}' created successfully!")
    except (Exception, psycopg2.Error) as error:
        print(f"Error creating restaurant table: {error}")


    # Close connection
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Database connection closed.")

# Column definitions for the restaurant table
restaurant_columns = [
    "Restaurant_ID VARCHAR(255) PRIMARY KEY",
    "Restaurant_Name VARCHAR(255)",
    "Country_Code VARCHAR(3)",
    "City VARCHAR(255)",
    "Address VARCHAR(255)",
    "Locality VARCHAR(255)",
    "Locality_Verbose VARCHAR(255)",
    "Longitude FLOAT",
    "Latitude FLOAT",
    "Cuisines VARCHAR(255)",
    "Average_Cost_for_two INTEGER",
    "Currency VARCHAR(30)",
    "Has_Table_booking BOOLEAN",
    "Has_Online_delivery BOOLEAN",
    "Is_delivering_now BOOLEAN",
    "Switch_to_order_menu BOOLEAN",
    "Price_range INTEGER",
    "Aggregate_rating FLOAT",
    "Rating_color VARCHAR(50)",
    "Rating_text VARCHAR(50)",
    "Votes INTEGER",
    "Country VARCHAR(255)"
]

user_columns = [
    "Username VARCHAR(30)",
    "Email VARCHAR(30)",
    "Password_ VARCHAR(30)"
]

# Example usage
create_table_and_load_data('restaurants.csv', 'restaurant_info', restaurant_columns,'users',user_columns)
