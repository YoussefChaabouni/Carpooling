
import random
from random import randint
from graphClasses import Trajectory, Graph, Vertex, MeetingPointsHandler
from personClasses import SetOfPersons, Rider, Driver
from plotMap import PLOTMap
import math
import pandas as pd
from Algorithms import driver_selection_in_only_carpooling, arrival_time_of_rider, driver_journey_generator,driver_selection_in_integrated_system
from datetime import time, timedelta, datetime
import matplotlib.pyplot as plt
from vehicleClasses import Car, Train

#### Simulation ####
### Seed ###
#random.seed(1) ## Change seed to generate different environment
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

### to calculate one proportion nb_drivers_min needs to be equal to nb_drivers_min
### Initialisation ###
nb_meetingpoints = 100
nb_stations = 10
nb_origins_destination=1000
nb_riders_min = 100
nb_riders_max = 1000
nb_drivers_min = 100
nb_drivers_max=1000
step=50
nb_simulation = 1
nb_trains=100
frequency_trains=5 #minutes

def environment_creater(nb_meetingpoints, nb_stations, nb_trains, nb_origins_destination):
    #### The graph ####
    simulation_graph=Graph()
    setOfOrigins={}
    setOfDestinations={}
    ### initialisation Backup on csv ###
    data_graph = {"id":[],"x" : [],"y" : []}
    setOfTrains={}

    ### Creating vertex and the meeting points handler ###
    mps_handler=MeetingPointsHandler()


    coords = []

    for i in range(nb_meetingpoints):
        node_id = f'node_{i}'
        node_name = f'name_{i}'
        x = random.random()*10
        y = random.random()*10
        while (x,y) in coords : ## Each node has to have a different coordinate
            x = random.random()*10
            y = random.random()*10
        coords.append((x,y))
        mps_handler.add_meetingpoint(node_id,node_name,x,y)
        data_graph["id"].append(node_id)
        data_graph["x"].append(x)
        data_graph["y"].append(y)

        simulation_graph.add_mpHandler(mps_handler)



    for i in range(nb_origins_destination):
        origin_id = f'origin_{i}'
        origin_name = f'origin_{i}'
        destination_id = f'destination_{i}'
        destination_name = f'destination_{i}'
        bool_org=False
        bool_dest=False
        x_org = random.random()*10
        y_org = random.random()*10
        x_dest = random.random()*10
        y_dest = random.random()*10

        while ((x_org,y_org)in coords) or((x_dest,y_dest)in coords) or ((x_org,y_org)==(x_dest,y_dest)) : ## some origins and destinations must be nears meeting points
            x_org = random.random()*10
            y_org = random.random()*10
            x_dest = random.random()*10
            y_dest = rrandom.random()*10

        node_org=Vertex(origin_id, origin_name, x_org, y_org)
        setOfOrigins[i]=node_org
        node_dest=Vertex(destination_id, destination_name, x_dest, y_dest)
        setOfDestinations[i]=node_dest

    #### Adding stations ####
    for i in range(nb_stations):
        station_id = f'station_{i}'
        station_name = f'station_name_{i}'
        x = i
        y = i
        simulation_graph.add_station(station_id,station_name,x,y)
    #### Adding trains ####
    for i in range(nb_trains):

        train_id=f'train_{i}'
        train=Train(train_id, i*frequency_trains)
        train.set_stations(simulation_graph.stations)
        setOfTrains[train_id]=train
        #print(train.stations)



    ### Saving to csv ###
    dg = pd.DataFrame.from_dict(data_graph)

    with open('Results/Vortexes.csv', 'a') as f:
        dg.to_csv(f, header=True)

    return simulation_graph, setOfTrains, setOfOrigins, setOfDestinations

### Creating riders and drivers ###
## Riders and drivers are created within a frame of 3 hours. if driver's time is 124min, this means is equivalent to 2h 4min
def persons_generator(nb_riders, nb_drivers, simulation_graph, setOfOrigins, setOfDestinations): ## we generate here riders and drivers (and their journeys)
    #### Persons data ####
    data_persons = {"id": [],"origin" : [],"destination" : []}

    #### initialisation for map visualisation ####
    origins_riders = []
    origins_drivers = []
    destinations_riders = []
    destinations_drivers = []

    #### setOfPersons, setOfDrivers and setOfCars ####
    setOfPersons= SetOfPersons("set1")
    setOfDrivers = {}
    setOfCars={}



    List_mps=[]

    for i in simulation_graph.mpHandler.get_meetingpoints():
        List_mps.append(i)


    for i in range(nb_riders):

        node_org=random.choice(list(setOfOrigins.items()))[1]
        node_dest=random.choice(list(setOfDestinations.items()))[1]
        rider=Rider(node_org, node_dest, random.randint(0,180), f'rider{i}', f'namer{i}')## a random time between 00h and 3am 180=60*3, in minutes
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


        #### Adding  a Car ####

        car.set_driver(driver)
        setOfCars[car_id]=Car(car_id)

        setOfPersons.add_passenger(driver)
        setOfDrivers[driver.id]=driver
        #origin
        node_org=random.choice(list(setOfOrigins.items()))[1]
        node_dest=random.choice(list(setOfDestinations.items()))[1]
        driver_org = node_org #for now, the driver starts from meeting points
        origins_drivers.append(driver_org)
        #destination
        driver_dest = node_dest
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

    return [setOfDrivers, setOfPersons, setOfCars, origins_riders, origins_drivers, destinations_riders, destinations_drivers]

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
    print(len(setOfDrivers))

    for i in range(nb_riders):
        rider=setOfPersons.get_carpooler(f'rider{i}')[0]
        ### Selecting drivers for riders ###
        driver, arrival_time, wainting_time, walking_distance= driver_selection_in_only_carpooling(setOfDrivers, rider,150, simulation_graph)
        if  arrival_time<math.inf:
            proportion_served+=1
            #print(rider.name, driver.name)
            #print('the driver journey: ', driver.get_trajectory().get_vertex_order().values(), '// the rider journey:  origin = (',rider.origin.x, ',', rider.origin.y, ')', ' and destination = (',rider.destination.x, ',', rider.destination.y, ')' )
        #else:
            #print('no driver found for', rider.name)
    #print('the proportion of rider served: ', proportion_served/nb_riders)
    return proportion_served/ nb_riders
def proportion_driver_taking_detour(nb_riders, setOfPersons, setOfDrivers, simulation_graph, setOfOrigins, setOfDestinations):

    proportion_detour=0
    print(len(setOfDrivers))

    for driver in setOfDrivers.values():
        origin=random.choice(list(setOfOrigins.items()))[1]
        destination=random.choice(list(setOfDestinations.items()))[1]
        ### Selecting drivers for riders ###
        journey_driver, time_travel=driver_journey_generator(origin, destination, driver,simulation_graph)
        if  len(journey_driver)>=5:
            proportion_detour+=1
            #print(rider.name, driver.name)
            #print('the driver journey: ', driver.get_trajectory().get_vertex_order().values(), '// the rider journey:  origin = (',rider.origin.x, ',', rider.origin.y, ')', ' and destination = (',rider.destination.x, ',', rider.destination.y, ')' )
        #else:
            #print('no driver found for', rider.name)
    #print('the proportion of rider served: ', proportion_served/nb_riders)
    return proportion_detour/ len(setOfDrivers)


### environment for the simualtion ###
simulation_graph, setOfTrains, setOfOrigins, setOfDestinations=environment_creater(nb_meetingpoints,nb_stations, nb_trains, nb_origins_destination)
setOfPersons=persons_generator(nb_riders_max, nb_drivers_min, simulation_graph,setOfOrigins, setOfDestinations)[1]
List_nb_drivers=[i for i in range(nb_drivers_min,nb_drivers_max,step)]
setOfCars=persons_generator(nb_riders_max, nb_drivers_min, simulation_graph,setOfOrigins, setOfDestinations)[2]
### proportion servered in integrated system ###
setOfDrivers=persons_generator(nb_riders_max, nb_drivers_min, simulation_graph,setOfOrigins, setOfDestinations)[0]
List_proportion_detour=[]

for i in range(nb_drivers_min,nb_drivers_max, step):
    set2=persons_generator(nb_riders_max, i, simulation_graph,setOfOrigins, setOfDestinations)[0]
    List_proportion_detour+=[proportion_driver_taking_detour(nb_riders_max, setOfPersons, set2, simulation_graph, setOfOrigins, setOfDestinations)]
    print(List_proportion_detour[-1])


plt.plot(List_nb_drivers, List_proportion_detour)
plt.xlabel('nb drivers')
plt.ylabel('drivers taking detour(%)')
plt.show()
