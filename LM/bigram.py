import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
from word_index_dict import clean
import sys
sys.path.append('../lib')

from show_process import ShowProcess

START = '<s>'
END = '</s>'

def train():
    lyric_data = '../data/lyrics' + sys.argv[1]
    word_dict_file = '../data/word_index_dict' + sys.argv[1]
    bigram_prob = '../data/bigram_prob.' + sys.argv[1]

    #read the csv file and store the lyrics in lyrics_store []
    csvReader = pd.read_csv(lyric_data)
    csvReader = csvReader.drop(0)
    lyrics_store = csvReader['lyrics']

    #get the tokens in lyrics
    with open(word_dict_file, 'r') as f:
        word_index_dict = eval(f.read())

    counts = np.zeros((len(word_index_dict), len(word_index_dict)), dtype = float)
    process = ShowProcess(len(lyrics_store))

    for line in lyrics_store:
        line = str(line)
        process.show_process()
        tokens = clean(line.split())
        previous = END

        for token in reversed(tokens):
            counts[word_index_dict[previous]][word_index_dict[token]] += 1
            previous = token

        counts[word_index_dict[previous]][word_index_dict[START]] += 1

    probs = normalize(counts, norm='l1')

    with open(bigram_prob, 'w+') as f:
        f.write(str(probs))

def generate(pair, word_index_dict, probs):
    index_word_dict = {v: k for k, v in word_index_dict.items()}
    sentence = []

    for i in range(2):
        returnSTR = pair[i]
        prevWord = pair[i]
        num_words = 1

        while(True):
            wordIndex = np.random.choice(len(word_index_dict), 1, p = list(probs[word_index_dict[prevWord]]))
            word = index_word_dict[wordIndex[0]]
            returnSTR = word + ' ' + returnSTR
            num_words +=1
            prevWord = word

            if word == "<s>" or num_words == 12:
                break

        sentence.append(returnSTR)

    return sentence

if __name__ == '__main__':
    train()
