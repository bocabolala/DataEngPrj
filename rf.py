from sklearn.datasets import fetch_covtype
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
import pandas 
import numpy as np

covtype = fetch_covtype(download_if_missing=True, as_frame=True)
clf = RandomForestClassifier()

X_train, X_val, y_train, y_val = train_test_split(covtype.data, 
                                                    covtype.target, 
                                                    test_size=0.3, )

params_search_space = {'max_depth':[30,50,100], 
                        'n_estimators':[20,30,40],
                        'ccp_alpha':[0,0.1,0.01]}

print(clf.get_params())


clf.fit(X_train, y_train )

base_scores = metrics.accuracy_score(y_val, clf.predict(X_val))

print(clf.get_params())

print('Score on default params:',base_scores)




