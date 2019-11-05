from bs4 import BeautifulSoup
from selenium import webdriver

def charachter_extractor(Series):
    url = "https://www.google.dz/search?q="+Series+"%20"+"cast"
    driver = webdriver.Chrome('C:/Program Files/chromedriver')
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, "lxml")
    charachters = []
    for temp in soup.select("div.P2m1Af div.wfg6Pb"):
        x = temp.get_text().lower().split()
        charachters.append(x[0])





    return charachters
