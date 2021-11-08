#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon March 29 2021

@author: ardant_p
"""

import sys
import datetime as dt
import pandas as pd
import numpy as np
from math import sqrt
from scipy.stats import norm
from graphClasses import Graph, Trajectory

class Vehicle:
    def __init__(self,id):
        self.id = id

class Car(Vehicle):
    def __init__(self,id):
        super().__init__(id)
        self.capacity = 5 #Initalisation
        self.driver   = None

    def __str__(self):
        return (f'car n°{self.id}')

    def get_capacity(self):
        return self.capacity

    def inc_capacity(self):
        if self.capacity == 5 :
            print("Capacity already maxed")
            return
        else :
            self.capacity +=1

    def dec_capacity(self):
        if self.capacity == 0 :
            print("There is no place remaining in this car")
            return 'Error'
        else :
            self.capacity -=1

    def get_driver(self):
        return self.driver

    def set_driver(self, driver):
        if self.driver :
            print("There already is a driver for this car")
            return
        else :
            self.driver = driver

class Train(Vehicle):
    def __init__(self, id, time_start):
        super().__init__(id)
        self.__capacity     = sys.maxsize # capacity infinity
        self.riders         = {} # { person_id : vert_frm, vert_to}
        self.stations       = {} # { station_id : [arrival_time, departure_time]}
        self.time_start=time_start
        self.waiting_time=1 # The train waits 1 min for passengers

    def __str__(self):
        return f'train n°{self.id}'

    def set_stations(self,set_of_stations):
        List_set_of_stations=[]
        for s in set_of_stations.items():
            List_set_of_stations.append(s[0])

        self.stations[List_set_of_stations[0]]=[self.time_start, self.time_start+self.waiting_time]

        for i in range(1,len(List_set_of_stations)):
            traj=Trajectory()
            time_between_stations=Graph.distance(set_of_stations[List_set_of_stations[i-1]], set_of_stations[List_set_of_stations[i]])/traj.get_train_speed()
            arrival_time=self.stations[List_set_of_stations[i-1]][1]+time_between_stations
            self.stations[List_set_of_stations[i]]=[arrival_time, arrival_time+self.waiting_time]
