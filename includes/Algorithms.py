import random
from random import randint
from graphClasses import Trajectory, Graph, Vertex, MeetingPointsHandler
from personClasses import SetOfPersons, Rider, Driver
from plotMap import PLOTMap
import math
import os

import pandas as pd

from datetime import time, timedelta, datetime

### in this algorithms, time is an int on minutes

## Algorithm 1

"""
 Input : driver (of the Driver class)
 Output
"""

scale=1 # this is the scale of our map (1.33*10 km for 10 in simulation)

## Algorithm 1 ##
def driver_journey_generator(origin, destination, driver,graph):
    #initialisation
    meeting_point_closest_origin = graph.get_neighbor_mp(origin.x,origin.y)
    meeting_point_closest_destination = graph.get_neighbor_mp(destination.x,destination.y)
    station_closest_origin = graph.get_neighbormp_station(origin)
    station_closest_destination = graph.get_neighbormp_station(destination)
    time_driver_starts = 190
    #algorithm
    journey_driver=Trajectory()
    origin.add_time_driver(driver.id,time_driver_starts, time_driver_starts+1)
    journey_driver.set_vertex_order({origin.id:origin, meeting_point_closest_origin.id:meeting_point_closest_origin, meeting_point_closest_destination.id: meeting_point_closest_destination, destination.id: destination})

    r=random.uniform(0,1)

    DETOUR_PERCENTAGE_LENGHT = 1.15

    if r<0.5 :
        ## Try to add a detour close to the origin
        if Graph.distance(meeting_point_closest_origin,station_closest_origin)+Graph.distance(station_closest_origin, meeting_point_closest_destination)<=DETOUR_PERCENTAGE_LENGHT*Graph.distance(meeting_point_closest_origin,meeting_point_closest_destination):
            ## Add a detour through station_closest_origin
            journey_driver.set_vertex_order({origin.id:origin, meeting_point_closest_origin.id: meeting_point_closest_origin,station_closest_origin.id: station_closest_origin, meeting_point_closest_destination.id: meeting_point_closest_destination, destination.id: destination})
            if Graph.distance(meeting_point_closest_origin,station_closest_origin)+Graph.distance(station_closest_origin,station_closest_destination)+Graph.distance(station_closest_destination, meeting_point_closest_destination)<=DETOUR_PERCENTAGE_LENGHT*Graph.distance(meeting_point_closest_origin,meeting_point_closest_destination):
                ##Also add a detour through the station close to the driver
                journey_driver.set_vertex_order({origin.id:origin , meeting_point_closest_origin.id:meeting_point_closest_origin,station_closest_origin.id:station_closest_origin, station_closest_destination.id:station_closest_destination, meeting_point_closest_destination.id:meeting_point_closest_destination,destination.id: destination })
    else:
        ##Try to add a detour close to the destination
        if Graph.distance(meeting_point_closest_origin,station_closest_destination)+Graph.distance(station_closest_destination, meeting_point_closest_destination)<=DETOUR_PERCENTAGE_LENGHT*Graph.distance(meeting_point_closest_origin,meeting_point_closest_destination):
            ##Add a detour through station_closest_destination
            journey_driver.set_vertex_order({origin.id:origin , meeting_point_closest_origin.id:meeting_point_closest_origin, station_closest_destination.id:station_closest_destination, meeting_point_closest_destination.id:meeting_point_closest_destination,destination.id: destination })
            if Graph.distance(meeting_point_closest_origin,station_closest_origin)+Graph.distance(station_closest_origin,station_closest_destination)+Graph.distance(station_closest_destination, meeting_point_closest_destination)<=DETOUR_PERCENTAGE_LENGHT*Graph.distance(meeting_point_closest_origin,meeting_point_closest_destination):
                ##Also add a detour through the station close to the driver destination.
                journey_driver.set_vertex_order({origin.id:origin , meeting_point_closest_origin.id:meeting_point_closest_origin,station_closest_origin.id:station_closest_origin, station_closest_destination.id:station_closest_destination, meeting_point_closest_destination.id:meeting_point_closest_destination,destination.id: destination })
    #print(journey_driver.get_vertex_order())
    driver.set_trajectory(journey_driver)
    ### set the journey's stops' time ###
    driver_origin=None
    for v in driver.get_trajectory().get_vertex_order().values():
        if driver_origin==None:
            driver_origin=v
        else:
            break

    List_mps=[]
    for v in driver.get_trajectory().get_vertex_order().items():
        List_mps.append(v[0])

    for i in range(1,len(List_mps)):
        arrival_time=driver.get_trajectory().get_vertex_order()[List_mps[i-1]].get_depart_time(driver.id)
        arrival_time+=Graph.distance(driver.get_trajectory().get_vertex_order()[List_mps[i-1]],driver.get_trajectory().get_vertex_order()[List_mps[i]])/journey_driver.get_car_speed()
        depart_time=arrival_time
        depart_time+=1
        #print('arrival_time:', arrival_time,' / depart_time:', depart_time)
        driver.get_trajectory().get_vertex_order()[List_mps[i]].add_time_driver(driver.id,arrival_time, depart_time)

    ### The journey's duration in minutes ###

    time_travel = driver.get_trajectory().get_vertex_order()[List_mps[len(List_mps)-1]].get_arrival_time(driver.id)-time_driver_starts

    return driver.get_trajectory().get_vertex_order(), time_travel

## Algorithm 2
def arrival_time_of_rider(start_location, end_location, time_start_location, driver, meeting_point_start, meeting_point_end):
    rider_arrival_time= math.inf
    wainting_time_rider=math.inf
    walking_distance_rider=math.inf

    ##Check if there is a seat available
    for v in driver.get_trajectory().get_vertex_order():
        if driver.available_places(v,meeting_point_end)<=0:
            #print(driver.get_name()+'has no available places')
            return math.inf,math.inf,math.inf

    rider_arrival_time=time_start_location+Graph.distance(start_location,meeting_point_start)/driver.get_trajectory().get_walking_speed()
    #print('rider arrival time',rider_arrival_time)
    walking_distance_rider=Graph.distance(start_location,meeting_point_start)

    #print('depart time mp',meeting_point_start.get_depart_time(driver.id))
    if rider_arrival_time>meeting_point_start.get_depart_time(driver.id):
        #print('the rider arrives too late')
        #print('late')
        return math.inf,math.inf,math.inf

    else:
        destination_driver =None
        for v in driver.get_trajectory().get_vertex_order().values():
            destination_driver=v
        waiting_time_rider=meeting_point_start.get_depart_time(driver.id) -rider_arrival_time
        rider_arrival_time=meeting_point_start.get_arrival_time(driver.id)
        walking_distance_rider+=Graph.distance(end_location, meeting_point_end)
        rider_arrival_time+=Graph.distance(end_location,meeting_point_end)/(driver.get_trajectory().get_walking_speed())

        return waiting_time_rider, walking_distance_rider, rider_arrival_time

## Algorithm 3
def driver_selection_in_only_carpooling(setOfDrivers, rider, time_start, graph):
    rider_arrival_time1= math.inf
    wainting_time_rider1=math.inf
    walking_distance_rider1=math.inf
    NearStationMeetingpoints=graph.get_mpHandler().get_meetingpoints()
    driver_selected=None
    #In the Only Carpooling option, a rider and a driver can carpool only if they have the same origin and destination meeting points
    for driver in setOfDrivers.values():
        origin_driver=None
        destination_driver=None
        for v in driver.get_trajectory().get_vertex_order().values():
            if origin_driver!=None:
                break
            else:
                origin_driver=v

        for v in driver.get_trajectory().get_vertex_order().values():
            destination_driver=v
        #print (graph.get_neighbor_mp(rider.origin.x,rider.origin.y )==graph.get_neighbor_mp(origin_driver.x, origin_driver.y)and graph.get_neighbor_mp(rider.destination.x,rider.destination.y )==graph.get_neighbor_mp(destination_driver.x, destination_driver.y))
        mp1=graph.get_neighbor_mp(origin_driver.x, origin_driver.y)

        mp2=graph.get_neighbor_mp(destination_driver.x, destination_driver.y)
        #for v in driver.get_trajectory().get_vertex_order().values():
        #    print('journey_driver',v.x, v.y)
        #for i in graph.mpHandler.get_meetingpoints().values():
        #    print('mps : ',i.x,i.y)
        if graph.get_neighbor_mp(rider.origin.x,rider.origin.y )==mp1 and graph.get_neighbor_mp(rider.destination.x,rider.destination.y )==mp2:
            #print((rider.origin.x,rider.origin.y),(graph.get_neighbor_mp(rider.origin.x,rider.origin.y ).x, graph.get_neighbor_mp(rider.origin.x,rider.origin.y ).y))
            #print((rider.destination.x,rider.destination.y),(graph.get_neighbor_mp(rider.destination.x,rider.destination.y ).x, graph.get_neighbor_mp(rider.destination.x,rider.destination.y ).y))
            waiting_time_rider=arrival_time_of_rider(rider.origin, rider.destination, time_start, driver, mp1,mp2)[0]
            walking_distance_rider=arrival_time_of_rider(rider.origin, rider.destination, time_start, driver, mp1,mp2)[1]
            rider_arrival_time=arrival_time_of_rider(rider.origin, rider.destination, time_start, driver, mp1, mp2)[2]
            driver_selected=driver

            #print(waiting_time_rider,walking_distance_rider,rider_arrival_time)
            if waiting_time_rider<=45 and walking_distance_rider<=2.5*scale and rider_arrival_time<rider_arrival_time1:
                #print('good')
                rider_arrival_time1=rider_arrival_time
                waiting_time_rider1=waiting_time_rider
                walking_distance_rider1=walking_distance_rider
    return driver_selected,rider_arrival_time1,wainting_time_rider1,walking_distance_rider1

## Algorithm 4
def driver_selection_in_integrated_system(rider, setOfDrivers, setOfTrains, simulation_graph):

    ## Initialisation ##
    arrival_time= 150
    walking_distance=0
    waiting_time=0

    ## FIRST MILE ##

    time_FIRST=math.inf # time at which rider arrives to the station closest to origin

    for driver in setOfDrivers.values():
        origin_driver=None
        for v in driver.get_trajectory().get_vertex_order().values():
            if origin_driver!=None:
                break
            else:
                origin_driver=v
        st_nearest_origin_rider= simulation_graph.get_neighbormp_station(rider.origin)
        mp_nearest_origin_driver=simulation_graph.get_neighbor_mp(origin_driver.x, origin_driver.y)
        mp_nearest_origin_rider=simulation_graph.get_neighbor_mp(rider.origin.x, rider.origin.y)
        if mp_nearest_origin_driver==mp_nearest_origin_rider and st_nearest_origin_rider in driver.get_trajectory().get_vertex_order().values():
            waiting_time1, walking_distance1, arrival_time1=arrival_time_of_rider(rider.origin, st_nearest_origin_rider, arrival_time, driver, mp_nearest_origin_driver, st_nearest_origin_rider)
            if walking_distance+walking_distance1<=2.5*scale and waiting_time+waiting_time1<=45 and arrival_time1<time_FIRST:
                time_FIRST=arrival_time1
                walking_distance=walking_distance+walking_distance1
                waiting_time=waiting_time+waiting_time1

    if time_FIRST==math.inf:
        for driver in setOfDrivers.values():
            origin_driver=None
            for v in driver.get_trajectory().get_vertex_order().values():
                if origin_driver!=None:
                    break
                else:
                    origin_driver=v
            destination_driver =None
            for v in driver.get_trajectory().get_vertex_order().values():
                destination_driver=v
            st_nearest_origin_rider= simulation_graph.get_neighbormp_station(rider.origin)
            mp_nearest_origin_driver=simulation_graph.get_neighbor_mp(origin_driver.x, origin_driver.y)
            mp_nearest_origin_rider=simulation_graph.get_neighbor_mp(rider.origin.x, rider.origin.y)
            mp_closest_to_st_nearest_origin_rider=simulation_graph.get_neighbor_mp(st_nearest_origin_rider.x, st_nearest_origin_rider.y)
            mp_closest_to_destination_driver=simulation_graph.get_neighbor_mp(destination_driver.x, destination_driver.y)
            if mp_closest_to_st_nearest_origin_rider==mp_closest_to_destination_driver:
                waiting_time1, walking_distance1, arrival_time1=arrival_time_of_rider(rider.origin, st_nearest_origin_rider, arrival_time, driver, mp_nearest_origin_driver, mp_closest_to_st_nearest_origin_rider)
                if walking_distance1<=2.5*scale and waiting_time1<=45 and arrival_time1<time_FIRST:
                    time_FIRST=arrival_time1
                    walking_distance=walking_distance1
                    waiting_time=waiting_time1

    if time_FIRST==math.inf:
        st_nearest_origin_rider= simulation_graph.get_neighbormp_station(rider.origin)
        walking_distance1=Graph.distance(rider.origin,st_nearest_origin_rider)
        if walking_distance1<=2.5:
            driver_to_be_ignored=list(setOfDrivers.values())[0] ## used for the following line, to get the speed
            time_FIRST=arrival_time+walking_distance1/driver_to_be_ignored.get_trajectory().get_walking_speed()
            walking_distance=walking_distance1

    if time_FIRST==math.inf:
        arrival_time=math.inf
        return arrival_time


    arrival_time=time_FIRST

    ## TRAIN ##
    arrival_time+=1
    st_nearest_origin_rider= simulation_graph.get_neighbormp_station(rider.origin)
    dict_trains_arrivals={}

    for train in setOfTrains.values():
        dict_trains_arrivals[train]=train.stations[st_nearest_origin_rider.id]

    train_chosen=None
    for  t in dict_trains_arrivals.items(): ## there are always trains in our algorithms
        if t[1][1]>=arrival_time:
            train_chosen=t[0]
            waiting_time+=t[1][1]-arrival_time
            #print(rider.name, 'took', train_chosen.id)
    if train_chosen!=None :
        st_nearest_destination_rider= simulation_graph.get_neighbormp_station(rider.destination)
        arrival_time=train_chosen.stations[st_nearest_destination_rider.id][0]

    ## LAST MILE ##
    time_LAST=math.inf
    List_drivers_LAST=[]
    for driver in setOfDrivers.values():
        if st_nearest_destination_rider in driver.get_trajectory().get_vertex_order().values():
            List_drivers_LAST.append(driver)

    for driver in List_drivers_LAST:
        destination_driver=None
        for v in driver.get_trajectory().get_vertex_order().values():
            destination_driver=v
        mp_closest_to_destination_driver=simulation_graph.get_neighbor_mp(destination_driver.x, destination_driver.y)
        waiting_time1, walking_distance1, arrival_time1=arrival_time_of_rider(st_nearest_destination_rider, rider.destination, arrival_time, driver, st_nearest_destination_rider, mp_closest_to_destination_driver)
        if walking_distance+walking_distance1<=2.5*scale and waiting_time+waiting_time1<=45 and arrival_time1<time_LAST:
            time_LAST=arrival_time1
            walking_distance=walking_distance+walking_distance1
            waiting_time=waiting_time+waiting_time1

    if time_LAST==math.inf:
        for driver in setOfDrivers.values():

            destination_driver=None
            for v in driver.get_trajectory().get_vertex_order().values():
                destination_driver=v

            origin_driver=None
            for v in driver.get_trajectory().get_vertex_order().values():
                if origin_driver!=None:
                    break
                else:
                    origin_driver=v
            st_nearest_destination_rider= simulation_graph.get_neighbormp_station(rider.destination)
            mp_nearest_st_nearest_destination_rider=simulation_graph.get_neighbor_mp(st_nearest_destination_rider.x, st_nearest_destination_rider.y)
            mp_nearest_destination_driver=simulation_graph.get_neighbor_mp(destination_driver.x, destination_driver.y)
            mp_nearest_destination_rider=simulation_graph.get_neighbor_mp(rider.destination.x, rider.destination.y)
            mp_nearest_origin_driver=simulation_graph.get_neighbor_mp(origin_driver.x, origin_driver.y)
            if st_nearest_destination_rider in driver.get_trajectory().get_vertex_order().values() and mp_nearest_destination_rider==mp_nearest_destination_driver:
                if mp_nearest_origin_driver==mp_nearest_st_nearest_destination_rider:
                    waiting_time1, walking_distance1, arrival_time1=arrival_time_of_rider(st_nearest_destination_rider, rider.destination, arrival_time, driver, mp_nearest_st_nearest_destination_rider, mp_closest_to_destination_driver)
                    if walking_distance+walking_distance1<=2.5*scale and waiting_time+waiting_time1<=45 and arrival_time1<time_LAST:
                        time_LAST=arrival_time1
                        walking_distance=walking_distance+walking_distance1
                        waiting_time=waiting_time+waiting_time1
    if time_LAST==math.inf:
        st_nearest_destination_rider= simulation_graph.get_neighbormp_station(rider.destination)
        walking_distance1=Graph.distance(rider.destination,st_nearest_destination_rider)
        if walking_distance1<=2.5*scale:
            driver_to_be_ignored=list(setOfDrivers.values())[0]
            time_LAST=arrival_time+walking_distance1/driver_to_be_ignored.get_trajectory().get_walking_speed()
            walking_distance=walking_distance1

    if time_LAST==math.inf:
        arrival_time=math.inf
        return arrival_time
        return arrival_time
    arrival_time+=time_LAST
    return arrival_time