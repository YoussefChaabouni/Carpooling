#! /bin/python3

## It's important to change the files in Simulation1 or 2 before launching several simulation if the paremeters have changed
import random
from random import randint
from graphClasses import Trajectory, Graph, Vertex, MeetingPointsHandler
from personClasses import SetOfPersons, Rider, Driver
#from plotMap import PLOTMap
import math
#import pandas as pd
from Algorithms import driver_selection_in_only_carpooling, arrival_time_of_rider, driver_journey_generator
from datetime import time, timedelta, datetime
import matplotlib.pyplot as plt
from vehicleClasses import Car, Train

#### Simulation ####
### Initialisation ###
from Simulation_variables import nb_meetingpoints, nb_stations, nb_origins_destination, nb_riders_min, nb_riders_max, nb_drivers_min, nb_drivers_max, step, nb_simulation, nb_trains, frequency_trains #minutes

from Simulation_variables import saving_file, SAVE
### Seed ###
#random.seed(1)     ## Change seed to generate different environment

print("test")

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

def environment_creator(nb_meetingpoints, nb_stations, nb_trains, nb_origins_destination):
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



    ### Saving to csv ### uncomment if you want to keep the vertexes (in order to run other simulations on the same graph for example)
    '''dg = pd.DataFrame.from_dict(data_graph)

    with open('Results/Vortexes.csv', 'a') as f:
        dg.to_csv(f, header=True)
    '''
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
#print(simulate(nb_riders,setOfPersons, persons_generator(nb_riders, nb_drivers_max, simulation_graph,setOfOrigins, setOfDestinations)[0], simulation_graph))

### map visualisation ###
def graph_plotter(simulation_graph, origins_riders, origins_drivers, destinations_riders, destinations_drivers):
    ### Plotting ###
    #initialisations for plot

    List_mps_plot = simulation_graph.mpHandler.get_meetingpoints()
    List_stations_plot = simulation_graph.get_stations()

    PLOTMap(origins_riders, destinations_riders, origins_drivers, destinations_drivers, List_stations_plot, List_mps_plot).plot_map()

### proportion calculator ###
def simulate(nb_riders, setOfPersons, setOfDrivers, simulation_graph):
    proportion_served=0
    #print(len(setOfDrivers))

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

#### effect of changing nb_drivers ####
def simulation_indenting_drivers(nb_meetingpoints,nb_stations, nb_trains, nb_origins_destination,nb_riders, nb_drivers_min,nb_drivers_max,step):
    ### environment for the simualtion ###
    print("creation de l'environnement indenting drivers")
    simulation_graph, setOfTrains, setOfOrigins, setOfDestinations=environment_creator(nb_meetingpoints,nb_stations, nb_trains, nb_origins_destination)

    #Generation of the different sets of persons
    print("generation des personnes dans indenting drivers")
    setOfPersons=persons_generator(nb_riders, nb_drivers_min, simulation_graph,setOfOrigins, setOfDestinations)
    print("fin de generation des personnes dans indenting drivers")
    setOfRiders = setOfPersons[1]
    setOfCars=setOfPersons[2]

    List_nb_drivers=[i for i in range(nb_drivers_min,nb_drivers_max,step)]
    List_proportion_served=[]# the interesting data from this simulation

    if nb_drivers_max==nb_drivers_min:
        set1=setOfPersons[0]
        setOfRiders=setOfPersons[1]
        print(setOfRiders)
        print(setOfRiders.carpooler_dict)
        results = simulate(nb_riders,setOfRiders, set1, simulation_graph)
        print(results)
        plt.plot(List_nb_drivers, List_proportion_served)
        plt.xlabel('nb drivers')
        plt.ylabel('severd riders')
        plt.show()
    else:
        List_setOfDrivers=[setOfPersons[0]]

        for nb_drivers in range(nb_drivers_min,nb_drivers_max, step):
            set1=persons_generator(nb_riders, nb_drivers, simulation_graph,setOfOrigins, setOfDestinations)[0]
            List_setOfDrivers.append(set1)
            List_proportion_served+=[simulate(nb_riders,setOfRiders, set1, simulation_graph)]
        if SAVE :
            with open(saving_file, 'a') as f: #don't forget to change the name of the file if you change the parameters
                print(List_proportion_served, file=f)
        else :
            plt.plot(List_nb_drivers, List_proportion_served)
            plt.xlabel('nb drivers')
            plt.ylabel('severd riders')
            plt.show()

#### effect of changing the variables ####

def simulation_indenting_riders(nb_meetingpoints,nb_stations, nb_trains, nb_origins_destination,nb_drivers, nb_riders_min,nb_riders_max,step):
    ### environment for the simualtion ###
    print("creation de l'environnement indenting riders")
    simulation_graph, setOfTrains, setOfOrigins, setOfDestinations = environment_creator(nb_meetingpoints,nb_stations, nb_trains, nb_origins_destination)

    #Generation of the different sets of persons
    print("generation des personnes dans indenting riders")
    setOfPersons=persons_generator(nb_riders_min, nb_drivers, simulation_graph,setOfOrigins, setOfDestinations)
    print("fin de generation des personnes dans indenting riders")

    setOfDrivers = setOfPersons[0]
    setOfCars=setOfPersons[2]

    List_nb_riders=[i for i in range(nb_drivers_min,nb_drivers_max,step)]
    List_proportion_served=[]# the interesting data from this simulation
    print(List_proportion_served)
    print(nb_riders_max)
    print(nb_riders_min)
    print(nb_riders_max==nb_riders_min)
    if nb_riders_max==nb_riders_min:
        setOfRiders=setOfPersons[1]
        print("lol")
        print(setOfRiders)
        print("lol2")
        print(setOfRiders[0])
        print("lol3")
        results = simulate(nb_riders,setOfRiders, setOfDrivers, simulation_graph)
        print(results)
        plt.plot(List_nb_drivers, List_proportion_served)
        plt.xlabel('nb riders')
        plt.ylabel('severd riders')
        plt.show()
    else:
        List_setOfRiders=[setOfPersons[1]]

        for nb_riders in range(nb_riders_min,nb_riders_max, step):
            setOfRiders=persons_generator(nb_riders, nb_drivers, simulation_graph,setOfOrigins, setOfDestinations)[1]
            List_setOfRiders.append(setOfRiders)
            List_proportion_served+=[simulate(nb_riders,setOfRiders, setOfDrivers, simulation_graph)]

        if SAVE :
            with open(saving_file, 'a') as f: #don't forget to change the name of the file if you change the parameters
                print(List_proportion_served, file=f)
        else :
            plt.plot(List_nb_drivers, List_proportion_served)
            plt.xlabel('nb drivers')
            plt.ylabel('severd riders')
            plt.show()


##Lancement de la simulation
def launching_simulation(nb_meetingpoints,nb_stations, nb_trains, nb_origins_destination,nb_drivers_min, nb_drivers_max, nb_riders_min,nb_riders_max,step):
    if nb_riders_max==nb_riders_min:
        nb_riders = nb_riders_max
        return simulation_indenting_drivers(nb_meetingpoints,nb_stations, nb_trains, nb_origins_destination,nb_riders, nb_drivers_min,nb_drivers_max,step)
    elif nb_drivers_max==nb_drivers_min:
        nb_drivers = nb_drivers_max
        return simulation_indenting_riders(nb_meetingpoints,nb_stations, nb_trains, nb_origins_destination, nb_drivers, nb_riders_min, nb_riders_max,step)
    else :
        print('Instruction unclear')
        return

launching_simulation(nb_meetingpoints,nb_stations, nb_trains, nb_origins_destination,\
                        nb_drivers_min, nb_drivers_max, nb_riders_min, nb_riders_max, step)
