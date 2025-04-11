# https://predictivehacks.com/how-to-build-an-autocorrect-in-python/

import pandas as pd
import numpy as np
from collections import Counter
import textdistance, re, os

class Autocorrect():
    words = None
    uniqueWords = None
    wordFrequency = None
    vocab = None
    probabilities = {}

    def __init__(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + "/dictionary.txt") as text:
            self.words = re.findall('\w+', text.read().lower())
        self.vocab = set(self.words)
        self.wordFrequency = Counter(self.words)
        total = sum(self.wordFrequency.values())
        for key in self.wordFrequency.keys():
            self.probabilities[key] = self.wordFrequency[key] / total
    
    def correct(self, text: str) -> pd.DataFrame:
        text = text.lower()
        similarities = [1 - (textdistance.Jaccard(qval=2).distance(v, text)) for v in self.wordFrequency.keys()]
        dataframe = pd.DataFrame.from_dict(self.probabilities, orient='index').reset_index()
        dataframe = dataframe.rename(columns={'index':'Word', 0:'Prob'})
        dataframe['Similarity'] = similarities
        output = dataframe.sort_values(['Similarity', 'Prob'], ascending=False).head()
        return output["Word"].values

if __name__ == "__main__":
    corrector = Autocorrect()
    print(corrector.correct("wirds")["Word"].values)