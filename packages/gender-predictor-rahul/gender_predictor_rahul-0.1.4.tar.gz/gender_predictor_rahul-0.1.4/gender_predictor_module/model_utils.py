# gender_predictor_module/model_utils.py

import pickle
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

def load_resources():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(BASE_DIR, "tokenizer.pkl"), 'rb') as f:
        tokenizer = pickle.load(f)

    model = load_model(os.path.join(BASE_DIR, "gender_predictor.keras"))
    return tokenizer, model

def predict_gender(name):
    tokenizer, model = load_resources()
    input_length = 15  # Ensure this matches training
    name_seq = tokenizer.texts_to_sequences([name])
    padded = pad_sequences(name_seq, maxlen=input_length)
    pred = model.predict(padded)[0][0]
    return 'Male' if pred >= 0.5 else 'Female'
