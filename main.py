import sys
sys.path.extend(['./GenerateWords', './LM', './rhyme', './lib'])

from GenerateCloseWords import related_word
from bigram import generate
from rhymePair import generate_pairs

if __name__ == '__main__':
    topic = sys.argv[1]
    words = related_word(topic, 1000)
    pairs = generate_pairs(words, 30)

    print(pairs)
