from sqlalchemy import create_engine

# Replace these with your PostgreSQL connection details
user = 'postgres'  # PostgreSQL username
password = '5211'  # PostgreSQL password
host = 'localhost'  # PostgreSQL host (default is 'localhost')
port = '5432'  # PostgreSQL port (default is '5432')
dbname = 'ecommerce_db'  # Name of your PostgreSQL database

# Create the connection string
connection_string = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'

# Create engine
engine = create_engine(connection_string)

try:
    # Test the connection
    with engine.connect() as conn:
        print("Connection successful!")
except Exception as e:
    print(f"Error connecting to database: {e}")
