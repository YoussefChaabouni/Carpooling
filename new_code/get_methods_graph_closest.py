import numpy as np

# POUR LA CLASSE NODE
# ------------------------------- #
def get_xy_coordinate(self):
    return np.array([self.x_coordinate,self.y_coordinate])
# ------------------------------- #


# POUR LA CLASSE GRAPH
# ------------------------------- #
def get_closest_MP_or_Station(self,nodes): # on prend en entrée une liste de nodes

    V = np.zeros((len(nodes),2))

    for i,n in enumerate(nodes):
        V[i] = nodes.get_xy_coordinate()

    org_x,dst_x = np.meshgrid(V[:,0],V[:,0])
    org_y,dst_y = np.meshgrid(V[:,1],V[:,1])

    # pour éviter que la node se choisisse elle-même comme node la plus proche on rajoute un poid de +infini sur la diagonale de la matrice des distances²
    I = np.diag([np.inf]*len(nodes))

    argmin_distance = np.argmin((org_x-dst_x)**2 + (org_y-dst_y)**2 + I,axis=0)

    return argmin_distance
# ------------------------------- #