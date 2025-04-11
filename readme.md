## Hololens to Python Server
This is a rudimentary word prediction and autocorrect server intended for use with Michigan Technological University's holo keyboard research. The hololens sends a json file containing one item, called "words", and then text that is to be corrected or predicted. The server then checks if the user is going to start typing a new word, or is typing an incomplete one. Depending on this, it will either predict 3 future words, or it will return 3 corrected words. These get sent back to the hololens in a json format with 3 items, "word1" through "word3". 

### Installation
1. Clone the repository. You may want to set up a venv. 
2. Install requirements. This can be done with  
```pip install -r requirements.txt```
   - (Optional) If you intend to train a word prediction model, you will need to edit a bit of included module code. On line 31 of WordPrediction.py, we use pad_sequences(). This comes from the keras_preprocessing.sequence module and includes outdated numpy code. Open sequence.py, most easily accessed by right clicking on pad_sequences() in an IDE like Visual Studio or VSCode and clicking 'Go to definition;. Here, scroll to line 79 and replace np.unicode_ with np.str_.
3. Run 'Server.py'. From there, the hololens can connect on port 8968.