from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from rake_nltk import Rake
# from routes import url

driver = webdriver.Chrome('/usr/local/bin/chromedriver')

#Use this one when combining the whole app
# driver.get(url)

#debugging - hardcoded URL
driver.get("https://en.wikipedia.org/wiki/Friends_(season_6)")

content = driver.page_source
soup = BeautifulSoup(content, "lxml")

summary = []
spoiler_content = soup.find('div', {'class': 'mw-parser-output'}).find_all('p')
for spoiler in spoiler_content:
    summary.append(spoiler)

summary_spoilers = []

#adding only summary paras from paras found in "mw-parser-output" class
summary_spoilers.append(summary[1].get_text())
summary_spoilers.append(summary[2].get_text())


#scraping content of each episode
episode_spoilers = []

episode_table = soup.find('table', {'class': 'wikitable plainrowheaders wikiepisodetable'}).find_all('td')
for temp in episode_table:
    episode_spoilers.append(temp.get_text())

all_spoilers = []
for i in range(len(summary_spoilers)):
    all_spoilers.append(summary_spoilers[i])
for i in range(len(episode_spoilers)):
    all_spoilers.append(episode_spoilers[i])

li = "".join(all_spoilers)
#extracting keywords
keywords = []
rake = Rake()

rake.extract_keywords_from_text(li)
spoiler_words = rake.get_ranked_phrases()
for i in range(len(spoiler_words)):
    keywords.append(spoiler_words[i])
print(keywords)

# for i in range(len(all_spoilers)):
#     text = all_spoilers[i]
#     rake.extract_keywords_from_text(text)
#     spoiler_words = rake.get_ranked_phrases()
#     # print(rake.get_ranked_phrases())
#     for i in range(len(spoiler_words)):
#         keywords.append(spoiler_words[i])
# print(keywords)

# df = pd.DataFrame({'Spoiler':main_spoilers})
# df.to_csv('spoilers.csv', index=False, encoding='utf-8')
