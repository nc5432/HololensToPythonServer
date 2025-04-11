# https://www.geeksforgeeks.org/next-word-prediction-with-deep-learning-in-nlp/

import keras, os, pickle
from keras.src.layers import Embedding, LSTM, Dense
from keras.src.models import Sequential
from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
import numpy as np
import regex as re

class WordPrediction:
    def __init__(self):
        text_data = self.file_to_sentence_list(os.path.dirname(os.path.realpath(__file__)) + "/dictionary.txt")

        self.tokenizer = Tokenizer()
        self.tokenizer.fit_on_texts(text_data)
        self.total_words = len(self.tokenizer.word_index) + 1

        text_data = self.file_to_sentence_list(os.path.dirname(os.path.realpath(__file__)) + "/dictionary.txt")

        # Create input sequences
        self.input_sequences = []
        for line in text_data:
            token_list = self.tokenizer.texts_to_sequences([line])[0]
            for i in range(1, len(token_list)):
                n_gram_sequence = token_list[:i+1]
                self.input_sequences.append(n_gram_sequence)

        # Pad sequences and split into predictors and label
        self.max_sequence_len = max([len(seq) for seq in self.input_sequences])
        self.input_sequences = np.array(pad_sequences(self.input_sequences, maxlen=self.max_sequence_len, padding='pre'))

    def train(self, epochs: int = 50):
        X, y = self.input_sequences[:, :-1], self.input_sequences[:, -1]

        # Convert target data to one-hot encoding
        y = keras.utils.to_categorical(y, num_classes=self.total_words)

        # Define the model
        self.model: Sequential = Sequential()
        self.model.add(Embedding(self.total_words, 10, input_length=self.max_sequence_len-1))
        self.model.add(LSTM(128))
        self.model.add(Dense(self.total_words, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Train the model
        self.history = self.model.fit(X, y, epochs=epochs, verbose=1)
        self.model.save('keras_next_word_model.h5')
        pickle.dump(self.history, open("history.p", "wb"))

    def load(self):
        self.model = keras.models.load_model('keras_next_word_model.h5')
        self.history = pickle.load(open("history.p", "rb"))

    def file_to_sentence_list(self, file_path):
        with open(file_path, 'r') as file:
            text = file.read()

        # Splitting the text into sentences using
        # delimiters like '.', '?', and '!'
        sentences = [sentence.strip() for sentence in re.split(r'(?<=[.!?])\s+', text) if sentence.strip()]

        return sentences

    def predict(self, seed_text: str, wordCount: int = 3) -> list[str]:
        results = []
        token_list = self.tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=self.max_sequence_len-1, padding='pre')
        predicted_probs = self.model.predict(token_list)
        indices = np.argsort(predicted_probs)
        for i in range(wordCount):
            results.append(self.tokenizer.index_word[indices[0][-i - 1]])
        return results

if __name__ == "__main__":
    predictor = WordPrediction()
    predictor.load()
    print(predictor.predict("This is a test of "))