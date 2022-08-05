import tensorflow as tf

from numpy import loadtxt
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout

import pandas as pd
import numpy as np

from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.metrics import r2_score 
from sklearn.model_selection import train_test_split


# Set path to model and data file 
# If use TF2 or Pytorch, include model architecture description json file(or include class here) and weight file)
# model_path = './entire_model.pth'

data_path = './data.csv' 

# Read file from csv file 
data_df = pd.read_csv(data_path)

def string_to_float(data, feature):
    l = data[feature].unique()
    l_dict = dict(zip(l, np.arange(0.0, len(l)+1)))
    return l_dict  

def preprocess(d): 
    clean_language = string_to_float(d,'language')
    clean_license = string_to_float(d,'license')
    d = d.drop(columns=['private', 'url', 'Unnamed: 0'])
    d['language'] = d['language'].apply(lambda x: clean_language[x])
    d['license'] = d['license'].apply(lambda x: clean_license[x])
    #d = d.drop(columns=['watchers'])
    
    X = d.drop(columns=['stars']).values
    y = d['stars'].values
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_val, y_train, y_val

X_train, X_val, y_train, y_val = preprocess(data_df)


np.savetxt('test.csv', np.asarray(np.hstack((X_val, y_val.reshape(-1,1))), dtype=int), delimiter=',')

def MLPRg():
    model = keras.models.Sequential()
    model.add(Dense(72, input_dim=10, activation="relu", name="layer1"))
    model.add(Dense(72, activation="relu", name="layer2"))
    model.add(Dense(36, activation="relu", name="layer3"))
    model.add(Dense(18, activation="relu", name="layer4"))
    model.add(Dense(9, activation="relu", name="layer5"))
    model.add(Dense(1, name="output"))

    model.compile(loss='mean_squared_error', optimizer='adam')

    return model


estimator = KerasRegressor(build_fn=MLPRg, epochs=1000, batch_size=200)

estimator.fit(X_train, y_train)

estimator.model.save("model.h5")

mdl_arch = MLPRg()
TFmdl_json = mdl_arch.to_json()
with open("model.json", "w") as json_file:
    json_file.write(TFmdl_json)

json_file = open("model.json", "r")
mdl_load_from_json = keras.models.model_from_json(json_file.read())
mdl_load_from_json.load_weights("model.h5")


print(type(mdl_load_from_json.predict(X_val)))
r2score = r2_score(mdl_load_from_json.predict(X_val), y_val)
print(r2score)