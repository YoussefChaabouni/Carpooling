


from PersonClasses import Rider
from graphClasses import Graph
from PersonClasses import Driver

## IMPORTANT CONSTANTS
alpha = 0.7 
vot = 20

def rider_cost_p(r: Rider,speed,G : Graph):

    org = G.get_node(r.pos_depart)
    dst = G.get_node(r.pos_arrivee)
    distance = G.get_distance(org,dst)
    Kpark = 10 #random for now

    return distance*(alpha + vot/speed) + Kpark

def price_to_pay(r: Rider,speed,G : Graph):

    ptp = rider_cost_p(r,speed,G) - vot*pool_time(r,G)
    #print("price to pay = ",ptp)
    #print("rider cost p = ",rider_cost_p(r,speed,G))
    #print("value of time and pool time = ",vot*pool_time(r,G))
    return rider_cost_p(r,speed,G) - vot*pool_time(r,G)

def pool_time(rider: Rider,graph:Graph):

    trajectory = rider.get_trajectory()
    means_list = trajectory.means_list
    drivers = [x for x in means_list if type(x) == Driver]

    encoding = ["org","MPorg","Mprime","Sorg","Sdst","Mseconde","MPdst","dst"]

    relative_boarding = rider.relative_boarding
    relative_alighting = rider.relative_alighting

    ins = []
    outs = []

    for i in range(len(relative_boarding)):
        if relative_boarding[i] == 1 :
            ins.append(encoding[i])
        if relative_alighting[i] == 1 :
            outs.append(encoding[i])

    t_pool = 0

    r_org = graph.get_node(rider.pos_depart)
    r_dst = graph.get_node(rider.pos_arrivee)

    print("________________rider = ",rider.id,"__________________")

    for i in range(len(drivers)):

        org_d = graph.get_node(drivers[i].pos_depart)
        #print(" class of d_org in alg1 = ",type(org_d))
        dst_d = graph.get_node(drivers[i].pos_arrivee)

        # prendre les meeting points les plus proches
        m_org_d = graph.get_closest_MP_or_Station(org_d,"MPs")
        m_dst_d = graph.get_closest_MP_or_Station(dst_d,"MPs")
        # prendre les stations les plus proches
        s_org_d = graph.get_closest_MP_or_Station(org_d,"Stations")
        s_dst_d = graph.get_closest_MP_or_Station(dst_d,"Stations")

        if ins[i] =="org":
            start = org_d
        if ins[i] =="MPorg":
            start = m_org_d
        if ins[i] == "Mseconde":
            s_r_dest = graph.get_closest_MP_or_Station(r_dst,"Stations")
            start = graph.get_closest_MP_or_Station(s_r_dest,"MPs")
        if ins[i] == "Sdst" :
            start = s_dst_d
        if outs[i] == "Mprime":
            s_r_org = graph.get_closest_MP_or_Station(r_org,"Stations")
            
            finish = graph.get_closest_MP_or_Station(s_r_org,"MPs")
        if outs[i] == "Sorg" :
            finish = s_org_d
        if outs[i] == "MPdst" :
            finish = m_dst_d
        if outs[i] == "dst" :
            finish = dst_d

        

        t_pool += graph.get_distance(start,finish)/drivers[i].speed
    if drivers != [] :
        print("drivers = ",drivers)
        print("ins = ",ins)
        print("outs = ",outs)
        print("total distance = ",t_pool*drivers[0].speed)

    return t_pool#trajectory.arr_time_list[-1] - trajectory.arr_time_list[0]

def driver_added_cost(d: Driver,G: Graph):

    
    detour = compute_detour(d,G)

    return detour*(alpha + vot)



def compute_detour(d:Driver,G:Graph):
    
    org = G.get_node(d.pos_depart)
    dst = G.get_node(d.pos_arrivee)
    trajectory = d.get_trajectory()

    direct_time = G.get_distance(org,dst)/d.speed
    actual_time = trajectory.arr_time_list[-1] - trajectory.arr_time_list[0]

    return actual_time - direct_time 

def profit(riders,drivers,G):

    money_received_by_riders = 0
    money_paid_to_drivers = 0 

    speed = drivers[0].speed

    for r in riders :
        print("______for rider : ",r.id,"______________")
        if r.solution == "integrated" and "carpooling":
            money_received_by_riders += price_to_pay(r,speed,G)
    
    for d in drivers :
        if min(d.current_capacity) < 4 :
            print("______driver : ",d.id,"___________")
            print("driver current capacity = ",d.current_capacity)
            money_paid_to_drivers += driver_added_cost(d,G)
    
    print("money_received = ",money_received_by_riders)
    print("money paid = ",money_paid_to_drivers)
    return money_received_by_riders - money_paid_to_drivers






