# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 14:54:55 2019

@author: Caro_2
"""

import numpy as np
from matplotlib import pyplot as plt
import random
from scipy import ndimage

import structure as st

# =============================================================================
# Function to create new random-number array and append it to the bubble_array
# =============================================================================
'''
Input: 
------------------------------------------------------------------------------
Bubble_array: np.array(nh,nw)-> defines gameboard 
State_array: np.array(nh,nw)-> gameboard, containing State Vectors 

Output: 
------------------------------------------------------------------------------
Bubble_array:   np.array(nh,nw)-> original gameboard plus new row of length nw 
                containing random numbers (floats) between [1:4]          
'''
def Add_new_row(Bubble_array, State_array):
    (nh,nw)=np.shape(Bubble_array)
    new_x = [random.randint(1, 4) for p in range(0, nw)]
    Bubble_array=np.vstack((new_x, Bubble_array))

    new_v = np.zeros( (1,nw,4), dtype=complex)
    new_v[0] = [ st.dict_states[new_x[j]] for j in range(0,nw)]
    State_array=np.vstack( (new_v, State_array) )

    return Bubble_array[:nh], State_array[:nh]

# =============================================================================
# Python -> find clusters
# =============================================================================
'''
Input: 
------------------------------------------------------------------------------
array: np.array(nh,nw)-> gameboard, containing integers between [1:4] 

Output: 
------------------------------------------------------------------------------
clustered: np.array(2d) -> contains similar integers for each individual cluster
cluster_count: int -> denotes amount of clusters detected (number equals 
                      the integer given to that specific cluster in "clustered)
cluster_size: np.array(1d) -> contains the number of elements in cluster 1,2,3,...
com: list -> contains positions of cluster 1,2,3....

'''

def find_clusters(array):
    clustered = np.empty_like(array)
    unique_vals = np.unique(array)
    cluster_count = 0
    for val in unique_vals:
        labelling, label_count = ndimage.label(array == val)
        for k in range(1, label_count + 1):
            clustered[labelling == k] = cluster_count
            cluster_count += 1
    #figure out cluster_size and cluster position
    ones = np.ones_like(array, dtype=int)
    cluster_sizes = ndimage.sum(ones, labels=clustered, index=range(cluster_count)).astype(int)
    com = ndimage.center_of_mass(ones, labels=clustered, index=range(cluster_count))
    return clustered, cluster_count, cluster_sizes, com;


# =============================================================================
# Implement shooting operator and shooting state function
# =============================================================================
'''
Input: 
------------------------------------------------------------------------------
array: np.array(nh,nw)-> gameboard, containing integers between [1:4]
column: integer -> column into which the state should be shoot 

Output: 
------------------------------------------------------------------------------
index: integer -> index at the first non-nan entry from the bottom is to be found
'''
def index_1st_notNan_entry_fromBotttom(array, column):
    line=array[:,column] #get only the values in column "column" of array
    ind_full=np.where(np.invert(np.isnan(line)))[0] #get indices at which line-values are not nan
    if np.shape(ind_full)[0]==0:
        ind=-1
    if np.shape(ind_full)[0]!=0:
        ind=ind_full[-1]
    return ind     
    
def shoot_state(array,state,column):
    ind=index_1st_notNan_entry_fromBottom(array,column)
    array[ind,column]=state
    return array
# =============================================================================
# Python -> remove clusters
# =============================================================================
'''
Input: 
------------------------------------------------------------------------------
Bubble_array: np.array(nh,nw)-> gameboard, containing integers between [1:4] 
State_array: np.array(nh,nw)-> gameboard, containing State Vectors

Output: 
------------------------------------------------------------------------------
Bubble_array 
State_array
'''
def remove_clusters(Bubble_array, State_array, isdebug=False):
    clusters, cluster_count, cluster_sizes,com = find_clusters(Bubble_array)
    for i, (size, center) in enumerate(zip(cluster_sizes, com)):
        if size>2:
            if (isdebug):
                #print(clusters==i)
                plt.figure(i)
                plt.imshow(clusters==i)
                plt.show()
                    
            Bubble_array[np.where((clusters==i))]=np.nan
            State_array[np.where((clusters==i))]=np.array([0,0,0,0]);
            
            if (isdebug):
                #print(Bubble_array)
                plt.figure(i+10)
                plt.imshow(Bubble_array)
                plt.show()
    return Bubble_array, State_array

# =============================================================================
# Create next value for "shooting"-element
# =============================================================================
'''
This function defines the element that will be shoot at the array
Output:
------------------------------------------------------------------------------
bool:   True if shooting element is an operator
        False if shooting element is a state
        
ind:    [1,2] if shooting element is an operator
        [1,2,3,4] if shooting element is a state
'''
def shooting_element():
    boolean=bool(random.getrandbits(1)) #if True: operator, if False=state
    if boolean==False:
        ind=random.randint(1,4)
    if boolean==True:
        ind=random.randint(1,2)
    return (boolean,ind)

# =============================================================================
'''
Plot the gameboard in colour
Input: Bubble_array
'''
def display_array(Bubble_array, nh, nw):
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    # make color map
    my_cmap = matplotlib.colors.ListedColormap(['r', 'g', 'b'])
    # set the 'bad' values (nan) to be white and transparent
    my_cmap.set_bad(color='w', alpha=0)
    # draw the grid
    for x in range(nw + 1):
        ax.axhline(x, lw=2, color='k', zorder=5)
        ax.axvline(x, lw=2, color='k', zorder=5)
        # draw the boxes
        ax.imshow(data, interpolation='none', cmap=my_cmap, extent=[0, nw, 0, nh], zorder=0)
        # turn off the axis labels
        ax.axis('off')


# =============================================================================
# Debug code
# =============================================================================

# create gameboard
# ----------------------------------------------------------------------------

def debug_python_array():
    (nh,nw)=(10,10)
    Bubble_array=np.empty((nh,nw,))
    Bubble_array[:]=np.nan #np.zeros(100).reshape(10,10)
    State_array=np.zeros( (nh, nw, 4), dtype=complex)
    display_array(Bubble_array, nh, nw)
    for i in range(3):
        Bubble_array, State_array = Add_new_row(Bubble_array, State_array)
        #plt.figure(i)
        #plt.imshow(Bubble_array[:10],origin='upper')
        #plt.show()
    
        plt.figure(101)
        plt.imshow(Bubble_array,origin='upper')
        plt.show()

        #print(Bubble_array)    

        # find clusters
        # ----------------------------------------------------------------------

        Bubble_array, State_array = remove_clusters(Bubble_array, State_array, True);


