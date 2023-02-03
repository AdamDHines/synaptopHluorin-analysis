# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 12:58:40 2023

@author: uqahine4
"""

"user set the parent folder directory for analysis"
import tkinter
import tkinter.filedialog as fd
import os

root = tkinter.Tk()
root.withdraw()

currdir = os.getcwd()
tempdir = fd.askdirectory(parent=root, initialdir=currdir, title='Please select folder')

"search selected folder for sub-directories containing .csv files"
import pandas as pd
import statistics
import math
from pathlib import Path
import numpy as np
from numpy import trapz
from sklearn.cluster import KMeans
import statistics

list_subfolders = [f.name for f in os.scandir(tempdir) if f.is_dir()]
file = 'Results.csv'

"load and store area and activity data for each file"
areas = []
activity = []
for i in list_subfolders:
    fulldir = os.path.join(tempdir,i,file)
    path = Path(fulldir)
    "if file exists, load data"
    if path.is_file():
        df = pd.read_csv(fulldir)
        "determine number of columns for area dataset"
        endcolarea = len(df.axes[1])-4
        numcolsarea = list(range(1,endcolarea,5))
        "output area data for file"
        temparea = df.iloc[1,numcolsarea]
        temparea = temparea.reset_index(drop=True)
        areas.append(temparea)
        "determine number of columns for activity dataset"
        endcolactivity = len(df.axes[1])-3
        numcolsactivity = list(range(2,endcolactivity,5))
        activityrows = list(range(0,len(df.axes[0]),1))
        "output activity data for file"
        tempactivity = df.iloc[activityrows,numcolsactivity]
        collength = list(range(0,len(tempactivity.axes[1]),1))
        temprename = tempactivity.set_axis(collength, axis=1, inplace=False)
        activity.append(temprename)
        
"calculate area clusters and sort results based on centroid sizes"
"define appendable variables"
average_areas = []
std_areas = []
lowarea = []
medarea = []
higharea = []
"perform k-means clustering on area"
all_area = pd.concat(areas,axis=1)
all_area_singcolumn = all_area.stack()
listareas = all_area_singcolumn.tolist()
kmeans = KMeans(n_clusters=3)
kmeanfit = kmeans.fit(np.reshape(listareas,(len(all_area_singcolumn),1)))
centroids = kmeans.cluster_centers_
centroids = sorted(centroids)
for i in areas:
    average_areas.append(sum(i)/len(i))
    std_areas.append(statistics.stdev(i))
    lowarea.append(i.loc[lambda x : (x < float(centroids[0]))])
    tempmed = i.loc[lambda x : (x > float(centroids[0]))]
    medarea.append(tempmed.loc[lambda x : (x < float(centroids[1]))])
    higharea.append(i.loc[lambda x : (x>= float(centroids[1]))])
"output index values for low area data"
lowindex = []
for i in lowarea:
    tempindex = i.index[:].tolist()
    lowindex.append(tempindex)
"output index values for medium area data"
medindex = []
for i in medarea:
    tempindex = i.index[:]
    medindex.append(tempindex)
"output index values for high area data"
highindex = []
for i in higharea:
    tempindex = i.index[:]
    highindex.append(tempindex)
"calculate basic row statistics for area data"
sem_areas = []
for i in std_areas:
    sem_areas.append(i/math.sqrt(len(std_areas)))

"analyse activity data"
"define appendable variables"
average_activity = []
std_activity = []
low_activity = []
med_activity = []
high_activity = []
"sort results by average, low, medium, and high"
for i, idx in enumerate(activity):
    average_activity.append(idx.sum(axis=1)/len(idx.columns))
    std_activity.append(idx.std(axis=1))
    low_activity.append(idx[lowindex[i]])
    med_activity.append(idx[medindex[i]])
    high_activity.append(idx[highindex[i]])

"calculate relative activity for activity traces"    