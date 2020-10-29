import structure as st
import python_array as pa

import numpy as np
from matplotlib import pyplot as plt


# =============================================================================
# Def user output
# =============================================================================
def Output_shooting_state(boolean, ind):
    # Boolean = True: operator, if False=state
    if boolean == True:
        print('please shoot operator', ind)
    if boolean == False:
        print('please shoot state',ind)
        
# =============================================================================
# Initialize pop-up windows
# =============================================================================
import tkinter as tk
import sys

class mainWindow(object):
    def __init__(self,master):
        self.master=master
        self.l=tk.Label(master,text='please indicate the number of the column \n you want to shoot the state/operator to')
        self.l.pack()
        self.e=tk.Entry(master)
        self.e.pack()
        self.b=tk.Button(master,text='Ok',command=self.cleanup)
        self.b.pack()
        
    def entryValue(self):
        return self.e
    def cleanup(self):
        self.value=self.e.get()
        self.master.destroy()

  
#st.debug_structure()
#Bubble_array,state_array=pa.debug_python_array()

#initialize Bubble_array, state-array and figure
#------------------------------------------------------------------------------
(nh,nw)=(10,10)
Bubble_array=np.empty((nh,nw,))
Bubble_array[:]=np.nan#np.zeros(100).reshape(10,10)
state_array=np.zeros( (nh, nw, 4), dtype=complex)

fig, ax, my_cmap = pa.init_display_array(Bubble_array, nh, nw)
plt.pause(0.0001)

#add a row
#------------------------------------------------------------------------------
Bubble_array, state_array=pa.Add_new_row(Bubble_array, state_array)

# check for clusters
#------------------------------------------------------------------------------
Bubble_array, state_array=pa.remove_clusters(Bubble_array, state_array)#,isdebug=True)

pa.update_display_array(fig,ax,my_cmap,Bubble_array, nh, nw)
'''
plt.figure()
plt.imshow(Bubble_array,plt.cm.jet)
plt.show()
'''
# get user input about where to shoot the object
#------------------------------------------------------------------------------
shooting_element=pa.shooting_element()
Text=Output_shooting_state(shooting_element[0],shooting_element[1])
root=tk.Tk()
m=mainWindow(root)
root.mainloop()
User_input=int(m.value)
print(User_input)

# shoot element
#------------------------------------------------------------------------------
row=pa.index_1st_notNan_entry_fromBotttom(Bubble_array,User_input)
print('row',row)
Bubble_array,state_array=st.shoot_shooting_element(shooting_element[0],shooting_element[1],row,User_input,Bubble_array,state_array,)

pa.update_display_array(fig,ax,my_cmap,Bubble_array, nh, nw)
plt.pause(1000)
