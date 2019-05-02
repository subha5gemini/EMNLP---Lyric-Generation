# Lyric Generation
Project, Empirical Methods in NLP

Dataset: GyanendraMishra. (2016) 380,000+ Lyrics from MetroLyrics. Retrieved from https://www.kaggle.com/gyani95/380000-lyrics-from-metrolyrics

## How to run the system

First create a new file folder called data.

Then download datafiles from links listed below and save them in the data folder (be sure to login with a GU account).

https://drive.google.com/open?id=19jaO1uIUzYoGDr62HH2ZhnLuN6etCtOQ

https://drive.google.com/open?id=1I7KjGWpWZ63AeL6fLyhL5FgZaOF2Ogov

https://drive.google.com/open?id=13GwObiHAnoHX3PtRcQo6QNPEPww4xQLe

https://drive.google.com/open?id=1011t_Hy0UHg1pCwWLeBssVf4Q90zL7Tp

run the code below to generate lyrics

```python
python main.py (a topic word)
```

wait for a few minute then boom! The lyrics come out.

## How to build the system

First create a new file folder called data. Then download the lyrics dataset from the link below and save it as lyrics.csv in the data folder.

https://www.kaggle.com/gyani95/380000-lyrics-from-metrolyrics

Then download a slight modified CMU pronouncing dictionary files from the links below and save it in the data folder.
(be sure to login with a GU account)

https://drive.google.com/open?id=1GQoH-RHgjlOPJhzAvIor__duWB0Jmapu

https://drive.google.com/open?id=1MeVH6ft3ZDGu0ZwS4VWeDuaQAt7Z9u7g

Finally download the pre-trained word embedding from the link below and save it in the data folder.
(be sure to login with a GU account)

https://drive.google.com/open?id=1I7KjGWpWZ63AeL6fLyhL5FgZaOF2Ogov

run the code below to pre-process the dataset

```python
python generateData.py nd
python word_index_dict.py nd
```

then go into LM folder, run the code below to train the bigram model

```python
python bigram.py
```

or run the code below to train a LSTM model

```python
python LSTM.py
```

or train whatever language model you want

then go into rhyme folder, run the code below to process the rhyming dictionary

```python
python processing.py
```

finally go back to the main directory and run the code below to generate lyrics 
(need to modify main.py a little if want to use other language model)

```python
python main.py (a topic word)
```
