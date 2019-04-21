import sys
sys.path.extend(['./GenerateWords', './LM', './rhyme', './lib'])

from GenerateCloseWords import related_word
from rhymePair import generate_pairs
from bigram import generate

if __name__ == '__main__':
    topic = 'love' #sys.argv[1]
    words = related_word(topic, 3000)
    pairs = generate_pairs(words, 10)

    with open('./data/word_index_dict', 'r') as f:
        word_index_dict = eval(f.read())
