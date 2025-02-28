import logging
from elasticsearch import Elasticsearch
import psycopg2
import time
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PushDataToES:
    
    def __init__(self, host):
        # Initializing Elasticsearch connection
        self.host = host
        self.es = None
        self.index_name = "skin_product_list"
        self.connect_es()

    def connect_es(self):
        retry_attempts = 5
        backoff_factor = 2  # Exponential backoff factor
        for attempt in range(retry_attempts):
            try:
                # Attempt to connect to Elasticsearch with Content-Type header
              
                self.es = Elasticsearch(self.host, request_timeout=100, headers={"Content-Type": "application/json"})


                if self.es.ping():
                    logger.info("Elasticsearch connection is alive.")
                    return True
                else:
                    logger.error("Elasticsearch connection failed.")
            except Exception as e:
                logger.error(f"Error connecting to Elasticsearch: {e}")
            
            # Exponential backoff before retrying
            sleep_time = backoff_factor ** attempt + random.uniform(0, 1)
            logger.info(f"Retrying in {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
        
        logger.error("Elasticsearch connection failed after multiple attempts.")
        return False

    def database_connection(self):
        # Connecting to the database and fetching data
        try:
            with psycopg2.connect(
                host="db",  # Use Docker container name or network alias
                user="postgres",
                password="1234",
                database="testdb"
            ) as connection:
                logger.info("Connected to PostgreSQL database.")
                with connection.cursor() as cursor:
                    query = "SELECT * FROM skinproducts"
                    cursor.execute(query)
                    logger.info("Fetched data from PostgreSQL.")
                    return cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Database error: {e}")
            return []

    def create_index(self):
    # Check if the Elasticsearch index exists, if not, create it with custom mappings
        if self.es and not self.es.indices.exists(index=self.index_name):
            try:
                self.es.indices.create(
                    index=self.index_name,
                    body={
                        "mappings": {
                            "properties": {
                                "product_name": {"type": "text"},
                                "product_price": {"type": "float"},
                                "product_brand": {"type": "text"},
                                "product_qty": {"type": "text"},
                                "product_skin_type": {"type": "text"},
                                "product_highlights": {"type": "text"},
                                "product_description": {"type": "text"},
                            }
                        }
                    }
                )
                logger.info(f"Index '{self.index_name}' created successfully.")
            except Exception as e:
                logger.error(f"Error creating index: {e}")
        else:
            logger.info(f"Index '{self.index_name}' already exists.")

    def database_to_es(self):
        # Fetch rows from the database and push them to Elasticsearch
        rows = self.database_connection()
        if not rows:
            logger.warning("No data fetched from database.")
            return

        for row in rows:
            # Adjusting the unpacking to check the length of the row
            if len(row) == 8:
                p_id, p_name, p_price, p_brand, p_qty, p_skin_type, p_highlights, p_description = row
                documents = {
                    "product_name": p_name,
                    "product_price": p_price,
                    "product_brand": p_brand,
                    "product_qty": p_qty,
                    "product_skin_type": p_skin_type,
                    "product_highlights": p_highlights,
                    "product_description": p_description,
                }

                doc_id = f"{p_name}_{p_brand}"  # Unique doc_id based on product name and brand
                try:
                    result = self.es.index(index=self.index_name, id=doc_id, body=documents)
                    logger.info(f"Data inserted into Elasticsearch: Document ID: {result['_id']}")
                    self.es.indices.refresh(index=self.index_name)
                except Exception as e:
                    logger.error(f"Error inserting data to Elasticsearch: {e}")
            else:
                logger.warning(f"Skipping row with unexpected number of columns: {len(row)}")

    def available_data_es(self):
        # Fetch and display available data from Elasticsearch
        try:
            result = self.es.search(index=self.index_name, size=100)  # You can adjust size if necessary
            data_list = []
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
            logger.info(f"Fetched {len(data_list)} documents from Elasticsearch.")
            return data_list
        except Exception as e:
            logger.error(f"Error fetching data from Elasticsearch: {e}")
            return []

# Main execution
host = "http://elasticsearch:9200"  # Elasticsearch host URL (for containers within the same Docker network)
p = PushDataToES(host)

# Ensure the index is created before inserting data
p.create_index()  # This will create the index if it doesn't exist

# Push data from PostgreSQL to Elasticsearch
p.database_to_es()  # Push data from PostgreSQL to Elasticsearch

# Optional: Get data from Elasticsearch
result = p.available_data_es()  # Get data from Elasticsearch
if result:
    print(f"Total documents fetched from Elasticsearch: {len(result)}")
else:
    print("No documents found.")
