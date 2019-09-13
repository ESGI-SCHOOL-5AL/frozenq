# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 14:54:55 2019

@author: Caro_2
"""

import numpy as np
from matplotlib import pyplot as plt
import random
from scipy import ndimage

import structure

# =============================================================================
# Function to create new random-number array and append it to the bubble_array
# =============================================================================
'''
Input: 
------------------------------------------------------------------------------
Bubble_array: np.array(nx,ny)-> defines gameboard 
State_array: np.array(nx,ny)-> gameboard, containing State Vectors 

Output: 
------------------------------------------------------------------------------
Bubble_array:   np.array(nx,ny)-> original gameboard plus new row of length ny 
                containing random numbers (floats) between [1:4]          
'''
def Add_new_row(Bubble_array, State_array):
    (nx,ny)=np.shape(Bubble_array)
    new_x = [random.randint(1, 4) for p in range(0, ny)]
    Bubble_array=np.vstack((new_x,Bubble_array))
    return Bubble_array, State_array

# =============================================================================
# Python -> find clusters
# =============================================================================
'''
Input: 
------------------------------------------------------------------------------
array: np.array(nx,ny)-> gameboard, containing integers between [1:4] 

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
    ones = np.ones_like(Bubble_array_final, dtype=int)
    cluster_sizes = ndimage.sum(ones, labels=clustered, index=range(cluster_count)).astype(int)
    com = ndimage.center_of_mass(ones, labels=clustered, index=range(cluster_count))
    return clustered, cluster_count, cluster_sizes, com


# =============================================================================
# Implement shooting operator and shooting state function
# =============================================================================
'''
Input: 
------------------------------------------------------------------------------
array: np.array(nx,ny)-> gameboard, containing integers between [1:4]
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
Bubble_array: np.array(nx,ny)-> gameboard, containing integers between [1:4] 
State_array: np.array(nx,ny)-> gameboard, containing State Vectors

Output: 
------------------------------------------------------------------------------
Bubble_array 
State_array
'''
def remove_clusters(Bubble_array, State_array, isdebug=False):
    clusters, cluster_count, cluster_sizes,com =
                 find_clusters(Bubble_array_final)
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
                #print(Bubble_array_final)
                plt.figure(i+10)
                plt.imshow(Bubble_array_final)
                plt.show()

# =============================================================================
# Main
# =============================================================================

# create gameboard
# ----------------------------------------------------------------------------
(nx,ny)=(10,10)
Bubble_array=np.empty((nx,ny,))
Bubble_array[:]=np.nan#np.zeros(100).reshape(10,10)
#print(Bubble_array)
for i in range(3):
    Bubble_array=Add_new_row(Bubble_array)
    #plt.figure(i)
    #plt.imshow(Bubble_array[:10],origin='upper')
    #plt.show()
    
Bubble_array_final=Bubble_array[:10]
plt.figure(101)
plt.imshow(Bubble_array_final,origin='upper')
plt.show()

#print(Bubble_array)    

# find clusters
# ----------------------------------------------------------------------------

Bubble_array_final, State_array = remove_clusters(Bubble_array_final, State_array, True)

