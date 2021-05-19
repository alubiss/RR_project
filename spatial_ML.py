#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# In[ ]:


pop_df_warsaw = pd.read_csv("pop_df_warsaw.csv")
df = pd.read_csv("dane.csv")
pop_df_warsaw = geopandas.GeoDataFrame(pop_df_warsaw, geometry=geopandas.points_from_xy(pop_df_warsaw.SHAPE_Leng, pop_df_warsaw.SHAPE_Area), crs='epsg:3035')
stacje = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.x, df.y), crs='epsg:4326')
ax = stacje.plot(markersize=1)
contextily.add_basemap(ax, crs=stacje.crs.to_string())
plt.show()

