#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 16:34:27 2023

@author: Egan Beauvais, Brendan Wernisch 
"""
import xlwings as xw
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#######################
# USER INPUTS
#######################
plt.rcParams.update({'font.size': 17})
plt.rcParams["font.family"] = "Times New Roman"
bw = .1  # bandwidth of plots
colors = ['xkcd:green', 'xkcd:red', 'xkcd:blue']
labels = ['0%', '10%', '20%']

alp = .3
ticklength = 5
var_pad = 10
var_binwidth = .1

wb = xw.Book(r'TRP_Corrected-DensityData-PythonFormatted.xlsx')
sheet = wb.sheets['Sheet1']

x_min = 0     # Set minimum x-axis value (None for default)
x_max = 16    # Set maximum x-axis value (None for default)
y_min = 0     # Set minimum y-axis value (None for default)
y_max = 250  # Set maximum y-axis value (None for default); note to self: 250 for inset, 1330 for TRP

boxPlot_yMin = 0
boxPlot_yMax = 9

PlotHistograms = True
PlotBoxPlots = False

material = "TRP"    # for the purpose of plot titles

######################
# END USER INPUTS
######################

# Read data from columns
data_col1 = sheet.range("B2:B1000001").value
data_col1 = [item for item in data_col1 if item is not None]

data_col2 = sheet.range("C2:C1000001").value
data_col2 = [item for item in data_col2 if item is not None]

data_col3 = sheet.range("D2:D1000001").value
data_col3 = [item for item in data_col3 if item is not None]

# data_col4 = sheet.range("E2:E1000001").value
# data_col4 = [item for item in data_col4 if item is not None]

# data_col5 = sheet.range("F2:F1000001").value
# data_col5 = [item for item in data_col5 if item is not None]

# data_col6 = sheet.range("G2:G1000001").value
# data_col6 = [item for item in data_col6 if item is not None]

data_col7 = sheet.range("H2:H1000001").value
data_col7 = [item for item in data_col7 if item is not None]

data_col8 = sheet.range("I2:I1000001").value
data_col8 = [item for item in data_col8 if item is not None]

data_col9 = sheet.range("J2:J1000001").value
data_col9 = [item for item in data_col9 if item is not None]

#Plot histograms
if PlotHistograms == True: 
    sns.histplot(data_col1, color=colors[0], bins='auto', label=labels[0], multiple='layer', fill=True, element="step", binwidth = var_binwidth, alpha=alp, stat='count')
    sns.histplot(data_col2, color=colors[1], bins='auto', label=labels[1], multiple='layer', fill=True, element="step", binwidth = var_binwidth, alpha=alp, stat='count')
    sns.histplot(data_col3, color=colors[2], bins='auto', label=labels[2], multiple='layer', fill=True, element="step", binwidth = var_binwidth, alpha=alp, stat='count')
    plt.title(str(material) + ' at 100K')
    plt.legend(title='Percent Elongation')
    plt.xlabel('')
    plt.ylabel('')
    if x_min is not None or x_max is not None:
        plt.xlim(x_min, x_max)
    if y_min is not None or y_max is not None:
        plt.ylim(y_min, y_max)
    plt.tick_params(axis ='both', length = ticklength, direction = 'in', pad = var_pad)
    plt.show()
    plt.clf()

    #sns.histplot(data_col4, color=colors[0], bins='auto', label=labels[0], multiple='layer', fill=True, element="step", binwidth = var_binwidth, alpha=alp, stat='count')
    #sns.histplot(data_col5, color=colors[1], bins='auto', label=labels[1], multiple='layer', fill=True, element="step", binwidth = var_binwidth, alpha=alp, stat='count')
    #sns.histplot(data_col6, color=colors[2], bins='auto', label=labels[2], multiple='layer', fill=True, element="step", binwidth = var_binwidth, alpha=alp, stat='count')
    plt.title(str(material) + ' at 300K')
    plt.legend(title='Percent Elongation')
    plt.xlabel('')
    plt.ylabel('')
    if x_min is not None or x_max is not None:
        plt.xlim(x_min, x_max)
    if y_min is not None or y_max is not None:
        plt.ylim(y_min, y_max)
    plt.tick_params(axis ='both', length = ticklength, direction = 'in', pad = var_pad)
    plt.show()
    plt.clf()
    
    sns.histplot(data_col7, color=colors[0], bins='auto', label=labels[0], multiple='layer', fill=True, element="step", binwidth = var_binwidth, alpha=alp, stat='count')
    sns.histplot(data_col8, color=colors[1], bins='auto', label=labels[1], multiple='layer', fill=True, element="step", binwidth = var_binwidth, alpha=alp, stat='count')
    sns.histplot(data_col9, color=colors[2], bins='auto', label=labels[2], multiple='layer', fill=True, element="step", binwidth = var_binwidth, alpha=alp, stat='count')
    plt.title(str(material) + ' at 500K')
    
    # plt.legend(title='Percent Elongation')
    plt.xlabel('')
    plt.ylabel('')
    if x_min is not None or x_max is not None:
        plt.xlim(x_min, x_max)
    if y_min is not None or y_max is not None:
        plt.ylim(y_min, y_max)
    plt.tick_params(axis ='both', length = ticklength, direction = 'in', pad = var_pad)
    plt.show()
    plt.clf()
    

# Create box and whisker plots
if PlotBoxPlots == True:
    data_cols = [
                [data_col1, data_col2, data_col3], 
                #[data_col4, data_col5, data_col6],
                [data_col7]
                 #data_col8, data_col9]
                ]
    #data_labels = labels[:len(data_cols)]
    
    for i, col in enumerate(data_cols):
        plt.boxplot(col, patch_artist=True, boxprops=dict(facecolor='white', color='black'), whiskerprops=dict(color='black'), medianprops=dict(color='black'), capprops=dict(color='black'), showfliers=False)
        
        temps = [100,300,500]
        plt.title(str(material) + ' : Box and Whisker Plot of ' + str(temps[i]) + "K")
        
        elongation = ["0%", "10%", "20%"]
        plt.xticks([1, 2, 3], elongation)
        
        plt.xlabel("% Elongation")
        plt.ylabel('Cavity Diameter [nm]')
        
        plt.tick_params(axis='both', length=ticklength, direction='in', pad=var_pad)
        plt.ylim(boxPlot_yMin, boxPlot_yMax)
        
        plt.show()
        
        plt.clf()
