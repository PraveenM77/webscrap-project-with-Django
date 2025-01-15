# webscrape-project-with-Django

Description: Scrape data from Flipkart, push it to PostgreSQL, and then to Elasticsearch. Using Elasticsearch, products can be searched through the search option displayed in the UI.

The main folder contains three subfolders: SkinproductA, templates, and webscrap_project.

**1. SkinproductA folder**
This folder contains four files:

webscrap.py: This file scrapes data from Flipkart.
fromWebToDatabase.py: This file pushes the scraped data to the database.
pushToElasticsearch.py: This file pushes the data from the database to Elasticsearch.
customeDetails.py: This file allows customers to enter their details and desired products. It includes a search_data function that searches for products in Elasticsearch.

**2. templates folder**
This folder contains the HTML files:

homepage.html
load.html
show_data.html

**3. webscrap_project folder**
This folder contains a file: views.py, which handles the functionality of buttons for:

Load Data: To load data.
Search Data: To search for data.
Show Data: To display data.
