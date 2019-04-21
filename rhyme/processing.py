import pickle
import re

word2stress = {}
word2phonemes = {}
word2rhyme = {}
phonemes2type = {}
rhyme2words = {}

with open('cmudict-0.7b.phones.txt', 'r', encoding = 'ISO-8859-1') as f:
    phonemes = f.readlines()

    for phoneme in phonemes:
        phoneme = phoneme.rstrip().split()
        phonemes2type[phoneme[0]] = phoneme[1]

with open('cmudict.txt', 'r', encoding = 'ISO-8859-1') as f:
    lines = f.readlines()
    duplicate_words = set()

    for line in lines:
        word = line.rstrip().split()[0]

        if '(' in word:
            duplicate_words.add(re.sub(r'[(][0-9]*[)]', '', word))

    for line in lines:
        line = line.rstrip().split()

        if line[0] in duplicate_words or ')' == line[0][-1]:
            continue

        word2stress[line[0]] = '';
        word2phonemes[line[0]] = []
        word2rhyme[line[0]] = ''

        for phoneme in line[1:]:
            if phoneme[-1] in '012':
                word2stress[line[0]] += '0' if phoneme[-1] == '0' else '1'

            word2phonemes[line[0]].append(phoneme.rstrip('120'))

        for phoneme in reversed(line[1:]):
            if phoneme[-1] not in '12':
                word2rhyme[line[0]] = phoneme.rstrip('0') + word2rhyme[line[0]]
            else:
                word2rhyme[line[0]] = phoneme.rstrip('12') + word2rhyme[line[0]]
                break;

for word, rhyme in word2rhyme.items():
    if rhyme in rhyme2words:
        rhyme2words[rhyme].add(word)
    else:
        rhyme2words[rhyme] = set([word])

unique_rhyme = set()

for rhyme, words in rhyme2words.items():
    if len(words) == 1:
        unique_rhyme.add(rhyme)
        del word2rhyme[list(words)[0]]

for rhyme in unique_rhyme:
    del rhyme2words[rhyme]

pickle.dump((word2stress, word2phonemes, word2rhyme, rhyme2words, phonemes2type) , open('../data/rhyme', 'wb+'))
