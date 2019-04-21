import pandas as pd
import string
import enchant
import sys
from pattern.en import lemma
sys.path.append('../lib')

from show_process import ShowProcess

lyric_csv = './data/lyrics.csv'
lyric_data = './data/lyrics.data'
lyric_nd = './data/lyrics.nd'
lyric_pattern = './data/lyric.pattern'

d_GB = enchant.Dict("en_GB")
d_US = enchant.Dict("en_US")

def clean(tokens):
    clean = []

    for token in tokens:
        #normalize token
        token = token.lower()
        token = token.strip(string.punctuation)

        if token != '' and (d_GB.check(token) or d_US.check(token)):
            clean.append(token)

    return clean.join(' ') + '\n'

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def clean_no_digit(tokens):
    clean = []

    for token in tokens:
        #normalize token
        token = token.lower()
        token = token.strip(string.punctuation)

        if token != '' and (d_GB.check(token) or d_US.check(token)) and not hasNumbers(token):
            clean.append(token)

    return clean.join(' ') + '\n'

def clean_pattern(tokens):
    clean = []

    for token in tokens:
        #normalize token
        token = token.lower()
        token = token.strip(string.punctuation)

        if token != '' and (d_GB.check(token) or d_US.check(token)) and not hasNumbers(token):
            token = lemma(token)
            clean.append(token)

    return clean.join(' ') + '\n'

#read the csv file and store the lyrics in lyrics_store []
csvReader = pd.read_csv(lyric_data)
csvReader = csvReader.drop(0)
lyrics_store = csvReader['lyrics']

#get the tokens in lyrics
data = ''
nd = ''
pattern = ''
process = ShowProcess(len(lyrics_store))

for line in lyrics_store:
    process.show_process()
    line = str(line)
    tokens = line.split()
    data += clean(tokens)
    nd += clean_no_digit(tokens)
    pattern += clean_pattern(tokens)

with open(lyric_data, 'w+') as f:
    f.wirte(data)

with open(lyric_nd, 'w+') as f:
    f.wirte(nd)

with open(lyric_pattern, 'w+') as f:
    f.wirte(pattern)
