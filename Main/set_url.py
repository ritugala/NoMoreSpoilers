from bs4 import BeautifulSoup
from selenium import webdriver

def setURL(Series, Season):
    searcher = "https://www.google.dz/search?q="+Series+"%20season%20"+ Season +"%20" +"wikipedia"
    driver = webdriver.Chrome('C:/Program Files/chromedriver')
    driver.get(searcher)
    content = driver.page_source
    soup = BeautifulSoup(content, "lxml")
    #url = soup.find('a')['href']
    for a in soup.find_all('a', href=True):
        print ("Found the URL:", a['href'])
        url = a['href']
        if "https://en.wikipedia.org" in url:
            break

    return url