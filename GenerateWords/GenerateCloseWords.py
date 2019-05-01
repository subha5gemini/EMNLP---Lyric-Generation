from gensim.scripts.glove2word2vec import glove2word2vec
import gensim.models.keyedvectors as Word2Vec
import sys

EMBEDDINGS = "./data/GoogleNews-vectors-negative300.bin"
model = Word2Vec.KeyedVectors.load_word2vec_format(EMBEDDINGS.strip(), binary=True)

def related_word(word, num):
    words = model.most_similar(word, topn = (num))
    words.append((word, 1.0))
    return words

if __name__ == '__main__':
    print(related_word(sys.argv[1], 10));
