from cgitb import html
import os 
from venv import main
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup,SoupStrainer
import colorama
import pickle
from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
import time
os.chdir(r"python things\Cataloging websites\pickle_files")
with open('cataloged_images.pkl', 'rb') as f: cataloged_images = pickle.load(f)
os.chdir(r"C:\Users\PyPit\OneDrive\Documents\CODE\python things\Cataloging websites\images")

DELAY = 2 # seconds
# driver.get("https://www.gapcanada.ca/browse/category.do?cid=6998")

# html2 = driver.execute_script("return document.documentElement.innerHTML;")

# soup = BeautifulSoup(html2, "html.parser", parse_only = ONLY_A_TAGS)
# print (soup.prettify())
for i in cataloged_images:
    try:
        for n in cataloged_images[i]["images"]:
            response = requests.get(n)
            file = open(str(cataloged_images[i]["name"]+n.rsplit('/', 1)[-1]), "wb")
            file.write(response.content)
            file.close()
    except Exception as e:
        print(e)

#changing dir



    