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
        print('Please )
    if boolean == False:
        

#st.debug_structure()
#Bubble_array,state_array=pa.debug_python_array()

#initialize Bubble_array and state_array
#------------------------------------------------------------------------------
(nh,nw)=(10,10)
Bubble_array=np.empty((nh,nw,))
Bubble_array[:]=np.nan#np.zeros(100).reshape(10,10)
state_array=np.zeros( (nh, nw, 4), dtype=complex)

#add a row
#------------------------------------------------------------------------------
Bubble_array, state_array=pa.Add_new_row(Bubble_array, state_array)

plt.figure()
plt.imshow(Bubble_array)
plt.show()

# check for clusters
#------------------------------------------------------------------------------
Bubble_array, state_array=pa.remove_clusters(Bubble_array, state_array)#,isdebug=True)

# shoot object
#------------------------------------------------------------------------------
shooting_element=pa.shooting_element()
print(shooting_element)
