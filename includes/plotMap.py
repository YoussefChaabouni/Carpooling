#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 15:11:35 2020

@author: ari
"""

import matplotlib.pyplot as plt



class PLOTMap():


    def __init__(self, all_riderso, all_ridersd, all_driverso, all_driversd, stations, mp):
        self.all_riderso = all_riderso
        self.all_ridersd = all_ridersd
        self.all_driverso = all_driverso
        self.all_driversd = all_driversd
        self.stations = stations
        self.meetingpoints = mp

    def plot_map(self):
        List_riderso_X=[]
        List_riderso_Y=[]
        for i in range(len(self.all_riderso)):
            List_riderso_X.append(self.all_riderso[i].x)
            List_riderso_Y.append(self.all_riderso[i].y)
        print("riders origins :", [(List_riderso_X[i] , List_riderso_Y[i]) for i in range(len(List_riderso_X))])
        plt.plot(List_riderso_Y, List_riderso_X, marker = "^", alpha = 0.3, label="Riders' origins")

        List_ridersd_X=[]
        List_ridersd_Y=[]
        for i in range(len(self.all_ridersd)):
            List_ridersd_X.append(self.all_ridersd[i].x)
            List_ridersd_Y.append(self.all_ridersd[i].y)
        print("riders destinations :", List_ridersd_X , List_ridersd_Y)
        plt.scatter(List_ridersd_Y, List_ridersd_X, marker = "v", alpha = 0.2, label="Riders' destinations")

        List_driverso_X=[]
        List_driverso_Y=[]
        for i in range(len(self.all_driverso)):
            List_driverso_X.append(self.all_driverso[i].x)
            List_driverso_Y.append(self.all_driverso[i].y)
        print("drivers origins :", List_driverso_X , List_driverso_Y)
        plt.scatter(List_driverso_Y, List_driverso_X, marker = ">", label="Drivers' origins")

        List_driversd_X=[]
        List_driversd_Y=[]
        for i in range(len(self.all_driversd)):
            List_driversd_X.append(self.all_driversd[i].x)
            List_driversd_Y.append(self.all_driversd[i].y)
        print("drivers destinations :", List_driversd_X , List_driversd_Y)
        plt.scatter(List_driversd_Y, List_driversd_X, marker = "<", label="Drivers' destinations")

        List_mps_X=[]
        List_mps_Y=[]
        for key,value in self.meetingpoints.items():
            List_mps_X.append(self.meetingpoints[key].x)
            List_mps_Y.append(self.meetingpoints[key].y)
        print("meetingpoints :", List_mps_X , List_mps_Y)
        plt.scatter(List_mps_Y, List_mps_X, marker = "x", label='Meeting points')

        List_st_X=[]
        List_st_Y=[]
        for key,value in self.stations.items():
            List_st_X.append(self.stations[key].x)
            List_st_Y.append(self.stations[key].y)
        print("stations :", List_st_X , List_st_Y)
        plt.scatter(List_st_Y, List_st_X, marker = "D", label='Train stations')

        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.show()

#    def plot_trajectories(self,trajectory):
### TODO ###
