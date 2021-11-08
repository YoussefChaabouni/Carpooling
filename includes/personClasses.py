#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 12:30:44 2020

@author: ari
"""

import sys
import datetime as dt
import pandas as pd
import numpy as np
from math import sqrt
from scipy.stats import norm
from graphClasses import Trajectory


### We need to diferenciate between WO CO CT

class Person:
    def __init__(self, dt, person_id, person_name):
        self.born_time  = dt
        self.id         = person_id
        self.name       = person_name
        self.trajectory = Trajectory()

    def __repr__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_trajectory(self):
        return self.trajectory

    def set_trajectory(self, trajectory1):
        self.trajectory=trajectory1


class Driver(Person):
    def __init__(self, dt, person_id, person_name, car):
        super().__init__(dt, person_id, person_name)
        self.__SPEED    = 40.0*16.6666666667 #40km/h in m/min
        self.car=car
        self.riders_in_journey={}

        for i in self.get_trajectory().get_vertex_order().keys():
            self.get_trajectory().get_vertex_order()[i]=[[],[]] ## less than capacity, for each stop, there is a list of before and a list for after.

    def get_speed(self):
        self.__SPEED

    def set_trajectory(self, trajectory1):
        super().set_trajectory(trajectory1)
        for v in self.trajectory.get_vertex_order().values():
            self.riders_in_journey[v]=[[],[]]

    def occupy_a_place(self,rider_id, mp1, mp2):

        if mp1 in self.riders_in_journey.keys() and mp2 in self.riders_in_journey.keys():

            if available_places(mp1,mp2)>0:

                for v in self.riders_in_journey.keys():
                    if v!=mp1 and v!=mp2:
                        self.riders_in_journey[v][0]=rider## adding rider to the the dict for after
                        v.riders_in_journey[v][1]=rider## adding rider to the the dict of before

                    elif v==mp1:
                        v.riders_in_journey[V][1]=rider
                    elif v==mp2:
                        v.riders_in_journey[v][0]=rider

            else:
                print(self.get_name()," has no available place")
        else:
            print("one or both of the meeting points are out of the journey")


    def available_places(self,mp1,mp2):

        List_places=[]  #list of number of places occupied before and after arrival in evry node of the trajectory
        for v in self.riders_in_journey.keys():
            if v!=mp1 and v!=mp2:
                List_places.append(self.car.capacity-len(self.riders_in_journey[v][0]))
                List_places.append(self.car.capacity-len(self.riders_in_journey[v][1]))
            elif v==mp1:
                List_places.append(self.car.capacity-len(self.riders_in_journey[v][1]))
            elif v==mp2:
                List_places.append(self.car.capacity-len(self.riders_in_journey[v][0]))
        return min(List_places)

''''
    def liberate_places(self,rider_id):
        List_keys=[]

        for v in self.riders_in_journey.keys():
            List_keys.append(v)

        for i in range(List_keys.index(mp1),List_keys.index(mp2)):
            for j in self.get_trajectory().get_vertex_order()[List_keys[i]][0]:
                if j==rider_id:
                    self.get_trajectory().get_vertex_order()[List_keys[i]][0].remove(rider)
            for j in self.get_trajectory().get_vertex_order()[List_keys[i]][1]:
                if j==rider_id:
                    self.get_trajectory().get_vertex_order()[List_keys[i]][1].remove(rider)
'''




class Rider(Person):
    def __init__(self, origin, destination, dt, person_id, person_name):
        super().__init__(dt, person_id, person_name)
        self.__SPEED    = 3.0*16.6666666667 #3km/h in m/min
        self.origin=origin
        self.destination=destination
        self.depart_time_origin=None
    def get_speed(self):
        return self.__SPEED

    def get_origin(self):
        return self.origin

    def get_destination(self):
        return self.destination

    # Candidate vehicles for carpooling only
    def get_candidatevehicles(self, drivers, mp_orig, mp_dest, wmp):
        found = 0
        c_drivers = list()
        for driv in drivers:
            driv_xo = driv.get_xorg()
            driv_yo = driv.get_yorg()
            driv_xd = driv.get_xdst()
            driv_yd = driv.get_ydst()
            mpo_x = mp_orig.get_x()
            mpo_y = mp_orig.get_y()
            mpd_x = mp_dest.get_x() # riders destination (neighbormpdest_id)
            mpd_y = mp_dest.get_y()
            if ((mpo_x == driv_xo) and (mpo_y == driv_yo)):
                if ((mpd_x == driv_xd) and (mpd_y == driv_yd)):
                    a, b = pd.to_datetime(driv.get_time()), pd.to_datetime(wmp)
                    if ((a > b) and (driv.get_id(), a) not in c_drivers):
                    #if (pd.to_datetime(driv.get_time()) > pd.to_datetime(wmp)):
                        #print z, b, a
                        c_drivers.append((driv.get_id(), a))
                        #c_drivers.append(driv.get_time())
                        found = 1
                    else:
                        None
                else:
                    None
            else:
                None
        if (len(c_drivers) == 0 or found == 0):
            #print '%s no driver available' %z
            return None
            #no_drivers.append(z)
        else:
            c_drivers.sort(key=lambda tup: tup[1])
            return c_drivers
            #rider_driver.append((z,candidate_drivers[0][0]))
        #return (c_drivers, found)

    def set_depart_time_origin(time_depart):
        self.depart_time_origin=time_depart

class SetOfPersons:
    def __init__(self, id):
        self.id             = id
        self.carpooler_dict = {} #{ rider : (Rider, vert_frm, vert_to ) } when it's for a car else just { person_id : Person}
        self.num_carpoolers = 0
        self.car            = None

    def __iter__(self):
        return iter(self.carpooler_dict.values())

    def get_carpooler(self, carpooler_id):
        if carpooler_id in self.carpooler_dict:
            return self.carpooler_dict[carpooler_id]
        else:
            print("Carpooler doesn't exist")
            return

    def add_passenger(self, person, vert_frm = None, vert_to = None): #Adds a new rider to the car or a new person to the graph

        if not (vert_frm or vert_to):
            self.carpooler_dict[person.id] = person

        else :
            self.carpooler_dict[person.id] = [person, vert_frm, vert_to]
