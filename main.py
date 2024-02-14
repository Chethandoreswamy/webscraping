import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import time


# URL of the website to scrape
url = "https://food.grab.com/sg/en/cuisines/promos-delivery/10566"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def make_request(url):
    zyte_apikey = 'b07fc9a220df487c8aa8754099836b94'
    proxy_url = 'proxy.zyte.com:8011'
    return requests.get(
    url,
    proxies={
                "http": "http://{}:@{}".format(zyte_apikey, proxy_url),
    },
    headers=headers,
    )

# Send an HTTP GET request to the website
response = make_request(url)

df = pd.DataFrame(columns=['Resutorant ID','Name', 'Cuisine','Rating','Time','Distance','offers','image','Promo'])

# Parse the HTML code using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

for row in soup.select('div.ant-col-24.RestaurantListCol___1FZ8V.ant-col-md-12.ant-col-lg-6'):
    
    try:
        name = row.find("h2").text

        cuisine = row.find("div", class_="basicInfoRow___UZM8d cuisine___T2tCh").text
    
        rating = row.findAll("div",class_="numbersChild___2qKMV")[0].text
        
        time_and_dist = row.findAll("div",class_="numbersChild___2qKMV")[1].text
        
        pattern = r'\b\d+\s*mins\b'
        match = re.search(pattern, time_and_dist)

        if match:
            time_taken = match.group()
        else:
            time_taken = "Time is not mentioned"

        
        pattern = r'\b\d+(?:\.\d+)? km\b'
        match = re.search(pattern, time_and_dist)

        if match:
            distance = match.group()
        else:
            distance = "No distance is mentioned"
        

        offers = row.find("span",class_="discountText___GQCkj").text

        image = row.find('img').get('alt')
        
        promo_tag = row.find('div', class_='promoTag___IYhfm').find('div',class_='promoTagHead___1bjRG')

        # Check if the div tag with class "row" is present
        if promo_tag:
            promo = True
        else:
            promo = False

        a_tag = row.find('a')
        href_value = ""

# Extract the value of the href attribute
        if a_tag:
            href_value = a_tag.get('href').split('/')[-1][:-1]
            
        else:
            print("Anchor tag not found")


    except:
        print("Data is not present")


    print(name,cuisine,rating,offers,distance,time_taken,image,promo,href_value)

        # Store the information in a pandas dataframe

    # Add a delay between requests to avoid overwhelming the website with requests
    df = df._append({'Resutorant ID':href_value,'Name': name, 'Cuisine': cuisine,'Rating':rating,'Time':time_taken,'Distance':distance,'offers':offers,'image':image,'Promo':promo},ignore_index=True)

df.to_csv('data.csv', index=True)


time.sleep(1)