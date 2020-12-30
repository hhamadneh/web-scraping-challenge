# web-scraping-challenge


This project is to scrap data from NASA website as follows:

### The data is scrapped in Jupiter Notebook first and displayed in the notebook outputs.
### Then the file is exported as .py file
### The scrape_mars.py file is imported in app.py which has 3 branches:
  * root / which displays the data if the mongodb contains documents.
  * /scrape to collect/scrape the data from NASA website and save to the mongodb.
  * /clear_data to remove all data
