import psycopg2
import webscrapflipkart

def get_product():
    return webscrapflipkart.get_all_product_details()

def fetch_connection():
    try:
        connection=psycopg2.connect(
            host = "localhost",
            user =  "postgres",
            password = "1234",
            database = "testdb"
        )
        return connection
    except Exception as e:
        print("Failed to connect")
        return None

def insert_to_database(cursor,product):
    try:
        insert_query = """
               INSERT INTO skinproducts(
                   product_name, product_price, product_brand, product_quantity, product_skin_type,product_highlights, product_description
               ) VALUES (%s, %s, %s, %s, %s, %s, %s)
               """
        cursor.execute(insert_query, (
            product.get("name", ""),
            product.get("price", ""),
            product.get("brand", ""),
            product.get("quantity",""),
            product.get("skin_type", ""),
            product.get("highlights", ""),
            product.get("description", "")
        ))
    except Exception as e:
        print(f"Error inserting product '{product.get('name', 'Unknown')}':", e)


def save_product_database():
    products = get_product()
    if not products:
        print("No products to insert.")
        return
    connection = fetch_connection()
    if connection is None:
        return
    try:
        cursor = connection.cursor()
        for product in products:
            insert_to_database(cursor,product)
        connection.commit()
        print("Data inserted successfully")
    except Exception as e:
        print("Error while inserting",e)
    finally:
        if cursor:
            cursor.close()
        connection.close()
save_product_database()


