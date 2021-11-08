##STG: Spatio Temporal Graph Shortest_path_dijkstra
##ariabbas

from csvWriter import CSVWriter # this imported class is written by me

import sys
import pickle
import random
import csv
import datetime as dt

from operator import attrgetter 
from datetime import timedelta
from math import sqrt, ceil

## Gobal var 
WALKING_SPEED = 3000 #3km/h
CAR_SPEED = 40000 #40km/h
##



## Person can be Rider or Driver 
## type is RIDER__ or DRIVER
        
class Person:
    def __init__(self, dt, person_id, person_name, x_o, y_o, x_d, y_d, kind):
        self.born_time = dt
        self.id = person_id
        self.name = person_name
        self.x_org = x_o
    	self.y_org = y_o
    	self.x_dst = x_d
    	self.y_dst = y_d
        self.type = kind
        
        
    def get_id(self):
        return self.id
    
    def get_time(self):
        return self.born_time
    
    def get_kind(self):
        return self.type
    
    def get_walkingspeed(self):
        global WALKING_SPEED
        return WALKING_SPEED
    
    def get_carspeed(self):
        global CAR_SPEED
        return CAR_SPEED
    
  
 
    def compute_sqr(self, a):
        return a*a
 
    def compute_distance(self,x1,y1,x2,y2):
        return sqrt(self.compute_sqr(y2-y1)+self.compute_sqr(x2-x1))
        
    
    def get_fsationdist(self, aVertex):
        #print self.compute_distance(self.x_org, self.y_org, aVertex.get_x(), aVertex.get_x())
        return self.compute_distance(self.x_org, self.y_org, aVertex.get_x(), aVertex.get_x())

    def get_walkingtime(self, aVertex):
        # walking time = distance / walking speed
        #print self.get_fsationdist(aVertex)
        # return in Minutes we can also return in seconds (*3600)
        print self.get_fsationdist(aVertex)
        return (self.get_fsationdist(aVertex)/self.get_walkingspeed())*60
        
     #def get_lsationdist(self, aVertex):
        # walking time = distance / walking speed
        
        #####TODO
 
class Carpooler:
    def __init__(self):
        self.carpooler_dict = {}
        self.num_carpoolers = 0
    
    def __iter__(self):
        return iter(self.carpooler_dict.values())	
        
    def add_carpooler(self, dt, carpooler_id, carpooler_name, x_o, y_o, x_d, y_d, kind):
        new_carpooler = Person(dt, carpooler_id, carpooler_name,x_o, y_o, x_d, y_d, kind)
        self.carpooler_dict[carpooler_id] = new_carpooler
        return new_carpooler

    def get_carpooler(self, n):
        if n in self.carpooler_dict:
            return self.carpooler_dict[n]
        else:
            return None
    #return (self.vert_dict[to].time - self.vert_dict[frm].time).total_seconds()
               


# 2 constructors classes: Vertex and Graph
# class Vertex: definition of all methods associated with nodes
# class Graph: use the class Vertex to construct a graph

## In our context
#node is (time,Ido_of_station)
# An example of node is (08:03,Id_of_Massy-Palaiseau)
#weight=trip time


class Vertex:
    def __init__(self, dt, node_id, node_name, x_n, y_n, kind):
        # node: id of the station
        # t is the train departure time 
        self.x = x_n
        self.y = y_n
        self.type = kind
        self.time = dt
        self.id = node_id
        self.name = node_name
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxint
        # Mark all nodes unvisited        
        self.visited = False  
        # Predecessor
        self.previous = None
        
    def __repr__(self):
        return repr((self.x, self.y, self.type, self.time, self.id, self.name, 
                     self.adjacent,self.distance, self.visited, self.previous))

        
    def add_neighbor(self, node_id, weight=0):
        # neighbor node
        ## remove weight in this function
        #weight = self.add_weight(neighbor)
        self.adjacent[node_id] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def get_weight(self, node_id):
        return self.adjacent[node_id]

    def set_distance(self, dist):
        self.distance = dist
    
    def get_time(self):
        return self.time
    
    def get_kind(self):
        return self.type

    # get_distance(self) return of total_weight, i.e., the cost of the shortest path
    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        # prev is the previous node
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.node_id) + str(self.time) + ' adjacent: ' + str([x.node_id for x in self.adjacent])

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, dt, node_id, node_name, x_n, y_n, kind):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(dt, node_id, node_name, x_n, y_n, kind)
        self.vert_dict[node_id] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None
        
    # define the methods to compute the weights 
    # The edges related to journey j1 are (5h08, z1)-->(5h11, z4),
    # (5h11, z4)-->(5h11, z4),(5h11, z4)-->(5h12, z5),
    # (5h12, z5)-->(5h14, z6), (5h14, z6)-->(5h16, z8)
    # The weights of such arcs are 5h11-5h08=3min, 5h12-5h11=1min, 
    # 5h14-5h12=2min, 5h16-5h14=2min, respectively.
    def add_weight(self, frm, to):
        #x.time = self.adjacent.time
        return (self.vert_dict[to].time - self.vert_dict[frm].time).total_seconds()
        
        #a = dt.datetime(2020,02,10,00,37,59)
        #b = dt.datetime(2020,02,10,00,39,59)
        #timedelta = b-a
        #(b-a).total_seconds()

    def add_edge(self, frm, to, cost = 0):
    #def add_edge(self, frm, to):
        #
        #cost = self.add_weight(frm, to)
        # dt, node_id, node_name, x_n, y_n, kind
        if frm not in self.vert_dict:
            ## TODO
            #self.add_vertex(dt, frm, node_name, x_n, y_n, kind)
            self.add_vertex(dt,frm)
        if to not in self.vert_dict:
            ## TODO
            #self.add_vertex(dt, to, node_name, x_n, y_n, kind)
            self.add_vertex(dt,to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        #self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return

import heapq


 
def dijkstra(aGraph, start):
    print '''Dijkstra's shortest path'''
    #print 'Sart_dijsktra_'+start.get_id()
    # Set the distance for the start node to zero 
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue =[]
    for v in aGraph:
        tt = start.get_id()
        uu = v.get_id()
        #print yu[1]
        if len(tt) > 2:
            if (tt[1] == uu[1]) and (tt[2] == uu[2]):
                unvisited_queue.append((v.get_distance(),v))
            else:
                None  
        else:
            if (tt[1] == uu[1]):
                unvisited_queue.append((v.get_distance(),v))
            else:
                None
                
            
    #unvisited_queue = [(v.get_distance(),v) for v in aGraph]
    #print unvisited_queue
    heapq.heapify(unvisited_queue)
    #t_cost = 0
    while len(unvisited_queue):
        # Pops a vertex with the smallest distance 
        uv = heapq.heappop(unvisited_queue)
        #print uv
        current = uv[1]
        current.set_visited()
        
        #for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            #if current.get_time():
                
            new_dist = current.get_distance() + current.get_weight(next)
            
            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                #print current.get_id()
                print 'updated : current = %s next = %s new_dist = %s' \
                        %(current.get_id(), next.get_id(), next.get_distance())
                #t_cost = next.get_distance()
            else:
                print current.get_id()
                print 'not updated : current = %s next = %s new_dist = %s' \
                        %(current.get_id(), next.get_id(), next.get_distance())
                        
                #t_cost = next.get_distance()
                
        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        #unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
        
        unvisited_queue =[]
        for v in aGraph:
            if not v.visited: 
                tt = start.get_id()
                uu = v.get_id()
                #print yu[1]
                if len(tt) > 2:
                    if (tt[1] == uu[1]) and (tt[2] == uu[2]):
                        unvisited_queue.append((v.get_distance(),v))
                    else:
                        None  
                else:
                    if (tt[1] == uu[1]):
                        unvisited_queue.append((v.get_distance(),v))
                    else:
                        None
            else:
                None
                
        #transform the list into unvisited_queue a heap
        heapq.heapify(unvisited_queue)
 
    
def daterange(start_date, end_date, n):
    #for n in range(int ((end_date - start_date).datetime)):
        #yield start_date + timedelta(minutes=n)
    q = start_date
    while q < end_date:
        #yield start_date + timedelta(minutes=n)
        q = q + timedelta(minutes=n)
        yield q

     
    

if __name__ == '__main__':
    
    start_date = dt.datetime(2020,02,10,7,35,00)
    end_date = dt.datetime(2020,02,10,8,35,00)
    born_date = dt.datetime(2020,02,10,7,38,00)
    frequences = [5,10,30,60]
    ## two graphs: s_g for all stations train and d_g for the direct train
    s_g = Graph()
    d_g = Graph()
    
    
    ## Carpoolers  
    carpoolers = Carpooler()
    
    
    
        

    #weight_matrix[x][y] is the weight, i.e. the time, from a stop i to j, 
    # e.g. weight_matrix[0][1] is the weight from the stop a to stop b. 
    #line=column=a,b,c,d,e,f,g,h,i ,ie, stop
    # -1 value means there is no egde between the that stop
    weight_matrix = [[-1, 3, 4, -1, -1, -1, -1, -1, -1],
                     [3, -1, 2, -1, -1, -1, -1, -1, -1],
                     [4, 2, -1, 2, -1, 2, -1, -1, -1],
                     [-1, -1, 2, -1, 3, -1, -1, -1, -1],
                     [-1, -1, -1, 3, -1, 1, -1, -1, -1],
                     [-1, -1, 2, -1, 1, -1, 3, -1, 2],
                     [-1, -1, -1, -1, -1, 3, -1, 2, -1],
                     [-1, -1, -1, -1, -1, -1, 2, -1, 2],
                     [-1, -1, -1, 3, -1, 2, -1, 2, -1],
                     ]
                     
        
    # all station a train each 3 minutes   
    for freq in frequences:
        myinter = CSVWriter('data/times'+str(freq)+'+.csv')
        myinter.write(("WalT","WaiT","TraT"))
        i = 0
        for single_date in daterange(start_date, end_date, freq):
            #print single_date
            s_weight_sum = 0
            s_g.add_vertex(single_date, 'a'+str(i), 'a', 1, 1, '_ALL_')
            
            s_weight_sum = weight_matrix[0][1]
            s_g.add_vertex(single_date + timedelta(minutes = s_weight_sum), 'b'+str(i), 'b', 1, 1, '_ALL_')
            
            s_weight_sum = s_weight_sum + weight_matrix[1][2]
            s_g.add_vertex(single_date + timedelta(minutes=s_weight_sum), 'c'+str(i), 'c', 1, 1, '_ALL_')
            
            s_weight_sum = s_weight_sum + weight_matrix[2][3]
            s_g.add_vertex(single_date + timedelta(minutes=s_weight_sum), 'd'+str(i), 'd', 1, 1, '_ALL_')
            
            s_weight_sum = s_weight_sum + weight_matrix[3][4]
            s_g.add_vertex(single_date + timedelta(minutes=s_weight_sum), 'e'+str(i), 'e', 1, 1, '_ALL_')
           
            s_weight_sum = s_weight_sum + weight_matrix[4][5]
            s_g.add_vertex(single_date + timedelta(minutes=s_weight_sum), 'f'+str(i), 'f', 1, 1, '_ALL_')
            
            s_weight_sum = s_weight_sum + weight_matrix[5][6]
            s_g.add_vertex(single_date + timedelta(minutes=s_weight_sum), 'g'+str(i), 'g', 1, 1, '_ALL_')
            
            s_weight_sum = s_weight_sum + weight_matrix[6][7]
            s_g.add_vertex(single_date + timedelta(minutes=s_weight_sum), 'h'+str(i), 'h', 1, 1, '_ALL_')
            
            s_weight_sum = s_weight_sum + weight_matrix[7][8]
            s_g.add_vertex(single_date + timedelta(minutes=s_weight_sum), 'i'+str(i), 'i', 1, 1, '_ALL_')
            
            i += 1
        
            
        
        # direct train each 7 min
        j = i+1
        for single_date in daterange(start_date, end_date, freq+3):
            d_weight_sum = 0
            d_g.add_vertex(single_date, 'a'+str(j), 'a', 1, 1, '_DIRECT_')
            
            d_weight_sum = weight_matrix[0][1]
            d_g.add_vertex(single_date + timedelta(minutes=d_weight_sum), 'c'+str(j), 'c', 1, 1, '_DIRECT_')
            
            d_weight_sum = d_weight_sum + weight_matrix[2][5]
            d_g.add_vertex(single_date + timedelta(minutes=d_weight_sum), 'f'+str(j), 'f', 1, 1, '_DIRECT_')
            
            d_weight_sum = d_weight_sum + weight_matrix[5][8]
            d_g.add_vertex(single_date + timedelta(minutes=d_weight_sum), 'i'+str(j), 'i', 1, 1, '_DIRECT_')
            
            j += 1
        
        
        # add edges all stations train   
        for l in range(0,i):
            s_g.add_edge('a'+str(l),'b'+str(l),weight_matrix[0][1])
            s_g.add_edge('b'+str(l),'c'+str(l),weight_matrix[1][2])
            s_g.add_edge('c'+str(l),'d'+str(l),weight_matrix[2][3])
            s_g.add_edge('d'+str(l),'e'+str(l),weight_matrix[3][4])
            s_g.add_edge('e'+str(l),'f'+str(l),weight_matrix[4][5])
            s_g.add_edge('f'+str(l),'g'+str(l),weight_matrix[5][6])
            s_g.add_edge('g'+str(l),'h'+str(l),weight_matrix[6][7])
            s_g.add_edge('h'+str(l),'i'+str(l),weight_matrix[7][8])
    
        # add edges direct train
        for k in range(i+1,j):
            d_g.add_edge('a'+str(k), 'c'+str(k),weight_matrix[0][2])
            d_g.add_edge('c'+str(k), 'f'+str(k),weight_matrix[2][5])
            d_g.add_edge('f'+str(k), 'i'+str(k),weight_matrix[5][8])
            
            
        ## Print Graphs information    
        print 'Graph data: all stations train'
        for v in s_g:
            #print v.get_time()
            #for w in v.get_id():
            for w in v.get_connections():
                vid = v.get_id()
                wid = w.get_id()
                
                
                print '( %s , %s, %3d), %s'  % ( vid, wid, v.get_weight(w), v.get_time())
                #print '( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w))
        print 'Graph data: direct train'
        for v in d_g:
            #print v.get_time()
            for w in v.get_connections():
                vid = v.get_id()
                wid = w.get_id()
                
                
                print '( %s , %s, %3d), %s'  % ( vid, wid, v.get_weight(w), v.get_time())
                #print '( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w))
                
        # if the ouptut  stop is for the all stations train, compute dijkstra(s_g, s_g.get_vertex('a'))
        # else compute dijkstra(s_g, s_g.get_vertex('a')) and dijkstra(d_g, s_g.get_vertex('a'))
        # then compare the two obtained costs and choose the smalest     
        
            
        ## TODO: Write a method to find the near (station,time) according to 
        ## the born time of a carpooler and the time to reach this station
        carpoolers_walkingtime = {}
        
        for i in range(0,100):
            delta_born = born_date + timedelta(minutes = random.randrange(0, 5, 1))
            
            carpoolers.add_carpooler(delta_born,'p'+str(i), 'p', 
                                     -900 + random.randrange(0, 500, 1), 
                                     -500 + random.randrange(0, 400, 1), 
                                     100, 100, 'RIDER')
            z = carpoolers.get_carpooler('p'+str(i)).get_id()
            
            ## Create Riders
            # while true
            
            vect_node = []
            #waiting_time = []
            ## TODO in the for loop replace s_g by the node near the carpooler, i.e.,
            # the set of (station, time) of a station, e.g., if it's the sation a, then
            # set of these node should be (a0,t0), (a1,t1), ..., (a5, t5,); (a6, t6), ...
            ## 
            for u in s_g:
                # Forcing: to force the station a to be the near station. 
                # This will be fixed when the above TODO will be achieved
                if (u.get_name() == 'a') and (u.get_kind() == '_ALL_'):
                    #s_g_cp = s_g_cp.
                    carpoolers_walkingtime[z] = carpoolers.carpooler_dict[z].get_walkingtime(u)
                    www = delta_born + timedelta(minutes = carpoolers_walkingtime[z])
                    #print delta_born, www, carpoolers_walkingtime[z]
                    
                    if www < u.get_time():
                        vect_node.append(u.get_id())
                        #waiting_time.append(u.get_time() - www)
                        #print www, u.get_time()
                    else:
                        None
                    #print vect_node
                        
                else:
                    None
                
            vv = []
            for k in range(0,len(vect_node)):
                vv.append(s_g.vert_dict[vect_node[k]])
            
            # sort  the vector of nodes (station, time) "near" the passenger 
            # with a time >= of the carpooler estimated arrival time at the 
            # departure (station, time) 
            
            vect_sort = sorted(vv, key=attrgetter('time'))
            
            xu = vect_sort[0]
            yu = vect_sort[0].get_id()
            
            dijkstra(s_g, s_g.get_vertex(yu))
            ## TODO find the last stop near the destination
            # for the moment, let'u fix the last station 
            target = s_g.get_vertex('e'+yu[1])
            path = [target.get_id()]
            shortest(target, path)
            print 'The shortest path : %s' %(path[::-1])
            
            
            
            #c = target.get_distance()
            #mycost = CSVWriter('costs.csv')
            myinter = CSVWriter('data/times'+str(freq)+'+.csv')
            cid = carpoolers.get_carpooler('p'+str(i)).get_id()
            cborn = carpoolers.get_carpooler('p'+str(i)).get_time()
            time_stop = xu.get_time()
            #s_g.get_vertex(yu).get_time()
            
            time_walk = (cborn + timedelta(minutes = ceil(carpoolers_walkingtime[cid])))
        
            
            waiting_time = (time_stop - time_walk).total_seconds()/60
            
            print time_stop, cborn, time_walk, waiting_time
            
            walking_time = ceil(carpoolers_walkingtime[cid])
            train_time = target.get_distance()
            ccost = walking_time + waiting_time + train_time
            print 'Rider %s Walking Time: %s, Waiting Time: %s, Train Time: %s' %(cid, walking_time, waiting_time, train_time) 
            print 'Total Cost : %s' %ccost
            
            #myinter.write((cborn, cborn + timedelta(minutes = ccost)))
            myinter.write((walking_time, waiting_time, train_time))
            myinter.close()
            
            #mycost.write((cid, path[::-1], ccost))
            #mycost.close()

    
    
  

    