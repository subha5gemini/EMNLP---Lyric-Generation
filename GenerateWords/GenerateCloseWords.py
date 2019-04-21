from gensim.scripts.glove2word2vec import glove2word2vec
import gensim.models.keyedvectors as Word2Vec
EMBEDDINGS = "/Users/yl947/Documents/glove/GoogleNews-vectors-negative300.bin"
model = Word2Vec.KeyedVectors.load_word2vec_format(EMBEDDINGS.strip(), binary=True)
words = model.most_similar("king", topn=(10))
print(words)

    
