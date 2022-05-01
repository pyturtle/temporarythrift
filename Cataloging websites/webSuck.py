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



CHROME_OPTIONS = Options()
CHROME_OPTIONS.add_argument("--headless")
ONLY_A_TAGS = SoupStrainer("a")
DRIVER = webdriver.Chrome("python things\Cataloging websites\chromedriver.exe",options=CHROME_OPTIONS)
DELAY = 2 # seconds
# driver.get("https://www.gapcanada.ca/browse/category.do?cid=6998")

# html2 = driver.execute_script("return document.documentElement.innerHTML;")

# soup = BeautifulSoup(html2, "html.parser", parse_only = ONLY_A_TAGS)
# print (soup.prettify())




#changing dir
os.chdir(r"python things\Cataloging websites\pickle_files")

link_set = set()
external_set = set()
link_list = []
total_urls_visited = 0



with open('total_urls_visited.pkl', 'rb') as f: total_urls_visited = pickle.load(f) 
with open('link_set.pkl', 'rb') as f: link_set = pickle.load(f)
with open('link_list.pkl', 'rb') as f: link_list = pickle.load(f)
# with open('external_set.pkl', 'rb') as f: external_set = pickle.load(f)   

#setting the colour text
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED

#max amount of urls to visit
MAX_URLS = 6000
ONLY_A_TAGS = SoupStrainer("a")




def GetAllWebsiteLinks(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    

    # domain name of the URL without the protocol
    DRIVER.get(url)
    #loading the whole website
    DRIVER.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(DELAY)
    html2 = DRIVER.page_source
    domain_name = "https"+"://" + urlparse(url).netloc
    soup = BeautifulSoup(html2, "lxml", parse_only = ONLY_A_TAGS)
    # print(soup.prettify())
    #running over each a tag found in the html
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        href = urljoin(url, href)
        # print(href)
        parsed_href = urlparse(href)
        href = href.split("&",1)[0]
        href = href.split("#",1)[0]
        # remove URL GET parameters, URL fragments, etc.
        if not IsValid(href):
            # not a valid URL
            continue
        if href in external_set :
            continue
        if href in link_set:
            continue

        if "/browse" not in parsed_href.path:
            link_set.add(href)
            continue
        
        if href.endswith('jpg'):
            continue

        if domain_name not in href:
            print(f"{RED}[*] External link: {href}{RESET}")
            external_set.add(href)
            with open('external_set.pkl', 'wb') as f:
                pickle.dump(external_set, f)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        link_list.append(href)
        link_set.add(href)
        with open('link_set.pkl', 'wb') as f:
            pickle.dump(link_set, f)
        with open('link_list.pkl', 'wb') as f:
            pickle.dump(link_list, f)
        



def IsValid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)



def Crawl(url,max_urls=30):
    
    """
    ALl THE LINKS FOUND ON THE WEBSITE
    """
    
    global total_urls_visited
    total_urls_visited += 1

    



    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    GetAllWebsiteLinks(url)
    with open('total_urls_visited.pkl', 'wb') as f:
            pickle.dump(total_urls_visited, f)
    if total_urls_visited >= max_urls:
        return

    

    for i in range(total_urls_visited,max_urls):
        link = link_list[i]
        total_urls_visited += 1
        print(total_urls_visited)
        print(f"{YELLOW}[*] Crawling: {link}{RESET}")
        GetAllWebsiteLinks(link)
        with open(r'total_urls_visited.pkl', 'wb') as f:
            pickle.dump(total_urls_visited, f)
        if total_urls_visited >= max_urls:
            break




    


if __name__ == "__main__":
    Crawl("https://www.gapcanada.ca/browse/product.do?pid=819620003",MAX_URLS)
    print("[+] Total Internal links:", len(link_set))
    