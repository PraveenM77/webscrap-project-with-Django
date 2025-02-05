# Webscrape Project with Django

**Description**: This project scrapes data from Flipkart, pushes it to PostgreSQL, and then to Elasticsearch. Using Elasticsearch, products can be searched via the search option displayed in the UI.

---

### Table of Contents:
1. Introduction
2. Installation
3. Project Folder Structure
---

### Introduction

This project scrapes product data from Flipkart, stores it in a PostgreSQL database, and then pushes the data into Elasticsearch for easy searching. It allows users to view, search, and filter products through a web interface built with Django.

Key Features:
- Scrapes data from Flipkart
- Stores scraped data in PostgreSQL
- Pushes data to Elasticsearch for fast searching
- Provides a search interface for users to find products

### Installation

Follow these steps to get the project up and running on your local machine:

###Python Installation on Mac


1. **Clone the repository** to your local machine:

    ```bash
    git clone https://github.com/username/webscrape-project-with-django.git
    ```

2. **Navigate into the project directory**:

    ```bash
    cd webscrape-project-with-django
    ```

3. **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    ```

4. **Activate the virtual environment**:

    - On Windows:

      ```bash
      venv\Scripts\activate
      ```

    - On Mac/Linux:

      ```bash
      source venv/bin/activate
      ```

5. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

6. **Configure PostgreSQL**:
    ### Windows
        - Install PostgreSQL using below link
          https://www.postgresql.org/download/windows/
    ### For Mac
        - Install PostgreSQL
          ```bash
             brew install postgresql
          ```
        - ```bash
             pip3 install psycopg2
          ```
 
8. **Intall Elasticsearch**:

   - ### On Windows
     1. Download Elasticsearch from the official site:

        ```bash
        https://www.elastic.co/downloads/elasticsearch
        ```
     2. Extract the ZIP file.
     3. Open Command Prompt and navigate to the extracted folder.
     4. Run the command:
      bin\elasticsearch.bat
      Elasticsearch will start running at http://localhost:9200/

   - ### On Mac
     1. Install Homebrew
         If you don't have Homebrew installed, install it using the following command:
   
     2. ```bash
           /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```
     3. ``` bash
             brew --version
        ```
         (After installation, verify it by running this command If Homebrew is installed, it will display the version number.

     4. ```bash
           brew tap elastic/tap
        ```
     5. ```bash
           brew install elastic/tap/elasticsearch-full
        ```
     6.To check elasticsearch status
     
        ```bash
            brew services list
        ```
    7. start elasticsearch
        ```bash
           brew services start elastic/tap/elasticsearch-full

     
     6. Verify Elasticsearch is Running. After starting Elasticsearch, open a new terminal and run
                 or
        open a browser and go to:
        ```bash
           http://localhost:9200/
        ```


9. **Start the development server**:

    ```bash
       python manage.py runserver
    ```
    project should now be running on `http://127.0.0.1:8000/`.

   ---
### Project Folder Structure

The main folder contains three subfolders: `SkinproductA`, `templates`, and `webscrap_project`.

#### 1. **SkinproductA** folder
This folder contains the following files:

- **webscrap.py**: Scrapes data from Flipkart.
- **fromWebToDatabase.py**: Pushes the scraped data to the database.
- **pushToElasticsearch.py**: Pushes the data from the database to Elasticsearch.
- **customeDetails.py**: Allows customers to enter their details and desired products. It includes a `search_data` function that searches for products in Elasticsearch.

#### 2. **templates** folder
This folder contains the following HTML files:

- **homepage.html**
- **load.html**
- **show_data.html**

#### 3. **webscrap_project** folder
This folder contains the following file:

- **views.py**: Handles the functionality of buttons for:
  - **Load Data**: Loads data.
  - **Search Data**: Searches for data.
  - **Show Data**: Displays data.
