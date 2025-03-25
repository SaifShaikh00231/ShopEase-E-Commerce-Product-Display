import requests
import pandas as pd

# URL for FakeStore API to fetch products
url = "https://fakestoreapi.com/products"

# Send a GET request to fetch the data
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()  # Convert JSON response to Python dictionary/list
    print("Data fetched successfully!")
    
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)
    
    # Show first 5 rows of the data
    print(df.head())
    
    # Optionally, save the data to a CSV file for future use
    df.to_csv("products_data.csv", index=False)
    print("Data saved to 'products_data.csv'")

else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
