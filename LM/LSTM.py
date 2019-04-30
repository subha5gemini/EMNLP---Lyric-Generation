import argparse
import random

from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, TimeDistributed
from keras.callbacks import EarlyStopping
from keras import optimizers

import numpy as np
import tensorflow as tf

tf.logging.set_verbosity(tf.logging.ERROR)

args = argparse.ArgumentParser(description='Program description.')
args.add_argument('-d','--device', default='cpu', help='Either "cpu" or "cuda"')
args.add_argument('-e','--epochs', default=10, type=int, help='Number of epochs')
args.add_argument('-lr','--learning-rate', default=0.1, type=float, help='Learning rate')
args.add_argument('-do','--dropout', default=0.3, type=float, help='Dropout rate')
args.add_argument('-ea','--early-stopping', default=2, type=int, help='Early stopping criteria')
args.add_argument('-em','--embedding-size', default=100, type=int, help='Embedding dimension size')
args.add_argument('-hs','--hidden-size', default=100, type=int, help='Hidden layer size')
args.add_argument('-b','--batch-size', default=50, type=int, help='Batch Size')
args = args.parse_args()

START = '<s>'
END = '</s>'
PAD = '<pad>'

def train():
    lyric_data = '../data/lyrics.nd'# + sys.argv[1]
    word_dict_file = '../data/word_index_dict.nd'# + sys.argv[1]
    
    with open(lyric_data, 'r') as f:
        lyrics_store = f.readlines()

    with open(word_dict_file, 'r') as f:
        word2index = eval(f.read())
        word2index[PAD] = len(word2index)
        
    describe_data(lyrics_store, None, None,
          batch_generator_lm(lyrics_store, word2index, args.batch_size))

    language_model = Sequential()
    language_model.add(Embedding(len(word2index), args.embedding_size))
    language_model.add(LSTM(args.hidden_size,
                            dropout = args.dropout,
                            recurrent_dropout = args.dropout,
                            return_sequences = True))
    language_model.add(LSTM(args.hidden_size,
                            dropout = args.dropout,
                            recurrent_dropout = args.dropout,
                            return_sequences = True))
    language_model.add(TimeDistributed(Dense(len(word2index), activation = 'softmax')))
    
    adadelta = optimizers.Adadelta(clipnorm=1.0)
    language_model.compile(optimizer=adadelta, loss = 'categorical_crossentropy', metrics = ['accuracy'])
    
    # Training
    language_model.fit_generator(batch_generator_lm(lyrics_store, word2index, args.batch_size),
                                 callbacks = [EarlyStopping(monitor='acc', patience = args.early_stopping)],
                                 epochs = args.epochs, steps_per_epoch = len(lyrics_store) / args.batch_size)
    
    language_model.save("../data/lstm.h5")
    
    return language_model, word2index

def vectorize_sequence(seq, word2index):
    seq = seq.rstrip().split()
    return [word2index[tok] for tok in reversed(seq)] + [word2index[START]]

def unvectorize_sequence(seq, word2index):
    index2word = {v: k for k, v in word2index.items()}
    return [index2word[index] for index in seq]

def one_hot_encode_label(label, word2index):
    vec = [1.0 if word2index[label] == i else 0.0 for i in range(len(word2index))]
    return vec

def batch_generator_lm(data, vocab, batch_size=1):
    while True:
        batch_x = []
        batch_y = []
        
        for sent in data:
            batch_x.append(vectorize_sequence(sent, vocab))
            batch_y.append([one_hot_encode_label(token, vocab) for token in shift_by_one(sent)])
            
            if len(batch_x) >= batch_size:
                # Pad Sequences in batch to same length
                batch_x = pad_sequences(batch_x, vocab[PAD])
                batch_y = pad_sequences(batch_y, one_hot_encode_label(PAD, vocab))
                yield np.array(batch_x), np.array(batch_y)
                batch_x = []
                batch_y = []

def describe_data(data, gold_labels, label_set, generator):
    batch_x, batch_y = [], []
    
    for bx, by in generator:
        batch_x = bx
        batch_y = by
        break
    
    print('Data example:',data[0])
    print('Label:',None)
    print('Label count:', None)
    print('Batch input shape:', batch_x.shape)
    print('Batch output shape:', batch_y.shape)


def pad_sequences(batch_x, pad_value):
    ''' This function should take a batch of sequences of different lengths
        and pad them with the pad_value token so that they are all the same length.

        Assume that batch_x is a list of lists.
    '''
    pad_length = len(max(batch_x, key=lambda x: len(x)))
    
    for i, x in enumerate(batch_x):
        if len(x) < pad_length:
            batch_x[i] = x + ([pad_value] * (pad_length - len(x)))
    
    return batch_x


def generate_text(language_model, word, word2index):
    prediction = [word]
    
    while not (prediction[-1] == START or len(prediction) >= 50):
        next_token_one_hot = language_model.predict(np.array([[word2index[p] for p in prediction]]), batch_size=1)[0][-1]
        next_tokens = sorted([i for i,v in enumerate(next_token_one_hot)], 
                              key = lambda i:next_token_one_hot[i], 
                              reverse = True)[:10]
        next_token = next_tokens[random.randint(0, 9)]
        
        for w, i in word2index.items():
            if i == next_token:
                prediction.append(w)
                break
            
    return ' '.join(reversed(prediction[:-1]))

def shift_by_one(seq):
    seq = seq.rstrip().split()
    return [seq[len(seq) - x - 2] if x < len(seq) - 1 else PAD for x in range(len(seq))] + [START]

if __name__ == '__main__':
    lstm, word2index = train()
    generate_text(lstm, 'love', word2index)