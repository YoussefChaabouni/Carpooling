#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon March 29 2021

@author: ardant_p
"""
import sys
import datetime as dt
import pandas as pd
import numpy as np
import random
from math import sqrt
from scipy.stats import norm


class Vertex:
    def __init__(self,node_id, node_name, x_n, y_n):
        # node: id of the station
        self.id = node_id
        self.x = x_n
        self.y = y_n
        self.arrival_time = {} ## dictionary of drivers: arrival time
        self.depart_time  = {}## dictionary of drivers: departure time
        self.name = node_name

    def __repr__(self):
        return repr((self.x, self.y))

    def __str__(self): #à compléter
        return str(self.id) # + ' adjacent: ' + str([x.id for x in self.adjacent])

    def __lt__(self, other):
        return self.distance < other.distance
    def __le__(self,other):
        return self.distance <= other.distance

    def add_time_driver(self,driver_id,arrival_time, departure_time):
        self.arrival_time[driver_id]=arrival_time
        self.depart_time[driver_id]=departure_time

    def get_arrival_time(self, driver_id):
        if driver_id in self.arrival_time.keys():
            return self.arrival_time[driver_id]


    def get_depart_time(self, driver_id):
        if driver_id in self.depart_time.keys():
            return self.depart_time[driver_id]

class Station(Vertex):
    def __init__(self,node_id, node_name, x_n, y_n):
        super().__init__(node_id, node_name, x_n, y_n)

class MeetingPointsHandler:
    def __init__(self):
        self.meetingpoint_dict = {}
        self.num_meetingpoints = 0

    def get_meetingpoints(self):
        return self.meetingpoint_dict

    def get_random(self):
        return random.choice(list(self.meetingpoint_dict.items()))[1]

    def __iter__(self):
        return iter(self.meetingpoint_dict.values())

    def add_meetingpoint(self, node_id, node_name, x_n, y_n):
        self.num_meetingpoints = self.num_meetingpoints + 1
        new_meetingpoint = Vertex(node_id, node_name, x_n, y_n)
        self.meetingpoint_dict[node_id] = new_meetingpoint

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0
        ## meeting point
        self.mpHandler = None
        ##stations {id : Station}
        self.stations = {}
        self.stations_arrival_time={}

    def get_mpHandler(self):
        return self.mpHandler

    def distance(node_1,node_2):
        return sqrt((node_2.x-node_1.y)**2 + (node_2.x-node_1.x)**2)

    def get_random_station(self):
        return random.choice(list(self.stations.items()))[1]

    def get_neighbormp_station(self, aMeetingpoint):
        neighbors = []
        for key, st in self.stations.items():
            dis = sqrt((aMeetingpoint.x-st.x)**2 + (aMeetingpoint.y-st.y)**2)
            neighbors.append((st, dis))
        neighbors.sort(key=lambda tup: tup[1])
        return neighbors[0][0]

    def get_neighbor_mp(self, x,y):
        neighbors = []
        for mp in self.mpHandler.get_meetingpoints().values():
            if mp.x!=x or mp.y!=y:
                dis = sqrt((x-mp.x)**2 + (y-mp.y)**2)
                neighbors.append((mp, dis))
        neighbors.sort(key=lambda tup: tup[1])
        return neighbors[0][0]

    def add_station(self, node_id, node_name, x_n, y_n):
        self.num_vertices += 1
        new_vertex = Station(node_id, node_name, x_n, y_n)
        self.stations[node_id] = new_vertex

    def add_mpHandler(self, mpsHandler):
        self.mpHandler=mpsHandler

    def get_stations(self):
        return self.stations

class Trajectory(Graph):
    def __init__(self):
        self.__walking_speed    = 3.0*0.0166666666667 #3km/h in km/min
        self.__car_speed        = 40.0*0.0166666666667  #40km/h in km/min
        self.__train_speed      = 80.0*0.0166666666667  #80km/h in km/min
        self.vertex_order       = {}

    def __iter__(self):
        return iter(self.vertex_order.values())

    def get_walking_speed(self):
        return self.__walking_speed

    def get_car_speed(self):
        return self.__car_speed

    def get_train_speed(self):
        return self.__train_speed

    def get_vertex_order(self):
        return self.vertex_order

    def set_vertex_order(self, dict_of_vertex):
        self.vertex_order=dict_of_vertex
