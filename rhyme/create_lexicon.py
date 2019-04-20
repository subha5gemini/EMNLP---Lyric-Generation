import pandas as pd
from nltk.corpus import stopwords
import string
import enchant


def clean(tokens):
    stop_words = set(stopwords.words('english'))
    clean = []
    d_GB = enchant.Dict("en_GB")
    d_US = enchant.Dict("en_US")
    for token in tokens:
        #normalize token
        token = token.lower()
        #drop stop words
        if token not in stop_words and token not in string.punctuation:
            if d_GB.check(token) or d_US.check(token):
                clean.append(token)
    print("end")
    return clean







#read the csv file and store the lyrics in lyrics_store []
csvReader = pd.read_csv('lyrics.csv')
csvReader = csvReader.drop(0)
lyrics_store = csvReader['lyrics']

#get the tokens in lyrics
lexicon = []
for line in lyrics_store:
    line = str(line)
    lexicon.extend(line.split())
lexicon = clean(lexicon)
print("end")
with open("lexicon.txt", 'w') as f:
    for word in lexicon:
        f.write(word)
        f.write(" ")
print("end")
