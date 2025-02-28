import sys
import os
from datetime import datetime
from django.shortcuts import render
from django.conf import settings
from SkinProductA.pushToElasticsearch import PushDataToES
from SkinProductA.customer_details import CustomerDetails

# Update the path to allow imports from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Helper function for Elasticsearch connection
def get_es_connection():
    host = settings.ES_HOST  # You should define these in your settings.py
    
    
    connection = PushDataToES(host)
    if not connection.es.ping():
        raise Exception("Elasticsearch is not serviceable. Please try again later")
    return connection

# View to show data from Elasticsearch
def show_data(request):
    time_result = None
    error_msg = None
    result = None

    try:
        es_conn = get_es_connection()
        start_time = datetime.now()
        result = es_conn.available_data_es()
        end_time = datetime.now()
        time_result = end_time - start_time
    except Exception as e:
        error_msg = str(e)

    data_list = {
        "output": result,
        "time": time_result,
        "error_msg": error_msg
    }
    return render(request, "show_data.html", data_list)

# Homepage view
def homepage(request):
    return render(request, "homepage.html")

# View to load data from Elasticsearch
def load_data(request):
    time_taken = None
    error_msg = None
    result = None

    try:
        es_conn = get_es_connection()
        start_time = datetime.now()
        result = es_conn.available_data_es()
        end_time = datetime.now()
        time_taken = end_time - start_time
    except Exception as e:
        error_msg = str(e)

    data_list = {
        "result": result,
        "time_taken": time_taken,
        "error_msg": error_msg
    }
    return render(request, "load.html", data_list)

# Search data view from Elasticsearch
def search_data_page(request):
    result = None
    search_data = ""
    error_msg = None
    time_taken = None

    try:
        if request.method == "POST":
            search_data = request.POST.get("search_data", "").strip()
            if not search_data:
                return render(request, "homepage.html")  # No search input, redirect to homepage

            # Perform Elasticsearch search
            cust_obj = CustomerDetails(settings.ES_HOST)
            if not cust_obj.es.ping():
                raise Exception("Elasticsearch is not serviceable. Please try again later")

            start_time = datetime.now()
            result = cust_obj.search_data(search_data)
            end_time = datetime.now()
            time_taken = end_time - start_time
    except Exception as e:
        error_msg = str(e)

    search_list = {
        "result": result,
        "time_taken": time_taken,
        "error_msg": error_msg,
        "search_data": search_data
    }
    return render(request, "search.html", search_list)
