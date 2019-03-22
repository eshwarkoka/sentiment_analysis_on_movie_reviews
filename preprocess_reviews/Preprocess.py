import os,nltk,string,collections,re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.probability import FreqDist

class Preprocess:

    def __init__(self):
        pass

    def pre_process(self, review):
        return self.word_tokenization(review)

    def word_tokenization(self, review):
        print("word tokenization started")
        tokens = word_tokenize(review)
        print("word tokenization completed")
        print(tokens)
        return self.punctuation_removal(tokens)

    def punctuation_removal(self, tokens):
        print("started removing punctuations")
        punc_dict = str.maketrans({ord(ch):" " for ch in string.punctuation })
        punc_free_tokens = [each_token.translate(punc_dict) for each_token in tokens if each_token.strip()]
        print("punctuations removed")
        print(punc_free_tokens)
        return self.stopwords_removal(punc_free_tokens)

    def stopwords_removal(self, tokens):
        print("started removing stopwords")
        stop_words = set(stopwords.words('english'))
        stop_words_free = []
        for each_token in tokens:
            if each_token in stop_words or any(char.isdigit() for char in each_token) or len(each_token)<3:
                continue
            stop_words_free.append(each_token.lower())
        print("stopwords removed")
        return self.stemming(stop_words_free)
        #return self.lemmatization(stop_words_free)

    def stemming(self, tokens):
        print("stemming started")
        pst = PorterStemmer()
        stemmed_tokens = [pst.stem(each_token) for each_token in tokens]
        print("stemming completed")
        return stemmed_tokens

    def lemmatization(self, tokens):
        print("lemmatization started")
        wnl = WordNetLemmatizer()
        lemmatized_tokens = [wnl.lemmatize(each_token) for each_token in tokens]
        print("lemmatization completed")
        return lemmatized_tokens
