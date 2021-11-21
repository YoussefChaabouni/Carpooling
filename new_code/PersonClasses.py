
import sys

## USER CLASS

class User:

    # Class constructor
    def __init__(self,pos_depart,pos_arrivee,ID,born_time):
        self.born_time = born_time
        self.id = ID
        self.pos_depart = pos_depart
        self.pos_arrivee = pos_arrivee
    

    ########## GETTERS AND SETTERS #########################
    def __repr__(self):
        return "User : "+str(self.id)
    
    def get_id(self):
        return self.id

    def get_pos_depart(self):
        return self.pos_depart
    
    def get_pos_arrivee(self):
        return self.pos_arrivee

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
    