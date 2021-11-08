##Variables for Simulation1##
''' The Simulation1 uses the first 3 algorithms to match drivers and riders.
In this simulation the drivers' and riders' origins and destination are random and not necessarily meeting points.
This simulation does not include trains for the moment.
'''

nb_meetingpoints = 100
nb_stations = 10
nb_origins_destination=1000
nb_riders_min = 100
nb_riders_max = 1000
nb_drivers_min = 100
nb_drivers_max = 100
step=20
nb_simulation = 1
nb_trains=10
frequency_trains=5 #minutes

saving_file = 'Results/result_graph_test2.txt'
SAVE = False #this variable should be True if you want to save the data and false if you want to print just this simulation

#-----------------------------------------------------------------------------------------------------------------------------------------------------#

##Variables for Simulation2##
''' The Simulation2 uses the first 3 algorithms to match drivers and riders. It is a first version of simulation 1 and therefore it is not used anymore.
In this simulation the drivers' and riders' origins and destinations are random meeting points.
This simulation does not include trains for the moment.
Moreover this simulation always generate between 10 and 100 drivers.
'''

"""nb_meetingpoints = 10
nb_stations = 10
nb_riders = 10
nb_drivers = 10
nb_simulation = 10"""

#-----------------------------------------------------------------------------------------------------------------------------------------------------#
#Variables for Simulation3##
''' The Simulation3 uses the 1st 2nd and 4th algorithms to generate riders' trajectories.
In this simulation the drivers' and riders' origins and destination are random and not necessarily meeting points.
This simulation includes trains.
'''

"""nb_meetingpoints = 100
nb_stations = 10
nb_origins_destination=1000
nb_riders_min = 100
nb_riders_max = 1000
nb_drivers_min = 100
nb_drivers_max = 100
step=50
nb_simulation = 1
nb_trains=100
frequency_trains=5 #minutes

saving_file = 'Results/result_graph_test3.txt'
SAVE = True #this variable should be True if you want to save the data and false if you want to print just this simulation
"""
#-----------------------------------------------------------------------------------------------------------------------------------------------------#
#Variables for Simulation4##
''' The Simulation4 uses the 3 first algorithms to generate drivers' trajectories.
In this simulation the drivers' and riders' origins and destination are random and not necessarily meeting points.
This simulation includes trains.
'''
"""
nb_meetingpoints = 100
nb_stations = 10
nb_origins_destination=1000
nb_riders_min = 100
nb_riders_max = 1000
nb_drivers_min = 100
nb_drivers_max = 100
step=50
nb_simulation = 1
nb_trains=100
frequency_trains=5 #minutes

saving_file = 'Results/result_graph_test4.txt'
SAVE = True #this variable should be True if you want to save the data and false if you want to print just this simulation
"""