import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SkinProductA.pushToElasticsearch import PushDataToES
from SkinProductA.customer_details import CustomerDetails
from django.shortcuts import render 
from datetime import datetime


def show_data(request):
    host="http://localhost:9200"
    user_name="elastic"
    password="elastic"
    p=PushDataToES(host, user_name, password)    
    start_time=datetime.now()
    result=p.available_data_es()
    end_time=datetime.now()
    time_result=end_time-start_time
    data_list={
        "output":result,
        "time":time_result
    }
    return render(request, "show_data.html",data_list)


def homepage(request):
    return render(request, "homepage.html")

def load_data(request):
    host="http://localhost:9200"
    user_name="elastic"
    password="elastic"
    p=PushDataToES(host, user_name, password)    
    start_time=datetime.now()
    result=p.available_data_es()
    end_time=datetime.now()
    time_taken=end_time-start_time
    data_list={
        "result":result,
        "time_taken":time_taken
    }
    return render(request, "load.html", data_list)

def search_data_page(request):
    result = None
    search_data = ""
    try:
        if request.method == "POST":
            if request.POST.get("search_data")=="":
                return render(request, "homepage.html")
            search_data = request.POST.get("search_data") 
            if search_data:
                start_time=datetime.now()
                customer_obj = CustomerDetails("http://localhost:9200")
                result = customer_obj.search_data(search_data)  
                end_time=datetime.now()
                time_taken=end_time-start_time
    except Exception as e:
        print(f"Error during search: {e}")

    search_list = {
        "result": result,  
        "search_data": search_data,
        "time_taken":time_taken
    }
    return render(request, "search.html", search_list)




