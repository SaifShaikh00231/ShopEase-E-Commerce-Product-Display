from flask import Flask, render_template
import psycopg2
import json  # Import json to parse the rating string

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="5211",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        # Fetch data from the products table
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()

        cur.close()
        conn.close()

        # Debugging: Print the original products to check the format of the rating
        print("Fetched products:", products)

        # Parse the rating field and extract only the 'rate' value
        for i in range(len(products)):
            product = products[i]
            try:
                # Check if the rating is not null and parse it
                rating = product[6]  # Assuming the rating is the 7th column
                print(f"Original rating for product {product[0]}:", rating)  # Debugging line
                
                # If rating is a string, attempt to parse it as JSON
                if isinstance(rating, str):
                    try:
                        rating_data = json.loads(rating)  # Parse as JSON
                        products[i] = list(product)  # Convert tuple to list so it can be modified
                        products[i][6] = rating_data['rate']  # Replace the rating with the 'rate' value
                    except json.JSONDecodeError:
                        print(f"Error parsing JSON for product {product[0]}. Rating is not valid JSON.")
                        products[i] = list(product)
                        products[i][6] = 'N/A'  # Set to N/A if JSON is invalid
                else:
                    # If it's already a dictionary, just extract the rate value
                    products[i] = list(product)
                    products[i][6] = rating.get('rate', 'N/A')

            except Exception as e:
                print(f"Error processing rating for product {product[0]}: {e}")
                products[i] = list(product)
                products[i][6] = 'N/A'  # Set to N/A if there's an error in processing

        # Pass data to the template
        return render_template('index.html', products=products)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
