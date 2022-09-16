import requests
from bs4 import BeautifulSoup
import json
results = []
def get_review(url):
    payload={}
    headers = {
    'Cookie': 'PHPSESSID=0g389kfme9uv277ejdnptfgjn3'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text,"lxml")
    reviews = soup.find_all("div", {"class": "review card"})
    items=[]
    for review in reviews:
        item={}
        item['user'] = review.find('p',{"class":"card-header-title"}).getText().strip()
        item['review_time'] = review.find('time',{"class":"review__time"}).getText().strip()
        item['content'] = review.find('div',{"class":"card-content"}).getText().strip()
        
        items.append(item)
    return items
        
def get_review_url(url):
    review =[]
    payload={}
    headers = {
    'Cookie': 'PHPSESSID=0g389kfme9uv277ejdnptfgjn3'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text,"lxml")
    links = soup.find_all("li", {"class": "pagination-link"})
    if len(links) ==0:
        review.extend(get_review(url))
    for link in links:
        if 'https' in link.a['href']:
            review.extend(get_review(link.a['href']))
    return review
def get_info(url):
    payload={}
    headers = {
    'Cookie': 'PHPSESSID=0g389kfme9uv277ejdnptfgjn3'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text,"lxml")
    companies = soup.find_all('div',{"class":'company-info row conpany-local'})
    
    for company in companies:
        print("---------------------------------------------------")
        result={}
        print(company.find('div',{"class":"company-name"}).h2.getText())
        result['link']=company.div.a['href']
        print('https://reviewcongty.me/'+ result['link'])
        result['name'] =company.find('div',{"class":"company-name"}).h2.getText()
        result['industry'] =company.find('div',{"class":"company-industry"}).getText().strip()
        result['info'] =company.find('div',{"class":"company-address"}).getText().strip()
        result['review'] = get_review_url('https://reviewcongty.me/'+ result['link'])
        results.append(result)


        

url = "https://reviewcongty.me/"

payload={}
headers = {
  'Cookie': 'PHPSESSID=0g389kfme9uv277ejdnptfgjn3'
}

response = requests.request("GET", url, headers=headers, data=payload)
soup = BeautifulSoup(response.text,"lxml")
links = soup.find_all("li", {"class": "pagination-link"})
page=1
for link in links:
    if 'https' in link.a['href']:
        get_info(link.a['href'])
        a_file = open(f"{page}.json", "w",encoding='utf8')
        page+=1
        json.dump(results, a_file, ensure_ascii=False)
        a_file.close()
        

