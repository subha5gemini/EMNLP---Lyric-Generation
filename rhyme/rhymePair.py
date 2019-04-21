import pickle

word2stress, word2phonemes, word2rhyme, rhyme2words, phonemes2type = pickle.load(open('./data/rhyme', 'rb'))

def generate_pairs(words, num):
    rhyme_class = {}
    rhyme_pairs = []
    used_words = set()
    selected_pairs = []

    for word in words:
        if word[0].upper() in word2rhyme:
            if word2rhyme[word[0].upper()] in rhyme_class:
                rhyme_class[word2rhyme[word[0].upper()]].append(word)
            else:
                rhyme_class[word2rhyme[word[0].upper()]] = [word]

    for key, word_set in rhyme_class.items():
        if len(word_set) == 1:
            continue
        else:
            for i in range(len(word_set) - 1):
                for j in range(1, len(word_set)):
                    if word_set[i][0].lower() != word_set[j][0].lower():
                        rhyme_pairs.append((word_set[i][0], word_set[j][0], word_set[i][1] + word_set[j][1]))

    rhyme_pairs.sort(key = lambda x: x[2], reverse = True)

    for pair in rhyme_pairs:
        if pair[0] not in used_words and pair[1] not in used_words:
            selected_pairs.append((pair[0].lower(), pair[1].lower()))
            used_words.update(set([pair[0], pair[1]]))

            if len(selected_pairs) == num:
                break

    return selected_pairs
