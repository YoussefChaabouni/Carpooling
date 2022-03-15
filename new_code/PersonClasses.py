
import sys
from meansClasses import Car
from graphClasses import Trajectory
## USER CLASS

class User:

    # Class constructor
    def __init__(self,pos_depart, pos_arrivee, ID, born_time, trajectory):
        self.born_time = born_time
        self.id = ID
        self.pos_depart = pos_depart # ID de node d'origine
        self.pos_arrivee = pos_arrivee # ID de node d'arrivée
        self.trajectory = trajectory
    

    ########## GETTERS AND SETTERS #########################
    def __repr__(self):
        return "User : "+str(self.id)
    
    def get_id(self):
        return self.id

    def get_pos_depart(self):
        return self.pos_depart
    
    def get_pos_arrivee(self):
        return self.pos_arrivee
    
    def get_born_time(self):
        return self.born_time
    
    def get_trajectory(self):
        return self.trajectory

class Rider(User):

    def __init__(self, pos_depart, pos_arrivee, ID, born_time,trajectory,waiting_time = 0,walking_distance = 0,walking_speed = 4.5,solution=""):
        User.__init__(self,pos_depart, pos_arrivee, ID, born_time,trajectory)
        self.waiting_time = waiting_time
        self.walking_distance = walking_distance
        self.walking_speed = walking_speed
        self.solution = solution
    
    ###### UPDATE WALKING AND WAITING TIMES ##########
    def update_waiting_time(self, waiting_duration):

        ## we could verify that the waiting duration is a positive integer
        if(waiting_duration >= 0):
            self.waiting_time = waiting_duration 
        else :
            sys.exit("waiting durations should always be positive")

    def update_walking_distance(self, walking_distance):

        ## we could verify that the walking duration is a positive integer
        if(walking_distance >= 0):
            self.walking_distance = walking_distance 
        else :
            sys.exit("walking distance should always be positive")

class Driver(User,Car):
    
    #_______________ init ________________
    def __init__(self,pos_depart,pos_arrivee,ID_user,born_time,ID_car,Speed,max_capacity,current_capacity,riders_list,trajectory,detour_rate=0.15):
        User.__init__(self,pos_depart, pos_arrivee, ID_user, born_time,trajectory)
        Car.__init__(self,ID_car,Speed,max_capacity,current_capacity)
        self.riders_list = riders_list
        self.journey = [] # algorithm 1 will fill the journey
        self.first_detour = False
        self.last_detour = False
        self.first_riders = 0
        self.last_riders = 0
        self.detour_rate = detour_rate

    # ______________________Getters and setters ________________________________
    def get_riders_list(self):
        return self.riders_list

    def get_journey(self):
        return self.journey

    def set_journey(self,new_journey):
        self.journey = new_journey

    # function to add a rider
    def add_rider(self,rider: Rider):
        self.riders_list.add(rider)
    
    


