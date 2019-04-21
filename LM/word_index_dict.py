import pandas as pd

lyric_data = '../data/lyrics.csv'
word_dict_file = '../data/word_index_dict'
START = '<s>'
END = '</s>'

def clean(tokens):
    clean = []

    for token in tokens:
        #normalize token
        token = token.lower()
        clean.append(token)
        #drop stop words

    return clean

#read the csv file and store the lyrics in lyrics_store []
csvReader = pd.read_csv(lyric_data)
csvReader = csvReader.drop(0)
lyrics_store = csvReader['lyrics']

#get the tokens in lyrics
lexicon = set()
word_index_dict = {}

for line in lyrics_store:
    line = str(line)
    lexicon.update(set(clean(line.split())))

for word in lexicon:
    word_index_dict[word] = len(word_index_dict)

word_index_dict[START] = len(word_index_dict)
word_index_dict[END] = len(word_index_dict)

with open(word_dict_file, 'w+') as f:
    f.write(str(word_index_dict))
