import psycopg2
import logging
import time
import webscrapflipkart

# Configure logging
logging.basicConfig(level=logging.INFO)

# Retry connection to PostgreSQL database
def fetch_connection(retries=5, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            connection = psycopg2.connect(
                host="db",  # Update with actual host
                user="postgres",  # Update with actual user
                password="1234",  # Update with actual password
                database="testdb"  # Update with actual database name
            )
            logging.info("Connected to the database successfully.")
            return connection
        except psycopg2.OperationalError as e:
            logging.error(f"OperationalError: Failed to connect to the database. Attempt {attempt + 1}/{retries}", exc_info=True)
            attempt += 1
            time.sleep(delay)
        except Exception as e:
            logging.error(f"Error connecting to the database: {e}", exc_info=True)
            return None
    return None

# Create the table for storing products
def create_table(cursor):
    create_query = """
    CREATE TABLE IF NOT EXISTS skinproducts (
        id SERIAL PRIMARY KEY,
        product_name TEXT UNIQUE,
        product_price TEXT,
        product_brand TEXT,
        product_quantity TEXT,
        product_skin_type TEXT,
        product_highlights TEXT[],
        product_description TEXT
    );
    """
    try:
        cursor.execute(create_query)
        logging.info("Table 'skinproducts' created or already exists.")
    except psycopg2.DatabaseError as e:
        logging.error("Database error while creating table:", exc_info=True)
        raise

# Validate product data before insertion
def validate_product(product):
    if not product.get("name") or not product.get("price"):
        logging.warning(f"Invalid data for product {product.get('name', 'Unknown')}. Skipping insertion.")
        return False
    return True

# Insert product details into the database
def insert_to_database(cursor, product):
    if not validate_product(product):
        return

    try:
        insert_query = """
            INSERT INTO skinproducts(
                product_name, product_price, product_brand, product_quantity, 
                product_skin_type, product_highlights, product_description
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            product.get("name", ""),
            product.get("price", ""),
            product.get("brand", ""),
            product.get("quantity", ""),
            product.get("skin_type", ""),
            product.get("highlights", []),  
            product.get("description", "")
        ))
        logging.info(f"Successfully inserted product: {product.get('name', 'Unknown')}")
    except psycopg2.IntegrityError as e:
        logging.warning(f"Integrity error while inserting product '{product.get('name', 'Unknown')}': {e}")
    except psycopg2.Error as e:
        logging.error(f"Error inserting product '{product.get('name', 'Unknown')}': {e}", exc_info=True)

# Save scraped products to the database
def save_product_database():
    products = webscrapflipkart.get_all_product_details()
    if not products:
        logging.warning("No products to insert.")
        return
    connection = fetch_connection()
    if connection is None:
        return
    try:
        cursor = connection.cursor()
        create_table(cursor)
        for product in products:
            insert_to_database(cursor, product)
            connection.commit()
        logging.info("Data inserted successfully.")
    except Exception as e:
        logging.error("Error while inserting data into the database.", exc_info=True)
        connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        logging.info("Connection and cursor closed.")

# Run the script to scrape products and save them to the database
save_product_database()
