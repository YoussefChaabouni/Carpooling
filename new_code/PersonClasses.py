
import sys
from Carpooling.new_code.meansClasses import Car
from Carpooling.new_code.graphClasses import Trajectory
## USER CLASS

class User:

    # Class constructor
    def __init__(self,pos_depart,pos_arrivee,ID,born_time,trajectory : Trajectory):
        self.born_time = born_time
        self.id = ID
        self.pos_depart = pos_depart
        self.pos_arrivee = pos_arrivee
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
        self.walking_time = 0
    
    ###### UPDATE WALKING AND WAITING TIMES ##########
    def update_waiting_time(self, waiting_duration):

        ## we could verify that the waiting duration is a positive integer
        if(waiting_duration >= 0):
            self.waiting_time += waiting_duration 
        else :
            sys.exit("waiting durations should always be positive")

    def update_walking_time(self, walking_duration):

        ## we could verify that the walking duration is a positive integer
        if(walking_duration >= 0):
            self.walking_time += walking_duration 
        else :
            sys.exit("walking durations should always be positive")

class Driver(User,Car):
    
    #_______________ init with a riders_list_____________________________
    def __init__(self, pos_depart, pos_arrivee, ID_user, born_time,
    ID_car,Speed,max_capacity,current_capacity,riders_list):
        User.__init__(pos_depart, pos_arrivee, ID_user, born_time)
        Car.__init__(ID_car,Speed,max_capacity,current_capacity)    
        self.riders_list = riders_list
        self.journey = [] # algorithm 1 will fill the journey
    
    # _____________________ init without a riders_list ________________________
    def __init__(self, pos_depart, pos_arrivee, ID_user, born_time,
    ID_car,Speed,max_capacity,current_capacity):
        User.__init__(pos_depart, pos_arrivee, ID_user, born_time)
        Car.__init__(ID_car,Speed,max_capacity,current_capacity)    
        self.riders_list = [] 
        self.journey = [] # algorithm 1 will fill the journey

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
    
    


