from elasticsearch import Elasticsearch, exceptions
import re

class CustomerDetails:
    def __init__(self, host="http://localhost:9200"):
        self.customer_details=[]
        self.mobile_pattern=r"^(\+91|0)?[6-9][0-9]{9}$"
        self.index_name = "mobile_list_index"
        self.cust_details = []
        self.es = Elasticsearch(host, basic_auth=("elastic", "elastic"))

    def get_name(self):
        while True:
            customer_name=input("Enter Name : ").strip()
            if len(customer_name)>2 and customer_name.isalpha():
                return customer_name
            print("Invalid name. Please try again! : ")

    def get_mobile_no(self):
        while True:
            customer_mobile_no=input("Enter Mobile Number : ")
            if re.match(self.mobile_pattern,customer_mobile_no):
                return customer_mobile_no
            print("Invalid Mobile Number. Please try again! : ")

    def get_address(self):
        while True:
            customer_address=input("Enter Your Address : ")
            if len(customer_address)>5 and len(customer_address)<25:
                return customer_address
            print("Invalid Address. Please try again! : ")

    def get_cust_details(self):
        cust_list={
            "cust_name":self.get_name(),
            "cust_mobile_no":self.get_mobile_no(),
            "cust_address":self.get_address(),

        }
        self.customer_details.append(cust_list)

    def search_query(self, data):
        query = {
            "query": {
                "multi_match": {
                    "query": data,
                    "fields": [
                        "product_name^2",  
                        "product_brand^2",
                        "product_description^2",
                        "product_skin_type^2",
                        "product_highlights^2",
                        "product_qty"
                    ],
                    "fuzziness": 2,
                    "type": "best_fields"
                }
            }
        }
        return query

    
    def search_data(self, data):
        query=self.search_query(data)
        results = []
        try:
            if self.es.ping():
                response = self.es.search(index=self.index_name, body=query)
                
                for hit in response["hits"]["hits"]:
                    source = hit["_source"]
                    product = {
                        "product_name": source.get("product_name", "N/A"),
                        "product_price": source.get("product_price", "N/A"),
                        "product_brand": source.get("product_brand", "N/A"),
                        "product_qty": source.get("product_qty", "N/A"),
                        "product_skin_type": source.get("product_skin_type", "N/A"),
                        "product_highlights": source.get("product_highlights", "N/A"),
                        "product_description": source.get("product_description", "N/A")
                    }
                    results.append(product)
            else:
                raise exceptions.ConnectionError("Elasticsearch server is not reachable.")

        except exceptions.ConnectionError as e:
            # Handle connection error
            print(f"Connection error: {e}")
            # You can return an empty list or any fallback behavior here
            results = []
        
        except exceptions.NotFoundError as e:
            # Handle "not found" errors if specific index or document is not found
            print(f"Not found error: {e}")
            results = []
        return results


#cust_details=CustomerDetails("http://localhost:9200")
#cust_details.get_cust_details()

#query=input("Search Your Product : ")
#result=cust_details.search_data(query)
