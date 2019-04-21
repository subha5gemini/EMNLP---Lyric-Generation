from gensim.scripts.glove2word2vec import glove2word2vec
import gensim.models.keyedvectors as Word2Vec

EMBEDDINGS = "./data/GoogleNews-vectors-negative300.bin"
model = Word2Vec.KeyedVectors.load_word2vec_format(EMBEDDINGS.strip(), binary=True)

def related_word(word, num):
    words = model.most_similar(word, topn = (num))
    return words.append((word, 1.0))
