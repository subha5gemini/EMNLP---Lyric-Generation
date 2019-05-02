import numpy as np
from sklearn.preprocessing import normalize
from scipy import sparse
import sys
sys.path.append('../lib')

from show_process import ShowProcess

START = '<s>'
END = '</s>'

def train():
    lyric_data = '../data/lyrics.nd'# + sys.argv[1]
    word_dict_file = '../data/word_index_dict.nd'# + sys.argv[1]
    bigram_count = '../data/bigram_count.nd'# + sys.argv[1]
    bigram_prob = '../data/bigram_prob.nd'# + sys.argv[1]

    try:
        sparse_counts = sparse.load_npz(bigram_count)
    except Exception as e:
        with open(lyric_data, 'r') as f:
            lyrics_store = f.readlines()

        #get the tokens in lyrics
        with open(word_dict_file, 'r') as f:
            word_index_dict = eval(f.read())

        counts = np.zeros((len(word_index_dict), len(word_index_dict)), dtype = float)
        process = ShowProcess(len(lyrics_store))

        for line in lyrics_store:
            tokens = line.rstrip().split()
            process.show_process()
            previous = END

            for token in reversed(tokens):
                counts[word_index_dict[previous]][word_index_dict[token]] += 1
                previous = token

            counts[word_index_dict[previous]][word_index_dict[START]] += 1

        sparse_counts = sparse.csc_matrix(counts)
    finally:
        probs = normalize(sparse_counts, norm = 'l1', copy = False)
        sparse.save_npz(bigram_prob + '.npz', probs)

def generate(pair, word_index_dict, probs):
    index_word_dict = {v: k for k, v in word_index_dict.items()}
    sentence = []

    for i in range(2):
        returnSTR = pair[i]
        prevWord = pair[i]
        num_words = 1

        while(True):
            if prevWord not in word_index_dict:
                wordIndex = np.random.choice(len(word_index_dict), 1)
            else:
                wordIndex = np.random.choice(len(word_index_dict), 1, p = probs[word_index_dict[prevWord]].tolist()[0])

            word = index_word_dict[wordIndex[0]]
            num_words += 1
            prevWord = word

            if word == "<s>":
                break

            returnSTR = word + ' ' + returnSTR

            if num_words == 12:
                break

        sentence.append(returnSTR)

    return sentence

if __name__ == '__main__':
    train()
