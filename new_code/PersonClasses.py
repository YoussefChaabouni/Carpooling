
import sys
from meansClasses import Car
from graphClasses import Trajectory
## USER CLASS

class User:

    # Class constructor
    def __init__(self,pos_depart:int, pos_arrivee:int, ID:int, born_time, trajectory:Trajectory):
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

    def __init__(self, pos_depart, pos_arrivee, ID, born_time):
        super().__init__(pos_depart, pos_arrivee, ID, born_time)
        self.waiting_time = 0
        self.walking_distance = 0
    
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
    def __init__(self, pos_depart, pos_arrivee, ID_user, born_time,
    ID_car,Speed,max_capacity,current_capacity,riders_list=[]):
        User.__init__(pos_depart, pos_arrivee, ID_user, born_time)
        Car.__init__(ID_car,Speed,max_capacity,current_capacity)    
        self.riders_list = riders_list
        

    # ______________________Getters and setters ________________________________
    def get_riders_list(self):
        return self.riders_list
    
    



    
    


