import os,nltk,string,collections,re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.probability import FreqDist

class PreprocessClass:

    def __init__(self):
        pass

    def pre_process(self, review):
        return self.word_tokenization(review)

    def word_tokenization(self, review):
        tokens = word_tokenize(review)
        return self.punctuation_removal(tokens)

    def punctuation_removal(self, tokens):
        punc_dict = str.maketrans({ord(ch):" " for ch in string.punctuation})
        punc_free_tokens = [each_token.translate(punc_dict) for each_token in tokens if each_token.strip()]
        return self.stopwords_removal(punc_free_tokens)

    def stopwords_removal(self, tokens):
        stop_words = set(stopwords.words('english'))
        stop_words_free = []
        for each_token in tokens:
            for each_split in each_token.split():
                if each_split.lower() in stop_words or any(char.isdigit() for char in each_split) or len(each_split.strip()) < 4:
                    continue
                stop_words_free.append(each_split.lower().strip())
        #return self.stemming(stop_words_free)
        return self.lemmatization(stop_words_free)

    def stemming(self, tokens):
        pst = PorterStemmer()
        stemmed_tokens = [pst.stem(each_token) for each_token in tokens]
        stemmed_tokens_str = " ".join(stemmed_tokens)
        return stemmed_tokens_str

    def lemmatization(self, tokens):
        wnl = WordNetLemmatizer()
        lemmatized_tokens = [wnl.lemmatize(each_token) for each_token in tokens]
        lemmatized_tokens_str = " ".join(lemmatized_tokens)
        return lemmatized_tokens_str