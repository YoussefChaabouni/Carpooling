


from typing import List
from PersonClasses import Driver,Rider
from graphClasses import Graph, Trajectory
import numpy as np
from helperFunctions import Drive, walk
from meansClasses import Foot

from paper_algorithm_2 import algorithm_2


def algorithm_3(drivers : List[Driver],rider : Rider,graph : Graph):

    t_prime = np.Infinity
    wt = np.Infinity
    wd = np.Infinity

    #get rider meeting points
    r_org = graph.get_node(rider.pos_depart)
    r_dest = graph.get_node(rider.pos_arrivee)

    m_r_org = graph.get_closest_MP_or_Station(r_org,"MPs").get_id()
    m_r_dest = graph.get_closest_MP_or_Station(r_dest,"MPs").get_id()


    for d in drivers:

        # get drivers meeting points
        d_org = graph.get_node(d.pos_depart)
        d_dest = graph.get_node(d.pos_arrivee)

        m_d_org = graph.get_closest_MP_or_Station(d_org,"MPs").get_id()
        m_d_dest = graph.get_closest_MP_or_Station(d_dest,"MPs").get_id()

        print(type(m_d_org))
        print("m_d_dest = ",m_d_dest)
        print("m_d_org = ",m_d_org)
        print("m_r_dest = ",m_r_dest)
        print("m_r_org = ",m_r_org)

        if m_d_org == m_r_org and m_d_dest == m_r_dest :
            
            t_chap,w_chap_t,w_chap_d = algorithm_2(r_org.get_id(),r_dest.get_id(),rider.born_time,d,m_d_org,m_d_dest,graph)
            
            print(t_chap," ",w_chap_t," ",w_chap_d)
            if w_chap_d <= 2500 and w_chap_t <= 45*60 and t_chap < t_prime :
                
                t_prime = t_chap
                wd = w_chap_d
                wt = w_chap_t



                # update rider information
                rider.update_waiting_time(wt)
                rider.update_walking_distance(wd)

                # update rider trajectory
                '''
                Le rider va :
                - marcher jusqu'au meeting point m_r_org
                - prendre une voiture jusqu'à m_r_dest
                - marcher jusqu'à r_dest
                '''
                arrival_time_m_r_org = rider.born_time + walk(r_org,graph.get_node(m_r_org),graph,5) # arrivée à m_r_org
                departure_time_m_r_org = arrival_time_m_r_org + wt #départ de m_r_org
                arrival_time_m_r_dest = departure_time_m_r_org + Drive(graph.get_node(m_r_org),graph.get_node(m_r_dest),graph,40) # arrivée à m_r_dest
                departure_time_m_r_dest = arrival_time_m_r_dest # départ de m_r_dest
                arrival_time_r_dest = departure_time_m_r_dest + walk(graph.get_node(m_r_dest),r_dest,graph,5) #arrivée à r_dest
                departure_time_r_dest = arrival_time_r_dest # départ de r_dest

                ## new_mean : Mean_of_transportation,new_arr_time,new_dep_time,new_node_id : int
                rider.get_trajectory().update_trajectory(Foot(ID=m_r_org,Speed=5),arrival_time_m_r_org,departure_time_m_r_org,m_r_org)
                rider.get_trajectory().update_trajectory(d,arrival_time_m_r_dest,departure_time_m_r_dest,m_r_dest)
                rider.get_trajectory().update_trajectory(Foot(ID = r_dest.get_id(),Speed=5),arrival_time_r_dest,departure_time_r_dest,r_dest.get_id())

    return t_prime