import os 
import pickle 
import numpy as np
from celery import Celery
from celery.result import AsyncResult
import sklearn
from sklearn.metrics import r2_score
import tensorflow 
from tensorflow import keras


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Celery configuration
CELERY_BROKER_URL = 'pyamqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
# Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


def load_model():
    global X_val
    global y_val 
    # ScikitLearn model config
    model_path = 'model.pkl'

    # TF model config
    # model_path = './model.h5'
    # model_json = './model.json'

    # Test data path
    data_path = './test.csv' 

    # Read file from csv file 
    test_data = np.loadtxt(data_path, delimiter=',')
    
    X_val = test_data[:,:-1]
    y_val = test_data[:,-1]

    try: 
        # Tensorflow model
        json_file = open(model_json, "r")
        model = keras.models.model_from_json(json_file.read())
        model.load_weights(model_path)
    except:
        # Sklearn model 
        with open(model_path, 'rb') as mdl:
            model = pickle.load(mdl)
    return model

@celery.task
def add_nums(a, b):
   return a + b

@celery.task
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

@celery.task
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

