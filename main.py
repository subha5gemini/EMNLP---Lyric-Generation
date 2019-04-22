import sys
sys.path.extend(['./GenerateWords', './LM', './rhyme', './lib'])

from GenerateCloseWords import related_word
from rhymePair import generate_pairs
from bigram import generate
from scipy import sparse

if __name__ == '__main__':
    topic = sys.argv[1]
    words = related_word(topic, 3000)
    pairs = generate_pairs(words, 10)

    with open('./data/word_index_dict', 'r') as f:
        word_index_dict = eval(f.read())

    probs = (sparse.load_npz('./data/bigram_prob.data.npz')).todense()

    for pair in pairs:
        print(generate(pair, word_index_dict, probs))
