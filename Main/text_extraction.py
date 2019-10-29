from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from rake_nltk import Rake
# from routes import url
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

driver = webdriver.Chrome('/usr/local/bin/chromedriver')

#Use this one when combining the whole app
# driver.get(url)

#debugging - hardcoded URL
driver.get("https://en.wikipedia.org/wiki/Brooklyn_Nine-Nine_(season_6)")

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

text = "".join(all_spoilers) #text itself
doc = []
doc.append(text) #list of the text, NOT USED ANYWHERE

"""TEXT CLEANING"""
#split into sentences or words
from nltk import sent_tokenize, word_tokenize
# tokens = sent_tokenize(text)
tokens = word_tokenize(text)

#convert to lower case
tokens = [w.lower() for w in tokens]

#remove punctuation
import string
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in tokens]

#remove anything thats not an alphabet
# sentences = [''.join(c for c in s if c not in string.punctuation) for s in stripped]
words = [word for word in stripped if word.isalpha()]

#removing stop words
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
words = [word for word in words if not word in stop_words]

#stemming words
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
porter = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stemmed = [lemmatizer.lemmatize(word) for word in words]
# print(stemmed[:100])

from sklearn.feature_extraction.text import CountVectorizer
import re
cv=CountVectorizer(max_df=0.8,stop_words=stop_words, max_features=10000, ngram_range=(1,3))
X=cv.fit_transform(stemmed)
# print(X) #encoded vector of entire vocabulary

# print(list(cv.vocabulary_.keys())[:10])

#keyword extraction
from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(X)

# get feature names
feature_names=cv.get_feature_names()
# fetch document for which keywords needs to be extracted
doc= " ".join(stemmed)

#generate tf-idf for the given document

tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))
#Function for sorting tf_idf in descending order
from scipy.sparse import coo_matrix
def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    #use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:

        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]

    return results
#sort the tf-idf vectors by descending order of scores
sorted_items=sort_coo(tf_idf_vector.tocoo())
#extract only the top n
keywords=extract_topn_from_vector(feature_names,sorted_items,20)

# # now print the results
# print("\nAbstract:")
# print(doc)
print("\nKeywords:")
for k in keywords:
    print(k,keywords[k])
