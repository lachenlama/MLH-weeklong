'''
    Presented to Major League hackathon by Swaroop Raj Lama.
    The code is submitted under the week-long challenge of MLH-Build.
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import bs4,time


URL = 'https://www.amazon.in/'
PATH = 'C:\Windows\chromedriver'

chromeoptions = webdriver.ChromeOptions()
chromeoptions.add_argument('--incognito')
driver = webdriver.Chrome(PATH, chrome_options=chromeoptions)
driver.get(URL)
driver.minimize_window()

time.sleep(3)
item_searched = driver.find_element_by_id('twotabsearchtextbox')
print()
search_item = input("Enter item name to search: ")
item_searched.send_keys(search_item)
item_searched.send_keys(Keys.ENTER)
print("Please wait...")

soup = bs4.BeautifulSoup(driver.page_source, 'html5lib')

links = []
for link in soup.find_all('a', attrs={'class':'a-link-normal a-text-normal'})[:21]:
    links.append(link.get('href'))

name = []
price = []
ratings = []
df = pd.DataFrame()
for link in links:
    
    link_page = driver.get(URL + link)
    nostarchsoup = bs4.BeautifulSoup(driver.page_source, 'html5lib')

    try:
        title = nostarchsoup.find('span', attrs={'id':'productTitle'}).string.strip()
    except AttributeError:
        title = ""
    name.append(title)

    try:
        item_price = nostarchsoup.find('span', attrs={'id':'priceblock_dealprice'}).string.strip()
    except AttributeError:
        try:
            item_price = nostarchsoup.find('span', attrs={'id':'priceblock_ourprice'}).string.strip()
        except:
            item_price = ""
    converted_price = item_price[2:]
    price.append(converted_price)

    try:
        rating = nostarchsoup.find('i', attrs={'class':'a-icon a-icon-star a-star-4-5'}).sting.strip()
    except AttributeError:
        try:
            rating = nostarchsoup.find('span', attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ''
    ratings.append(rating)

    print('%%%')
    print('Downloading data...')

df = pd.DataFrame({'Product_name':name, 'Price':price, 'Rating':ratings})
df.to_csv('data.csv', encoding='utf-8')