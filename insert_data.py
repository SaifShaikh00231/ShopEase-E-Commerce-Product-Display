import pandas as pd
import psycopg2
import json

# Load the CSV data into a DataFrame
df = pd.read_csv('products.csv')

# Print columns to verify the correct ones
print("Columns in the DataFrame:", df.columns)

# Ensure the 'rating' column is formatted as valid JSON
df['rating'] = df['rating'].apply(lambda x: json.loads(x.replace("'", '"')) if isinstance(x, str) else x)

# Print the data to check
print(df.head())

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname="postgres", 
        user="postgres", 
        password="5211", 
        host="localhost", 
        port="5432"
    )
    cursor = conn.cursor()
    print("Connection successful!")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit()

# Inserting data into the 'products' table using psycopg2
try:
    print("Inserting data into PostgreSQL...")

    # Insert data row by row
    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO products (id, title, price, description, category, image, rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (row['id'], row['title'], row['price'], row['description'], row['category'], row['image'], json.dumps(row['rating'])))

    # Commit the transaction
    conn.commit()
    print("Data inserted successfully!")

except Exception as e:
    print(f"Error inserting data: {e}")
    conn.rollback()

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
