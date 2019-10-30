from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from scipy.sparse import coo_matrix

class TextExtractor:
    #Function for sorting tf_idf in descending order
    def sort_coo(self, coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    def extract_topn_from_vector(self, feature_names, sorted_items, topn=10, flag=0):
        """get the feature names and tf-idf score of top n items"""

        if flag==1:
            #use only topn items from vector
            sorted_items = sorted_items[:topn]

            score_vals = []
            feature_vals = []

            # word index and corresponding tf-idf score
            for idx, score in sorted_items:
                #keep track of feature name and its corresponding score
                score_vals.append(round(score, 3))
                feature_vals.append(feature_names[idx])

            #create a dictionary of feature,score
            results= {}
            for idx in range(len(feature_vals)):
                results[feature_vals[idx]]=score_vals[idx]
            return results, feature_vals
        else:
            score_vals = []
            feature_vals = []
            # word index and corresponding tf-idf score
            for idx, score in sorted_items:
                #keep track of feature name and its corresponding score
                score_vals.append(round(score, 3))
                feature_vals.append(feature_names[idx])

            #create a dictionary of feature,score
            results= {}
            for idx in range(len(feature_vals)):
                results[feature_vals[idx]]=score_vals[idx]
            return results, feature_vals

    def text_extractor(self, text):
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

        from sklearn.feature_extraction.text import CountVectorizer
        import re
        cv=CountVectorizer(max_df=0.8,stop_words=stop_words, max_features=10000, ngram_range=(1,3))
        X=cv.fit_transform(stemmed)

        #keyword extraction
        from sklearn.feature_extraction.text import TfidfTransformer

        tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
        tfidf_transformer.fit(X)

        feature_names=cv.get_feature_names()
        doc= " ".join(stemmed)
        tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))

        sorted_items=self.sort_coo(tf_idf_vector.tocoo())
        #extract only the top n and set flag to 1, default flag is 0---will pick ALL possible keywords
        keywords_with_scores, keywords = self.extract_topn_from_vector(feature_names, sorted_items)
        return keywords
