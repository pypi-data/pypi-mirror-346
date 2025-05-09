import pickle
import os
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

# Get the directory of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, 'assets')

# Load tokenizer and model
with open(os.path.join(ASSET_DIR, "C:\Users\Desk0012\Downloads\gender_predictor_module\gender_predictor_module\tokenizer.pkl"), 'rb') as f:
    tokenizer = pickle.load(f)

model = load_model(os.path.join(ASSET_DIR, "C:\Users\Desk0012\Downloads\gender_predictor_module\gender_predictor_module\gender_predictor.pkl"))

input_length = 15  # Ensure this matches training

def predict_gender(name):
    name_seq = tokenizer.texts_to_sequences([name])
    padded = pad_sequences(name_seq, maxlen=input_length)
    pred = model.predict(padded)[0][0]
    return 'Male' if pred >= 0.5 else 'Female'
