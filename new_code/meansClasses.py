
import sys
from typing import List



class Mean_of_transportation:
    def __init__(self,ID,Speed):
        self.id = ID
        self.speed = Speed
    
    #_____________________________ GETTERS AND SETTERS_________________________________"


    def get_id(self):
        return self.id
    
    def get_speed(self):
        return self.speed
    
    def set_speed(self,new_speed):
        
        ## Check if the speed is strictly positive
        if(new_speed > 0):
            self.speed = new_speed
        else:
            sys.out("A speed should always be strictly positive for means of transportation")
        

class Car(Mean_of_transportation):

    #_________________CLASS CONSTRUCTOR__________________________
    def __init__(self, ID, Speed=40,max_capacity=4,current_capacity=[]):
        super().__init__(ID, Speed)
        self.max_capacity = max_capacity
        self.current_capacity = current_capacity

    #___________________GETTERS AND SETTERS___________________________
    def get_max_capacity(self):
        return self.max_capacity

    def get_current_capacity(self):
        return self.current_capacity   
    
    def set_max_capacity(self,new_max_capacity):
        # we check if it is above zero
        if(new_max_capacity > 0):
            self.max_capacity = new_max_capacity
        else:
            sys.out("Maximum capacity of a car should always be a positive integer")
        
    def set_current_capacity(self,new_current_capacity: List):

         self.current_capacity = new_current_capacity
        
    
class Train(Mean_of_transportation):
         #_________________CLASS CONSTRUCTOR__________________________
    def __init__(self, ID, Speed=80,max_capacity=1000,current_capacity=1000):
        super().__init__(ID, Speed)
        self.max_capacity = max_capacity
        self.current_capacity = current_capacity

    #___________________GETTERS AND SETTERS___________________________
    def get_max_capacity(self):
        return self.max_capacity

    def get_current_capacity(self):
        return self.current_capacity   
    
    def set_max_capacity(self,new_max_capacity):
        # we check if it is above zero
        if(new_max_capacity > 0):
            self.max_capacity = new_max_capacity
        else:
            sys.out("Maximum capacity of a train should always be a positive integer")
        
    def set_current_capacity(self,new_current_capacity):
        # we check that this is positive
        if(new_current_capacity >= 0):
            self.current_capacity = new_current_capacity
        else:
            sys.out("Current capacity of a train can't be negative!!")   
    

class Foot(Mean_of_transportation):

    ##___________________ CLASS CONSTRUCTOR ________________________
    def __init__(self, ID, Speed=5):
        super().__init__(ID, Speed)

