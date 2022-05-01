import requests
from bs4 import BeautifulSoup
import pickle
from urllib.parse import urlparse, urljoin
import os



os.chdir(r"python things\Cataloging websites\pickle_files")
FILENAME = 'cataloged_images.pkl'
data = {}
MAX_DATA = 2
with open('product_list.pkl', 'rb') as f: productlinks = pickle.load(f)



def main():
    for i,link in enumerate(productlinks):
        baseurl = "https"+"://" + urlparse(link).netloc
        f = requests.get(link).text
        urmom = BeautifulSoup(f, 'lxml')

        try:
            name = urmom.find("h1", {"class": "pdp-mfe-lz12c0"}).text.replace('\n', "")
        except Exception as e:
            print("Name not found")
            print(e)
            print (link)
            name = None




        images = urmom.findAll("a")
        if name in data:
            for tag in images:
                img = tag.attrs.get("href")
                if img == None:
                    continue
                if img.endswith("jpg"):
                    img = baseurl + img
                    data[name]["images"].add(img)



        try:
            price = urmom.find("span", {"class": "pdp-pricing--highlight pdp-pricing__selected pdp-mfe-19nkmoj"}).text.replace\
                ('\n', "")
        except Exception as e:
            try:
                price = urmom.find("span", {"class": "pdp-pricing__selected pdp-mfe-19nkmoj"}).text.replace\
                ('\n', "")
            except:
                print("price not found")
                print(e)
                print (link)
                price = None


        #images = [a['href'] for a in urmom.find_all('a', class_='hover-zoom hover-zoom-in pdp-mfe-1scitg2', href=True)]

        imageset = set()
        for tag in images:
            img = tag.attrs.get("href")
            if img == None:
                continue
            if img.endswith("jpg"):
                img = baseurl + img
                imageset.add(img)


        clothing = {"name": name, "price": price, "images": imageset, "link": link}

        data[name] = clothing
        print(i)
    return data

if __name__ == '__main__':
    data = main()
    with open(FILENAME, 'wb') as f:
                pickle.dump(data, f)
    print(data)
