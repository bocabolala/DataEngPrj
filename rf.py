from sklearn.datasets import fetch_covtype
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from sklearn import metrics
from ray.tune.sklearn import TuneGridSearchCV 
import pandas 
import numpy as np

covtype = fetch_covtype(download_if_missing=True, as_frame=True)
rfclf = RandomForestClassifier()

X_train, X_test, y_train, y_test = train_test_split(covtype.data, 
                                                    covtype.target, 
                                                    test_size=0.8, )

params_search_space = {'max_depth':[30,50], 
                        'n_estimators':[20,30],
                        'ccp_alpha':[0,0.1]}

print(rfclf.get_params())

rfclf.fit(X_train, y_train )

base_scores = metrics.accuracy_score(y_test, rfclf.predict(X_test))

print('Score on default params:',base_scores)

tune_search = TuneGridSearchCV(estimator=rfclf,
								param_grid=params_search_space,
								scoring='accuracy',
                                n_jobs=-1,
                                refit=True,
                                return_train_score=True,
                                )

print(tune_search)

ts_best_score = tune_search.fit(X_train, y_train)
print('Score on tune-searched best parameters in cross-validation:', tune_search.best_score_)

print('Best parameter found:', tune_search.best_params_)

ts_best_param_test = metrics.accuracy_score(y_test, tune_search.predict(X_test))

print('Score on tune-searched best parameters in testset:', ts_best_param_test)





