from elasticsearch import Elasticsearch
import psycopg2

class PushDataToES:

    def __init__(self, host, user, password):
        self.es = Elasticsearch(host, basic_auth=(user, password)) if user and password else None
        self.index_name = "skin_product"

    def database_connection(self):
        try:
            with psycopg2.connect(
                host="localhost",
                user="postgres",
                password="1234",
                database="testdb"
            ) as connection:
                with connection.cursor() as cursor:
                    query = "SELECT * FROM skinproducts"
                    cursor.execute(query)
                    return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return []

    def database_to_es(self):
        rows = self.database_connection()
        for row in rows:
            p_name, p_price, p_brand, p_qty, p_skin_type, p_highlights, p_description = row
            documents = {
                "product_name": p_name,
                "product_price": p_price,
                "product_brand": p_brand,
                "product_qty": p_qty,
                "product_skin_type": p_skin_type,
                "product_highlights": p_highlights,
                "product_description": p_description,
            }

            doc_id = f"{p_name}_{p_brand}"
            try:
                result = self.es.index(index=self.index_name, id=doc_id, document=documents)
                print("Data inserted successfully:", result["_id"])
            except Exception as e:
                print(f"Error inserting data to Elasticsearch: {e}")

    def connect_es(self):
        try:
            return self.es.ping()
        except Exception as e:
            print(f"Error connecting to Elasticsearch: {e}")
            return False

    def create_index(self):
        if self.connect_es():
            if not self.es.indices.exists(index=self.index_name):
                try:
                    self.es.indices.create(index=self.index_name)
                    print("Index created successfully.")
                except Exception as e:
                    print(f"Error creating index: {e}")
            else:
                print("Index already exists.")

    def available_data_es(self):
        
        try:
            result = self.es.search(index=self.index_name, size=100) 
            data_list=[]
            for hit in result["hits"]["hits"]:
                source = hit["_source"]
                data_list.append(
                    f"Product Name: {source['product_name']} \n"
                    f"Product Price: {source['product_price']} \n"
                    f"Product Brand: {source['product_brand']} \n"
                    f"Product Qty: {source['product_qty']} \n"
                    f"Product Skin Type: {source['product_skin_type']} \n"
                    f"Product Highlights: {source['product_highlights']} \n"
                    f"Product Description: {source['product_description']}\n"
                )
            return data_list
            
            
                
        except Exception as e:
            print(f"Error fetching data from Elasticsearch: {e}")


host = "http://localhost:9200"
user = "elastic"
password = "elastic"
p = PushDataToES(host, user, password)

# Create index and push data
#p.create_index()
#p.database_to_es()
#result=p.available_data_es()
#print(result)

# Display available data

