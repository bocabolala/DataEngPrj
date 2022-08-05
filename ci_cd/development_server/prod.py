import pickle
import numpy as np
import pandas as pd
import tensorflow as tf

from numpy import loadtxt
from tensorflow import keras
from sklearn.metrics import r2_score 


model_path = './model.h5'

data_path = './test.csv' 



# Read file from csv file 
data_df = np.loadtxt(data_path, delimiter=',')

# print(data_df)
X_val = data_df[:,:-1]
y_val = data_df[:,-1]
y_val = y_val.flatten()
print(y_val.shape)
# print(y_val)

def load_model():
    try:
        json_file = open("TFmdl.json", "r")
        model = keras.models.model_from_json(json_file.read())
        model.load_weights("TFw.h5")
    except:
        # Sklearn model 
        with open(model_path, 'rb') as mdl:
            model = pickle.load(mdl)
    return model


def get_predictions():
    # Load model and weights
    model = load_model()
    predictions = model.predict(X_val)
    predictions.flatten()

    # Generate result dictionary
    results ={}
    results['y'] = y_val.tolist()
    results['predicted'] =[]
    for i in range(len(results['y'])):
        results['predicted'].append(predictions[i])

    # Convert float to string 
    results['y'] = [str(int(x)) for x in results['y']]
    results['predicted'] = [str(int(x)) for x in results['predicted']]

    return results

def get_accuracy():
    model = load_model()
    predictions = model.predict(X_val)
    predictions.flatten()

    results ={}
    results['y'] = y_val.tolist()
    results['predicted'] =[]
    for i in range(len(results['y'])):
        results['predicted'].append(predictions[i])
           
    return r2_score(results['y'], results['predicted'])

res = get_predictions()
acc = get_accuracy()

print(acc)
print(res)
# print(mdl_load_from_json.predict(X_val).shape)
# r2score = r2_score(mdl_load_from_json.predict(X_val), y_val)
# print(r2score)