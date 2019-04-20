import pandas as pd
import csv
from collections import OrderedDict, Counter

class OrderedCounter(Counter, OrderedDict):
    pass

def clean(tokens):
    clean = []
    for token in tokens:
        #normalize token
        token = token.lower()
        clean.append(token)
        #drop stop words
    print("end1")
    return clean







#read the csv file and store the lyrics in lyrics_store []
csvReader = pd.read_csv('lyrics.csv')
csvReader = csvReader.drop(0)
lyrics_store = csvReader['lyrics']

#get the tokens in lyrics
lexicon = []
for line in lyrics_store:
    line = str(line)
    lexicon.extend(line.split())
lexicon = clean(lexicon)

bigram = []

for i in range(len(lexicon) - 1):
    temp = (lexicon[i], lexicon[i + 1])
    bigram.append(temp)
count = Counter(bigram)
print("end2")

csv_list = []
csv_list.append(['Bigram', 'Frequency'])
for pair in count.most_common():
    temp = pair
    csv_list.append(temp)
print("end3")
print(csv_list)
with open('bigram.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csv_list)
csvFile.close()
print("end4")
