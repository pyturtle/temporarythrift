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



chrome_options = Options()
chrome_options.add_argument("--headless")
only_a_tags = SoupStrainer("a")
driver = webdriver.Chrome("python things\Cataloging websites\chromedriver.exe",options=chrome_options)
os.chdir("python things\Cataloging websites\pickle_files")
delay = 3 # seconds
# driver.get("https://www.gapcanada.ca/browse/category.do?cid=6998")

# html2 = driver.execute_script("return document.documentElement.innerHTML;")

# soup = BeautifulSoup(html2, "html.parser", parse_only = only_a_tags)
# print (soup.prettify())




        


#
link_set = set()
external_set = set()
total_urls_visited = 0
product_list = []



with open('link_list.pkl', 'rb') as f: link_list = pickle.load(f)
# with open('external_set.pkl', 'rb') as f: external_set = pickle.load(f)   

print(len(link_list))


for link in link_list:
    if "/product" in link:
        product_list.append(link)
        print(link)



print(len(product_list))




with open('product_list.pkl', 'wb') as f:
            pickle.dump(product_list, f)