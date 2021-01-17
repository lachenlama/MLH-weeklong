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

time.sleep(3)
item_searched = driver.find_element_by_id('twotabsearchtextbox')
search_item = input("Enter item name to search: ")
item_searched.send_keys(search_item)
item_searched.send_keys(Keys.ENTER)

soup = bs4.BeautifulSoup(driver.page_source, 'html5lib')

links = []
for link in soup.find_all('a', attrs={'class':'a-link-normal a-text-normal'})[:5]:
    links.append(link.get('href'))

name = []
price = []
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
        deal_price = nostarchsoup.find('span', attrs={'id':'priceblock_dealprice'}).string.strip()
    except AttributeError:
        try:
            deal_price = nostarchsoup.find('span', attrs={'id':'priceblock_ourprice'}).string.strip()
        except:
            deal_price = ""
    converted_price = deal_price[2:]
    price.append(converted_price)

df = pd.DataFrame({'Product_name':name, 'Price':price})
df.to_csv('data.csv', encoding='utf-8')
