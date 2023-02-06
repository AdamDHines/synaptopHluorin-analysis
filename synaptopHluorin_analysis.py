# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 12:58:40 2023

@author: uqahine4
"""

"search selected folder for sub-directories containing .csv files"
import pandas as pd
import statistics
import math
from pathlib import Path
import numpy as np
from sklearn.cluster import KMeans

"user set the parent folder directory for analysis"
import tkinter
import tkinter.filedialog as fd
import os

root = tkinter.Tk()
root.withdraw()

currdir = os.getcwd()
tempdir = fd.askdirectory(parent=root, initialdir=currdir, title='Please select folder')

list_subfolders = [f.name for f in os.scandir(tempdir) if f.is_dir()]
file = 'Results.csv'

def truncate_data(activity_data,index_range):
    average = []
    for idx in activity_data:
        temp_trunc = []
        for o in range(0,13):
            tempmean = [] 
            tempmean = np.nanmean(idx[0:100])
            temp_trunc.append(tempmean)
            idx.drop(rangedrop,inplace=True)
            idx.reset_index(drop=True,inplace=True)
        average.append(pd.Series(temp_trunc))
    
    return average
def mean_AUC(activity_data):
    mean_activity = np.nanmean(pd.concat(activity_data,axis=1),axis=1)
    sem_activity = np.std(activity_data,axis=0)/math.sqrt(len(activity_data))
                                                                                         
    "AUC for the truncated data"
    AUC_activity = np.trapz(pd.concat(activity_data,axis=1),axis=0)
    
    return mean_activity, sem_activity, AUC_activity

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
total_areas = [] 
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
    total_areas.append(sum(i))
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
    
"output areas for individual regions and calculate total"
lowarea_totals = []
medarea_totals = []
higharea_totals = []
for i in lowarea:
    lowarea_totals.append(np.nanmean(i))
for i in medarea:
    medarea_totals.append(np.nanmean(i))
for i in higharea:
    higharea_totals.append(np.nanmean(i))
  
"analyse activity data"
"define appendable variables"
sum_activity = [] 
sum_activity_rel = []
low_activity = [] 
med_activity = []
high_activity = []
"sort results by average, low, medium, and high"
for i, idx in enumerate(activity):
    sum_activity.append(idx.sum(axis=1))
    sum_activity_rel.append(idx.sum(axis=1)/total_areas[i])
    low_activity.append(idx[lowindex[i]].sum(axis=1)/total_areas[i])
    med_activity.append(idx[medindex[i]].sum(axis=1)/total_areas[i])
    high_activity.append(idx[highindex[i]].sum(axis=1)/total_areas[i])

"mean activity"
mean_sum_activity = np.nanmean(pd.concat(sum_activity,axis=1),axis=1)
mean_sum_activity_rel = np.nanmean(pd.concat(sum_activity_rel,axis=1),axis=1)

mean_low_activity_rel = np.nanmean(pd.concat(low_activity,axis=1),axis=1)
mean_med_activity_rel = np.nanmean(pd.concat(med_activity,axis=1),axis=1)
mean_high_activity_rel = np.nanmean(pd.concat(high_activity,axis=1),axis=1)

"truncated figures for display and analysis"
rangedrop = list(range(0,100,1))
sum_activity_temp = sum_activity
sum_activity_rel_temp = sum_activity_rel
trunc_sum_activity = truncate_data(sum_activity_temp,rangedrop)
trunc_sum_activity_rel = truncate_data(sum_activity_rel_temp,rangedrop)
trunc_low_activity_rel = truncate_data(low_activity,rangedrop)
trunc_med_activity_rel = truncate_data(med_activity,rangedrop)
trunc_high_activity_rel = truncate_data(high_activity,rangedrop)
"calculate mean and sem for activity and the AUC"
mean_sum_activity_trunc, sem_sum_activity_trunc, AUC_sum_activity_trunc = mean_AUC(trunc_sum_activity)
mean_sum_activity_rel_trunc, sem_sum_activity_rel_trunc, AUC_sum_activity_rel_trunc = mean_AUC(trunc_sum_activity_rel)
mean_low_activity_trunc, sem_low_activity_trunc, AUC_low_activity_trunc = mean_AUC(trunc_low_activity_rel)
mean_med_activity_trunc, sem_med_activity_trunc, AUC_med_activity_trunc = mean_AUC(trunc_med_activity_rel)
mean_high_activity_trunc, sem_high_activity_trunc, AUC_high_activity_trunc = mean_AUC(trunc_high_activity_rel)