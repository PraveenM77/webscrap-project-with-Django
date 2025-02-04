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
    time_result=None
    error_msg=None
    result=None
      
    try:
        p=PushDataToES(host, user_name, password)
        if not p.es.ping():
            raise Exception("Server is not serviceable. Please try again later")
        start_time=datetime.now()
        result=p.available_data_es()
        end_time=datetime.now()
        time_result=end_time-start_time
    except Exception as e:
        error_msg=str(e)
    data_list={
        "output":result,
        "time":time_result,
        "error_msg":error_msg
    }
    return render(request, "show_data.html",data_list)


def homepage(request):
    return render(request, "homepage.html")

def load_data(request):
    host="http://localhost:9200"
    user_name="elastic"
    password="elastic"
    time_taken=None
    error_msg=None
    result=None
    try:
        p=PushDataToES(host, user_name, password)    
        if not p.es.ping():
            raise Exception("Server is not serviceable. Please try again later")
        start_time=datetime.now()
        result=p.available_data_es()
        end_time=datetime.now()
        time_taken=end_time-start_time
    except Exception as e:
        error_msg=str(e)


    data_list={
        "result":result,
        "time_taken":time_taken,
        "error_msg":error_msg
    }
    return render(request, "load.html", data_list)


def search_data_page(request):
    result=None
    search_data=""
    error_msg=None
    time_taken=None
    try:
        if request.method=="POST":
            if request.POST.get("search_data","").strip()=="":
                return render(request, "homepage.html")
            search_data=request.POST.get("search_data")
            if search_data:
                cust_obj=CustomerDetails("http://localhost:9200")
                if not cust_obj.es.ping():
                    raise Exception("Server is not serviceable. Please try again later")
                start_time=datetime.now()
                result=cust_obj.search_data(search_data)
                end_time=datetime.now()
                time_taken=end_time-start_time
    except Exception as e:
        print("Error During Search",e)
        error_msg=e
    
    search_list={   
        "result":result,
        "time_taken":time_taken,
        "error_msg":error_msg,
        "search_data":search_data
    }
    return render(request, "search.html", search_list)
    
    



