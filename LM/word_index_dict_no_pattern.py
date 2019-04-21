import pandas as pd
import string
import enchant
import sys
from string import digits
sys.path.append("../")

from show_process import ShowProcess

lyric_data = '../data//lyrics.csv'
word_dict_file = '../data/word_index_dict_no_pattern'
START = '<s>'
END = '</s>'

d_GB = enchant.Dict("en_GB")
d_US = enchant.Dict("en_US")

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def clean(tokens):
    clean = []

    for token in tokens:
        #normalize token
        token = token.lower()
        token = token.strip(string.punctuation)

        if token != '' and (d_GB.check(token) or d_US.check(token)) and not hasNumbers(token):
            clean.append(token)

    return clean

#read the csv file and store the lyrics in lyrics_store []
csvReader = pd.read_csv(lyric_data)
csvReader = csvReader.drop(0)
lyrics_store = csvReader['lyrics']

#get the tokens in lyrics
lexicon = set()
word_index_dict = {}
process = ShowProcess(len(lyrics_store))

for line in lyrics_store:
    process.show_process()
    line = str(line)
    lexicon.update(set(clean(line.split())))

for word in lexicon:
    word_index_dict[word] = len(word_index_dict)

word_index_dict[START] = len(word_index_dict)
word_index_dict[END] = len(word_index_dict)

with open(word_dict_file, 'w+') as f:
    f.write(str(word_index_dict))
