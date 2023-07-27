# -*- coding: utf-8 -*-

"""
Created on Tue Jul 18 16:22:17 2023

Author: Brendan Wernisch
"""

####################
# %% IMPORT PACKAGES
####################

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

#####################################
# %% USER INPUTS - Log Files and Data
#####################################

'''
Keep in this order, as the LRR slopes are called in the same orientation 
(they are actually called by 'figNumber' in the function call), but those are ordered in the same order as these
'''

log_files_PMP100 = ['DeformationLogFiles/PMP_100K_5E9.lammps', 'DeformationLogFiles/PMP_100K_25E9.lammps', 'DeformationLogFiles/PMP_100K_50E9.lammps']
log_files_PMP300 = ['DeformationLogFiles/PMP_300K_5E9.lammps', 'DeformationLogFiles/PMP_300K_25E9.lammps', 'DeformationLogFiles/PMP_300K_50E9.lammps']
log_files_PMP500 = ['DeformationLogFiles/PMP_500K_5E9.lammps', 'DeformationLogFiles/PMP_500K_25E9.lammps', 'DeformationLogFiles/PMP_500K_50E9.lammps']

log_files_PS100 = ['DeformationLogFiles/PS_100K_5E9.lammps', 'DeformationLogFiles/PS_100K_25E9.lammps', 'DeformationLogFiles/PS_100K_50E9.lammps']
log_files_PS300 = ['DeformationLogFiles/PS_300K_5E9.lammps', 'DeformationLogFiles/PS_300K_25E9.lammps', 'DeformationLogFiles/PS_300K_50E9.lammps']
log_files_PS500 = ['DeformationLogFiles/PS_500K_5E9.lammps', 'DeformationLogFiles/PS_500K_25E9.lammps', 'DeformationLogFiles/PS_500K_50E9.lammps']

log_files_TRP100 = ['DeformationLogFiles/TRP_100K_5E9.lammps', 'DeformationLogFiles/TRP_100K_25E9.lammps', 'DeformationLogFiles/TRP_100K_50E9.lammps']
log_files_TRP300 = ['DeformationLogFiles/TRP_300K_5E9.lammps', 'DeformationLogFiles/TRP_300K_25E9.lammps', 'DeformationLogFiles/TRP_300K_50E9.lammps']
log_files_TRP500 = ['DeformationLogFiles/TRP_500K_5E9.lammps', 'DeformationLogFiles/TRP_500K_25E9.lammps', 'DeformationLogFiles/TRP_500K_50E9.lammps']

#### LRR Slopes, with order provided
LRR_slopes = [
               16.66787594, 8.004734736, 2.884455028,   # PMP100, 300, 500
               14.28933875, 11.20873003, 5.875177772,   # PS100, 300, 500
               9.432204559, 7.043654722, 5.308985700      # TRP100, 300, 500
             ]

y_col = 4   # column number in LAMMPS log file for y-axis data; indexing basis is not zero. it's 1.
x_col = 5   # column number for x-axis data; same index basis

#######################################
# %% USER INPUTS - Customizable Options
#######################################

#### Initialize color list for plotting.
# In the order of 1st log file to 3rd log file on plot
# (i.e. 5E9, 25E9, and 50E9 at the time of writing)
colors = ['#004D40', '#D81B60', '#1E88E5']

#### Line options

markerSize    = 400  # for optional, additional markers
lineThickness = 400  # does not work right now
window_size   = 100  # width of smoothing function

#### Axis + label options;
x_min, x_max = 0, 20
y_min, y_max = 0, 100

x_minor_tick_interval = 10
x_major_tick_interval = 10

y_minor_tick_interval = 5
y_major_tick_interval = 20

#### Font Options
fontSize = 50
fontFamily = "Times New Roman"

####################
# %% BOOLEAN OPTIONS
####################

bool_axesLabel = False
bool_pltTitle = True

bool_additionalMarkers = True

bool_insetPlot = True


##############
# %% FUNCTIONS
##############

def calculate_strain(xData):
    '''Calculates strain (%) from elongation data.
    
    Args:
        xData (list of numpy arrays): List containing elongation data (x-axis data).
        
    Returns:
        list: List containing the calculated strain (%) for each elongation data array.
        
    Details:
        - The function takes a list of numpy arrays, representing elongation data (xData).
        - For each elongation data array, it calculates the initial length (x[0]) and applies
          the engineering strain formula to calculate the strain values for each elongation step.
        - The calculated strain values (in %) are appended to the strainData list.
        - The function returns a list containing the calculated strain (%) for each elongation data array.
    '''
    
    strainData = []  # Initialize a list for storing strain data
    
    for x in xData:
        initial_length = x[0]                                  # Get the initial length of the material
        strain = 100 * (x - initial_length) / initial_length   # Apply the engineering strain formula
        strainData.append(strain)                              # Append the calculated strain to the list
        
    return strainData


def window_smoothing(xData, yData, window_size):
    ''' Smooths yData using a sliding window of size window_size.
    
    Args:
        xData (list of numpy arrays): List containing x-axis data.
        yData (list of numpy arrays): List containing y-axis data.
        window_size (int): Size of the sliding window for smoothing.
        
    Returns:
        tuple: Tuple containing two lists with smoothed xData and yData, respectively.
        
    Details:
        - The function applies a sliding window of the given window_size to the yData arrays.
        - For each window, it calculates the average value of yData in that window.
        - The resulting average values are stored in smoothed_ys, corresponding to each yData array.
        - The corresponding xData arrays are modified to match the smoothed data length and stored in smoothed_xs.
        - The function returns a tuple containing the smoothed xData and yData lists.
    '''

    smoothed_ys = [ [] for _ in yData]
    smoothed_xs = [ [] for _ in yData]
    
    for i, array in enumerate(yData):
        
        for datapoint in range(1, len(array)-window_size):  
            averaged_y = np.mean(array[datapoint:datapoint+window_size]) * -0.101325  # converts from atm to MPa
            smoothed_ys[i].append(averaged_y)
            
        smoothed_xs[i] = xData[i][window_size+1:] 
    
    return smoothed_xs, smoothed_ys

def format_func(x, pos):
    '''Formatter for tick labels on the x and y axes.

    Args:
        x (float): Tick value on the axis.
        pos (int): Position of the tick.

    Returns:
        str: The formatted tick label.
        
    Details:
        - If x is equal to 0, it returns an empty string to hide the label.
        - Otherwise, it returns the integer part of x as the tick label.
    '''
    
    if x == 0:
        return ""
    else:
        return f"{int(x)}"

def plot_three_curves(log_files, pltTitle, figNumber): 
    ''' Plots stress-strain curves for three datasets from log files.

    Args:
        log_files (list of str): List of paths to log files containing x (length) and y (pressure) data.
        pltTitle (str): Title for the plot.
        figNumber (int): Figure number for matplotlib figure.

    Returns:
        None

    Details:
        - Reads log file(s) and imports x (length) and y axis (pressure) data.
        - Converts length into % elongation using the engineering strain formula.
        - Performs window smoothing on y-axis data using the window_smoothing function.
        - Plots smoothed data along with additional markers at key positions.
        - Optionally adds black, dotted lines with linear slopes to the plot.
        - Provides customizable options for plot attributes (see Boolean Options section for options).

    '''

    # housekeeping
    xData = []
    yData = []
    strainData = []
    stressData = []
    x = []
    y = []

    # looping through provided log files' paths
    for file_path in log_files:     
        
        # opening a log file
        with open(file_path, 'r') as f:
            lines = f.readlines()
            storingData = False
            
        # Initialize lists to store x and y data
        x = []
        y = []

        # Extracting data from log file
        for line in lines:
            if line.startswith('Step'):
                storingData = True
                continue
            elif line.startswith('Loop'):
                storingData = False
                break
            elif storingData:
                data = line.split()
                x.append(float(data[x_col - 1]))
                y.append(float(data[y_col - 1]))

        # Convert lists to numpy arrays
        xData.append(np.array(x))
        yData.append(np.array(y))
        
        # Using engineering strain formula, convert elongation data to strain values
        # via calculate_strain function
        strainData = calculate_strain(xData)
        
        # Apply a window smoothing to the data, where the window size is a user input.
        # Also converts y data from atm to MPa.
        strainData, stressData = window_smoothing(strainData, yData, window_size)

    # Set figure dimensions
    plt.figure(figNumber, figsize=(8, 8))

    # Set x-axis limits
    plt.xlim(x_min, x_max)

    # Set y-axis limits
    plt.ylim(y_min, y_max)
    
    # Define markers for each line
    markers = ['s', '^', 'o']
    
    # Plot data
    for i in range(len(log_files)):
        plt.plot(strainData[i], stressData[i], color=colors[i], markersize=lineThickness, zorder=1)

        if bool_additionalMarkers == True:
            # Add additional markers at x = [n, 2n, 3n, ..., 10n]
            n = len(strainData[i]) // 7
        
            x_vals = [strainData[i][j] for j in range(0, len(strainData[i]), n)]
            y_vals = [stressData[i][j] for j in range(0, len(stressData[i]), n)]
        
            plt.scatter(x_vals, y_vals, color='black', marker=markers[i], s=markerSize, zorder=2)

    # Add black, dotted lines with linear slope
    if figNumber in range(1, 9):  # Check if figNumber is between 1 or 9 to avoid index errors
        slope = LRR_slopes[figNumber - 1]
        x_range = np.array([np.min(strainData[0]), 100])
        y_range = slope * x_range
        plt.plot(x_range, y_range, color='black', linestyle='dashed', markersize = lineThickness, zorder=3)

    # Adjust padding and linewidth for axis labels and axes spines
    if bool_axesLabel == True:
        plt.xlabel("% Elongation", labelpad=20)
        plt.ylabel("Stress [MPa]", labelpad=20)
        
    if bool_pltTitle == True: 
        plt.title(pltTitle)

    # Set tick intervals and tick parameters
    plt.tick_params(axis='both', which='both', direction='in', length=10, width=2.25, pad=30)
    
    ax = plt.gca()
    ax.spines['left'].set_linewidth(2.25)
    ax.spines['bottom'].set_linewidth(2.25)
    ax.spines['right'].set_linewidth(2.25)
    ax.spines['top'].set_linewidth(2.25)
    
    mpl.rcParams['font.size'] = fontSize
    mpl.rcParams['font.family'] = fontFamily
    
    plt.gca().xaxis.set_major_locator(mpl.ticker.MultipleLocator(x_major_tick_interval))
    plt.gca().yaxis.set_major_locator(mpl.ticker.MultipleLocator(y_major_tick_interval))
    
    plt.gca().xaxis.set_major_formatter(mpl.ticker.FuncFormatter(format_func))
    plt.gca().yaxis.set_major_formatter(mpl.ticker.FuncFormatter(format_func))

    # Show plot
    plt.show()
    
    return

###############
# %% BEGIN CODE
###############

plot_three_curves(log_files_PMP100, "PMP100", 1)

plot_three_curves(log_files_PMP300, "PMP300", 2)

plot_three_curves(log_files_PMP500, "PMP500", 3)

plot_three_curves(log_files_PS100,  "PS100" , 4)

plot_three_curves(log_files_PS300,  "PS300" , 5)

plot_three_curves(log_files_PS500,  "PS500" , 6)

plot_three_curves(log_files_TRP100, "TRP100", 7)

plot_three_curves(log_files_TRP300, "TRP300", 8)

plot_three_curves(log_files_TRP500, "TRP500", 9)