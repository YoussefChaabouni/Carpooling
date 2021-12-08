from typing import List
import numpy as np
from PersonClasses import Rider, Driver
from graphClasses import Graph
from paper_algorithm_2 import algorithm_2
'''
this algorithm checks the time it takes the rider to reach his destination using algorithm 3

remark :
- algorithm 3 has rider trajectory updates and this one does not
- this is a hypothetical version of algorithm 3
- we will fill the trajectory in the system we will use this function in (current / integrated)
'''

def check_algorithm_3(drivers : List[Driver],rider : Rider,graph : Graph):

    t_prime = np.Infinity
    wt = np.Infinity
    wd = np.Infinity

    best_driver = "no driver"
    #get rider meeting points
    r_org = graph.get_node(rider.pos_depart)
    r_dest = graph.get_node(rider.pos_arrivee)

    m_r_org = graph.get_closest_MP_or_Station(r_org,"MPs").get_id()
    m_r_dest = graph.get_closest_MP_or_Station(r_dest,"MPs").get_id()

    print("CARPOOLING : ")
    for d in drivers:
        #print("algorithm 3 is considering driver = ",d.get_id())
        # get drivers meeting points
        d_org = graph.get_node(d.pos_depart)
        d_dest = graph.get_node(d.pos_arrivee)

        m_d_org = graph.get_closest_MP_or_Station(d_org,"MPs").get_id()
        m_d_dest = graph.get_closest_MP_or_Station(d_dest,"MPs").get_id()

        #print(type(m_d_org))
        '''
        print("m_d_dest = ",m_d_dest)
        print("m_d_org = ",m_d_org)
        print("m_r_dest = ",m_r_dest)
        print("m_r_org = ",m_r_org)
        '''
        if m_d_org == m_r_org and m_d_dest == m_r_dest :
            print("algorithm 2 is considering driver = ",d.get_id())
            print("drivers trajectory = ",d.get_trajectory().node_id_list)
            t_chap,w_chap_t,w_chap_d = algorithm_2(r_org.get_id(),r_dest.get_id(),rider.born_time,d,m_d_org,m_d_dest,graph)
            
            #print(t_chap," ",w_chap_t," ",w_chap_d)
            
            print("      estimated time in carpooling = ",t_chap)
            print("      estimated walking distance in carpooling = ",w_chap_d)
            print("      estimated waiting time in carpooling = ",w_chap_t)
            if w_chap_d <= 2.5 and w_chap_t <= 45 and t_chap < t_prime :
                best_driver = d.get_id()
                t_prime = t_chap
                wd = w_chap_d
                wt = w_chap_t

                # update rider trajectory (WE DO THIS IN paper_algorithm_3.py)
                '''
                Le rider va :
                - marcher jusqu'au meeting point m_r_org
                - prendre une voiture jusqu'à m_r_dest
                - marcher jusqu'à r_dest
                '''
    print("best driver for carpooling option is = ",best_driver)
    return t_prime
