import requests
from bs4 import BeautifulSoup
import re
import time
import random

def get_headers():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com",
        "Accept-Encoding": "gzip, deflate"
    }
    return headers

def fetch_html_response(url,headers):
    try:
        with requests.session() as session:
            response = session.get(url,headers=headers)
            if response.status_code == 200:
                return response.text
            else:
                print("Can't connect ",response.status_code)

    except Exception as e:
        print(e)
    return None

def extract_product_links(url,headers):
    response_text = fetch_html_response(url,headers)
    if response_text:
        soup = BeautifulSoup(response_text,"lxml")
        container = soup.find("div",class_="DOjaWF gdgoEp")
        products_links = container.find_all("a",class_="wjcEIp")
        return ["http://www.flipkart.com"+product["href"] for product in products_links] if products_links else []

def get_products_name(soup):
    product_name_tag = soup.find("span",class_="VU-ZEz")
    return product_name_tag.text.strip() if product_name_tag else None

def get_product_price(soup):
    product_price_tag = soup.find("div",class_="Nx9bqj CxhGGd")
    return product_price_tag.text.replace("₹", "").replace(",", "").strip() if product_price_tag else None

def get_product_quantity(soup):
    rows=soup.find_all("tr",class_="WJdYP6 row")
    if rows:
        for row in rows:
            label=row.find("td",class_="+fFi1w col col-3-12")
            if label and label.text.strip() == "Quantity":
                quantity_td=row.find("td",class_="Izz52n col col-9-12")
                quantity=quantity_td.find("li",class_="HPETK2")
                return quantity.text.strip() or "quantity is not listed"
    return None

def get_product_brand(soup):
    product_brand_tag =  get_products_name(soup)
    if product_brand_tag:
        brand_name = re.match(r"^[\w'’\-]+(?:\s[\w'’\-]+)?", product_brand_tag)
        return brand_name.group() if brand_name else None

def get_product_highlights(soup):
    product_highlights_container=soup.find("div",class_="xFVion")
    if product_highlights_container:
        product_highlights=product_highlights_container.find_all("li")
        return [highlights.text.strip() for highlights in product_highlights] if product_highlights else []
    return []

def get_product_description(soup):
    product_description=soup.find("div",class_="yN+eNk w9jEaj")
    return product_description.text.strip() if product_description else None

def get_product_skin_type(soup):
    rows = soup.find_all("tr",class_="WJdYP6 row")
    if rows:
        for row in rows:
            label = row.find("td",class_="+fFi1w col col-3-12")
            if label and label.text.strip() == "Skin Type":
                skin_type_td = row.find("td",class_="Izz52n col col-9-12")
                if skin_type_td:
                    skin_type = skin_type_td.find("li",class_="HPETK2")
                    return skin_type.text.strip() or "Skin Type not listed"
    return "Skin Type not found"

def fetch_product_details(product_url, headers):
    response_text = fetch_html_response(product_url, headers)
    if response_text:
        soup = BeautifulSoup(response_text, "lxml")
        product_details = {
            "name": get_products_name(soup),
            "price": get_product_price(soup),
            "brand": get_product_brand(soup),
            "quantity":get_product_quantity(soup),
            "skin_type": get_product_skin_type(soup),
            "highlights": get_product_highlights(soup),
            "description": get_product_description(soup)
        }
        return product_details
    else:
        print(f"Failed to fetch product page for link: {product_url}")
    return None

def get_all_product_details():
    headers = get_headers()
    url = "https://www.flipkart.com/search?q=beauty%20products&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    product_links = extract_product_links(url, headers)
    all_product_details = []
    for product_url in product_links:
        time.sleep(random.uniform(5, 7))
        product_details = fetch_product_details(product_url, headers)
        if product_details:
            all_product_details.append(product_details)
    return all_product_details

product=get_all_product_details()
print(product)