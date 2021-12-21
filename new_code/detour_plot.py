'''
this function should be able to plot the ratio of detours in the first, last or both miles
it can also display the none ratio (drivers without detours)
'''

from typing import List
from PersonClasses import Driver
import pandas as pd
import seaborn as sns


def detour_plot(DRIVERS : List[Driver]):
    detours = [0,0,0,0] # encoded first ,last, both,none
    
    # for loop to check detours
    for d in DRIVERS:
        #first mile only
        if d.first_detour and not d.last_detour :
            detours[0] += 1

        #last mile only    
        if d.last_detour and not d.first_detour: 
            detours[1] += 1

        #first and last    
        if d.last_detour and d.first_detour :
            print("first and last!!!")
            detours[2] += 1

        # none    
        if not (d.last_detour or d.first_detour) :
            detours[3] += 1
    
    percent = 100/len(DRIVERS)
    detours = [x*percent for x in detours]
    details = {
    'detour type' : ['First mile', 'Last mile', 'Both', 'None'],
    'detour ratio' : detours,
    }
    detours_df = pd.DataFrame(details)

    sns.set_theme(style="whitegrid")
   
    ax = sns.barplot(x="detour type", y="detour ratio", data=detours_df)

    return detours
