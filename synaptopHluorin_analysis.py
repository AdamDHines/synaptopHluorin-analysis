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
from pathlib import Path

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
        areas.append(temparea)
        "determine number of columns for activity dataset"
        endcolactivity = len(df.axes[1])-3
        numcolsactivity = list(range(2,endcolactivity,5))
        activityrows = list(range(0,len(df.axes[0]),1))
        "output activity data for file"
        tempactivity = df.iloc[activityrows,numcolsactivity]
        activity.append(tempactivity)
        
