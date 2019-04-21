import pandas as pd
import string
import enchant
import sys
sys.path.append('./lib')

from show_process import ShowProcess

lyric_data = './data/lyrics.' + sys.argv[1]
word_dict_file = './data/word_index_dict.' + sys.argv[1]
START = '<s>'
END = '</s>'

with open(lyric_data, 'r') as f:
    lyrics = f.readlines()

lexicon = set()
word_index_dict = {}
process = ShowProcess(len(lyrics))

for line in lyrics:
    process.show_process()
    lexicon.update(set(line.rstrip().split()))

for word in lexicon:
    word_index_dict[word] = len(word_index_dict)

word_index_dict[START] = len(word_index_dict)
word_index_dict[END] = len(word_index_dict)

with open(word_dict_file, 'w+') as f:
    f.write(str(word_index_dict))
