#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyspatialml import Raster
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import contextily
import geopandas
from scipy.interpolate import griddata
import rasterio
from copy import deepcopy
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.utils import resample
import shap
import time
from matplotlib import pyplot as plt
plt.style.use('seaborn-dark')
import random


# In[2]:


pop_df_warsaw = pd.read_csv("pop_df_warsaw.csv")
df = pd.read_csv("dane.csv")
pop_df_warsaw = geopandas.GeoDataFrame(pop_df_warsaw, geometry=geopandas.points_from_xy(pop_df_warsaw.SHAPE_Leng, pop_df_warsaw.SHAPE_Area), crs='epsg:3035')
stacje = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.x, df.y), crs='epsg:4326')
ax = stacje.plot(markersize=1)
contextily.add_basemap(ax, crs=stacje.crs.to_string())
plt.show()


# In[3]:


dane = pd.read_csv("dane.csv")
y = dane.N
dane= dane[["cena", "x", "y", "liczba gwiazdek", "min_odl_trunk", 'max_odl_trunk', 'avg_odl_trunk',
       'min_odl_primary', 'max_odl_primary', 'avg_odl_primary',
       'palac_kultury', 'min_odl_stacji', 'max_odl_stacji',
       'avg_odl_stacji', 'ile_stacji_r5', 'ile_stacji_r10']]


# In[5]:


X_train, X_test, y_train, y_test = train_test_split(dane, y, test_size=0.2)


# In[8]:


import spacv
from sklearn.model_selection import cross_val_score
# Feature Scaling
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# In[17]:


from sklearn.ensemble import RandomForestRegressor

regressor = RandomForestRegressor(random_state=0)
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)


# In[18]:


from sklearn import metrics

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
mape = 100 * (abs(y_pred - y_test) / y_test)
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')


# In[24]:


# Hyperparameter tunning
from sklearn.model_selection import RandomizedSearchCV
# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
# max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}


# In[25]:


# base model
rf = RandomForestRegressor()
# Random search of parameters, using 3 fold cross validation, 
# search across 100 different combinations, and use all available cores
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, 
                               cv = 3, verbose=2, random_state=42, n_jobs = -1)
# Fit the random search model
rf_random.fit(X_train, y_train)


# In[26]:


rf_random.best_params_


# In[30]:


from sklearn.model_selection import GridSearchCV
# Create the parameter grid based on the results of random search 
param_grid={'bootstrap': [True],
             'max_depth': [30, 40, 50, 60,70],
             'max_features': ['sqrt'],
             'min_samples_leaf': [3,4,5,6,7],
             'min_samples_split': [3,4,5,6],
             'n_estimators': [1100, 1200, 1300,1400,1500,1600,1700,1800]}
    
# based model
rf = RandomForestRegressor()
# using 3 fold cross validation, 
grid_search = GridSearchCV(estimator = rf, param_grid = param_grid, 
                          cv = 3, n_jobs = -1, verbose = 2)
grid_search.fit(X_train, y_train)
grid_search.best_params_


# In[34]:


y_pred2 = grid_search.predict(X_test)

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred2))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred2))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred2)))
mape = 100 * (abs(y_pred2 - y_test) / y_test)
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')

