#! /bin/python3
# SIMULATION WITH ONLY CARPOOLING


## It's important to change the files in Simulation1 or 2 before launching several simulation if the paremeters have changed
import random
from random import randint
from graphClasses import Trajectory, Graph, Vertex, MeetingPointsHandler
from personClasses import SetOfPersons, Rider, Driver
from plotMap import PLOTMap
import math
import pandas as pd
from Algorithms import driver_selection_in_only_carpooling, arrival_time_of_rider, driver_journey_generator
from datetime import time, timedelta, datetime
import matplotlib.pyplot as plt
from vehicleClasses import Train, Car

#### Simulation ####
### Initialisation ###
from Simulation_variables import nb_meetingpoints, nb_stations, nb_riders, nb_drivers, nb_simulation

### Seed ###
#random.seed(1)     ## Change seed to generate different environment

def time_printer(t):
    t=t/60
    m,h= math.modf(t)
    H=''
    if h<24:
        return  str(int(h))+'h '+str(int(m*60))+'min'
    else:
        r=h/24
        h=h-r*24
        return  str(int(r))+'days '+str(int(h))+'h '+str(int(m*60))+'min'

### creating the environment
def environment_creater(nb_meetingpoints, nb_stations):
    #### The graph ####
    simulation_graph=Graph()
    ### initialisation Backup on csv ###
    data_graph = {"id":[],"x" : [],"y" : []}
    ### Creating vertex and the meeting points handler ###
    mps_handler=MeetingPointsHandler()
    coords = []
    for i in range(nb_meetingpoints):
        node_id = f'node_{i}'
        node_name = f'name_{i}'
        x = random.randint(0,50)
        y = random.randint(0,50)
        while (x,y) in coords : ## Each node has to have a different coordinate
            x = random.randint(0,50)
            y = random.randint(0,50)
        mps_handler.add_meetingpoint(node_id,node_name,x,y)
        data_graph["id"].append(node_id)
        data_graph["x"].append(x)
        data_graph["y"].append(y)
        simulation_graph.add_mpHandler(mps_handler)
    #### Adding stations ####
    for i in range(nb_stations):
        station_id = f'station_{i}'
        station_name = f'station_name_{i}'
        x = i*10
        y = i*10
        simulation_graph.add_station(station_id,station_name,x,y)
    ### Saving to csv ###
    dg = pd.DataFrame.from_dict(data_graph)
    with open('Results/Vortexes.csv', 'a') as f:
        dg.to_csv(f, header=True)
    return simulation_graph


### Creating riders and drivers ###
## Riders and drivers are created within a frame of 3 hours. if driver's time is 124min, this means is equivalent to 2h 4min
def persons_generator(nb_riders, nb_drivers, simulation_graph,setOfDrivers1 = {}): ## we generate here riders and drivers (and their journeys)
    #### Persons data ####
    data_persons = {"id": [],"origin" : [],"destination" : []}
    #### initialisation for map visualisation ####
    origins_riders = []
    origins_drivers = []
    destinations_riders = []
    destinations_drivers = []
    #### setOfPersons and setOfDrivers ####
    setOfPersons= SetOfPersons("set1")
    setOfDrivers = setOfDrivers1
    List_mps=[]
    for i in simulation_graph.mpHandler.get_meetingpoints():
        List_mps.append(i)
    for i in range(nb_riders):
        rider=Rider(simulation_graph.mpHandler.get_random(), simulation_graph.mpHandler.get_random(), random.randint(0,180), f'rider{i}', f'namer{i}')## a random time between 00h and 3am 180=60*3, in minutes
        setOfPersons.add_passenger(rider, rider.get_origin(), rider.get_destination())
        data_persons["origin"].append((rider.get_origin().x,rider.get_origin().y))
        data_persons["destination"].append((rider.get_destination().x,rider.get_destination().x))
        data_persons["id"].append(f'rider{i}')
        origins_riders.append(rider.get_origin())
        destinations_riders.append(rider.get_destination())
    #Loop to create the driver's journeys and adding them to the csv file and the plot
    for i in range(nb_drivers):
        car_id=f'car_{i}'
        car=Car(car_id)
        driver=Driver(random.randint(0,180), f'driver{i}', f'named{i}', car)
        #print(time_printer(driver.born_time))
        #print(driver.born_time)
        setOfPersons.add_passenger(driver)
        setOfDrivers[driver.id]=driver
        #origin
        driver_org = simulation_graph.mpHandler.get_random() #for now, the driver starts from meeting points
        origins_drivers.append(driver_org)
        #destination
        driver_dest = simulation_graph.mpHandler.get_random()
        destinations_drivers.append(driver_dest)
        #data for csv
        data_persons["origin"].append((driver_org.x,driver_org.y))
        data_persons["destination"].append((driver_dest.x,driver_dest.x))
        data_persons["id"].append(f'driver{i}')
        ### Creating journeys for drivers
        driver_journey_generator(driver_org, driver_dest, driver, simulation_graph)
        ### Saving to csv ###
        """
        dp = pd.DataFrame.from_dict(data_persons)
        with open('Results/Persons.csv', 'a') as ff:
            dp.to_csv(ff, header=True)
        """
    return [setOfDrivers, setOfPersons, origins_riders, origins_drivers, destinations_riders, destinations_drivers]


### map visualisation ###
def graph_plotter(simulation_graph, origins_riders, origins_drivers, destinations_riders, destinations_drivers):
    ### Plotting ###
    #initialisations for plot
    List_mps_plot = simulation_graph.mpHandler.get_meetingpoints()
    List_stations_plot = simulation_graph.get_stations()
    PLOTMap(origins_riders, destinations_riders, origins_drivers, destinations_drivers, List_stations_plot, List_mps_plot).plot_map()


### proportion calculator ###
def proportion_served_calculator(nb_riders, setOfPersons, setOfDrivers, simulation_graph):
    proportion_served=0
    for i in range(nb_riders):
        rider=setOfPersons.get_carpooler(f'rider{i}')[0]
        ### Selecting drivers for riders ###
        drS = driver_selection_in_only_carpooling(setOfDrivers, rider, 150, simulation_graph)
        if drS[1]<math.inf:
            proportion_served+=1
            driver= drS(setOfDrivers, rider, 150, simulation_graph)[0]
            #print(rider.name, driver.name)
            #print('the driver journey: ', driver.get_trajectory().get_vertex_order().values(), '// the rider journey:  origin = (',rider.origin.x, ',', rider.origin.y, ')', ' and destination = (',rider.destination.x, ',', rider.destination.y, ')' )
        #else:
            #print('no driver found for', rider.name)
    #print('the proportion of rider served: ', proportion_served/nb_riders)
    return proportion_served / nb_riders



#### effect of changing nb_drivers ####
### environment for the simualtion ###
simulation_graph=environment_creater(nb_meetingpoints,nb_stations)
setOfPersons=persons_generator(nb_riders, nb_drivers, simulation_graph)[1]
List_nb_drivers=[i for i in range(10,100)]
List_setOfDrivers=[persons_generator(nb_riders, List_nb_drivers[0], simulation_graph)[0]]
List_proportion_served=[proportion_served_calculator(nb_riders,setOfPersons, persons_generator(nb_riders, nb_drivers, simulation_graph)[0], simulation_graph)]
for i in range(11,100):
    car_id=f'car_{i}'
    car=Car(car_id)
    driver=Driver(random.randint(0,180), f'driver{i}', f'named{i}', car)
    driver_org = simulation_graph.mpHandler.get_random() #for now, the driver starts from meeting points
    #destination
    driver_dest = simulation_graph.mpHandler.get_random()
    driver_journey_generator(driver_org, driver_dest, driver, simulation_graph)
    set1=List_setOfDrivers[i-11]
    set1[driver.id]=driver
    List_setOfDrivers.append(set1)
    setOfPersons=persons_generator(nb_riders, nb_drivers, simulation_graph)[1]
    List_proportion_served+=[proportion_served_calculator(nb_riders,setOfPersons, List_setOfDrivers[i-10], simulation_graph)]

    ##  uncomment the following lines in order to plot this simulation
    #plt.plot(List_nb_drivers, List_proportion_served)
    #plt.xlabel('nb drivers')
    #plt.ylabel('severd riders(%)')

#saves the graph points for nb of riders taken in function of the number of driver in a file
#with open('Results/result_diff_graph.txt', 'a') as f:
#    print(List_proportion_served, file=f)
