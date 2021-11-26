#!usr/bin/python3
# coding: utf-8
import re
import lxml
from bs4 import BeautifulSoup
import requests
import random
import csv
import json
import time


base_url = "https://en.wikipedia.org"
url = 'https://en.wikipedia.org/wiki/Category:Companies_listed_on_the_London_Stock_Exchange'
url1 = 'https://en.wikipedia.org/w/index.php?title=Category:Companies_listed_on_the_London_Stock_Exchange&pagefrom=Grafton+Group#mw-pages'
url2 = 'https://en.wikipedia.org/w/index.php?title=Category:Companies_listed_on_the_London_Stock_Exchange&pagefrom=Grafton+Group#mw-pages'

def get_request(url, query=""):
    headers = {
    'User-Agent': random.choice(
            [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
                'Mozilla/5.0 (Windows NT 10.0; Win 64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            ]
        ),
    'content-type': "text/html",
    'uule': 'w+CAIQICIHR2VybWFueQ',
    }
    payload ={
        "q":query,
        'uule': 'w+CAIQICIHR2VybWFueQ',
        "ia": "web",
    }
    response = requests.get(url, headers=headers)
    return response


def parse_html(text):
    return BeautifulSoup(text, "lxml")

def get_all_link_1(url):
    result = []
    response = get_request(url)
    soup = parse_html(response.text)
    groups_categories = soup.find_all("div", {"class": "mw-category-group"})
    for group in groups_categories:
        all_link = group.find_all("a")
        for l in all_link:
            result.append((base_url+l.get('href'), l.get_text()))
    return result

def get_website(url):
    response = get_request(url)
    soup = parse_html(response)
    table = soup.find("table", {"class": "infobox vcard"})
    if not table:
        return ""
    all_links = [i.get("href") for i in table.find_all("a", {"rel": 'nofollow', "class":"external text"}) if re.match(r".*\..*", i.get_text())]
    if len(all_links)==0:
        return None
    else:
        return all_links[0]

def get_all_link(url):

    response = get_request(url)
    soup = parse_html(response)
    all_links = [url + link.get("href") if str(link.get("href")).startswith("/") else link.get("href") for link in soup.find_all("a") if link.get("href")]
    return all_links

    
def save_as_csv(name, data):
    with open(f"{name}.csv", 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        for el in data:
            spamwriter.writerow(el)

def save_with_json(name, data):
    with open(f"{name}.json","w",encoding='utf-8') as flux_json:
        json.dump(data, flux_json,indent=4)
    

def scraper_with_google(url):
    result = []
    query = f"'annual report' and 2021 site:{url} filetype:pdf"
    response = requests.get(f"https://google.com/search?q={query}")
    soup = parse_html(response.text)
    for l in soup.find_all(href=lambda a: a and re.compile(r"^/url\?q=(?P<url>.*\.pdf).*").match(a)):
        result.append(re.match(r"^/url\?q=(?P<url>.*\.pdf).*", l.get("href")).group("url"))
    return result

def scraper_with_duckduckgo(url):
    result = []
    query = f"'annual report' and 2021 site:{url} filetype:pdf"
    response = requests.get(f"https://duckduckgo.com/?q={query}")
    print(response.url)
    soup = parse_html(response.text)
    for l in soup.find_all(href=lambda a: a and re.compile(r"(?P<url>.*\.pdf).*").match(a)):
        result.append(re.match(r"(?P<url>.*\.pdf).*", l.get("href")).group("url"))
    return result

def print_result(result):
        for i in result:
            print(f"[+] : {i}")
        
def main():
    
    results = []
    with open("website_compagnie_.csv", "r", encoding="utf-8") as f:
        for line in f:
            try:
                
                lines = line.split(";")
                lines[2]=lines[2].strip()
                print(lines[2])
                if lines[2]!="":
                    data = {
                        "name":lines[1],
                        "old_webiste": lines[2],
                        "new_website": lines[2],
                    }
                    data["annual report"] = scraper_with_google(lines[2])
                    print(data)
                    results.append(data)
                    time.sleep(100)
            except Exception as e:
                print(e)
            
    save_with_json("results", results)



if __name__ == "__main__":
    main()
    
    


