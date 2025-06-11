"""
CPSC 5510, Seattle University, Project #3
:Author: student # Manish Kumar Reddy Challa
:Version: s23
"""
""" Added Extra credit"""
# YOU MAY NOT ADD ANY IMPORTS
from entity import Entity
from student_utilities import to_layer_2
INF = float('inf')


def common_init(self):
    """
    You may call a common function like this from your individual __init__ 
    methods if you want.
    """
    print(f"entity {self.node}: initializing")

    #copy costs from distance table
    self.links = self.distance_table[self.node][:]  
    self.forward = [i for i in range(4)]  
    
    # find immediate neighbots
    self.neighbors = []
    for i in range(4):
        if i != self.node and 0 < self.distance_table[self.node][i] < INF:
            self.neighbors.append(i)
    
    # initial info
    print(f"node: {self.node}")
    for row in self.distance_table:
        formatted_row = [str(int(val)) if val != INF else 'inf' for val in row]
        print("[" + ", ".join(formatted_row) + "]")

    print("  sending costs to neighbors")
    costs = self.distance_table[self.node][:]
    
    # send initial costs to neighbors
    for neighbor in self.neighbors:
        to_layer_2(self.node, neighbor, costs)


def common_update(self, packet):
    """
    You may call a common function like this from your individual update 
    methods if you want.
    """
    print(f"node {self.node}: update from {packet.src} received")
    sender = packet.src
    
    #update distance table with sender's mincosts
    for dest in range(4):
        self.distance_table[sender][dest] = packet.mincost[dest]


    # store curr costs before update
    oldcosts = self.distance_table[self.node][:]
    
    # reset paths
    for dest in range(4):
        if dest != self.node and self.forward[dest] == sender:
            self.distance_table[self.node][dest] = self.links[dest]
            if self.links[dest] < INF:
                self.forward[dest] = dest
            else:
                self.forward[dest] = -1  

    changed = False
    my_direct_cost_to_sender = self.distance_table[self.node][sender]

    for dest in range(4):
        if dest != self.node: 
            curcost = self.distance_table[self.node][dest]
            newcosts = my_direct_cost_to_sender + packet.mincost[dest]
            
            if newcosts < curcost:
                self.distance_table[self.node][dest] = newcosts
                self.forward[dest] = sender 
                changed = True

    # If any changes inform neighbors
    if self.distance_table[self.node] != oldcosts:
        print("  changes based on update")
        print(f"node: {self.node}")
        for row in self.distance_table:
            formatted_row = [str(int(val)) if val != INF else 'inf' for val in row]
            print("[" + ", ".join(formatted_row) + "]")
        
        print("  sending mincost updates to neighbors")
        my_costs = self.distance_table[self.node][:]
        
        for neighbor in self.neighbors:
            to_layer_2(self.node, neighbor, my_costs)
    else:
        print(f"  no changes in node {self.node}, so nothing to do")
        print(f"node: {self.node}")
        for row in self.distance_table:
            formatted_row = [str(int(val)) if val != INF else 'inf' for val in row]
            print("[" + ", ".join(formatted_row) + "]")


def common_link_cost_change(self, to_entity, new_cost):
    """
    You may call a common function like this from your individual 
    link_cost_change methods if you want.
    Note this is only for extra credit and only required for Entity0 and 
    Entity1.
    """
    print(f"node {self.node}: link cost to {to_entity} changed to {new_cost}")
    
    #update direct costs to neighbor
    old_cost = self.links[to_entity]
    self.links[to_entity] = new_cost
    self.distance_table[self.node][to_entity] = new_cost
    

    #Re-eveluate paths
    for dest in range(4):
        if dest != self.node:
            if (self.forward[dest] == to_entity or 
                dest == to_entity):                  
                
                self.distance_table[self.node][dest] = self.links[dest]
                # if direct path else no path
                if self.links[dest] < INF:
                    self.forward[dest] = dest
                else:
                    self.forward[dest] = -1
    
    print(f"node: {self.node}")
    for row in self.distance_table:
        formatted_row = [str(int(val)) if val != INF else 'inf' for val in row]
        print("[" + ", ".join(formatted_row) + "]")
    
    print("  sending costs to neighbors")
    my_costs = self.distance_table[self.node][:]
    for neighbor in self.neighbors:
        to_layer_2(self.node, neighbor, my_costs)


class Entity0(Entity):
    """Router running a DV algorithm at node 0"""
    def __init__(self):
        super().__init__()
        self.node = 0
        INF = float('inf')

        # Initialize
        for i in range(4):
            for j in range(4):
                self.distance_table[i][j] = INF

        self.distance_table[0] = [0, 1, 3, 7]
        
        common_init(self)

    def update(self, packet):
        common_update(self, packet)

    # Link cost change method for Entity0
    def link_cost_change(self, to_entity, new_cost):
        common_link_cost_change(self, to_entity, new_cost)


class Entity1(Entity):
    """Router running a DV algorithm at node 1"""
    def __init__(self):
        super().__init__()
        self.node = 1
        INF = float('inf')

        for i in range(4):
            for j in range(4):
                self.distance_table[i][j] = INF

        self.distance_table[1] = [1, 0, 1, INF]
        
        common_init(self)

    def update(self, packet):
        common_update(self, packet)

    # Link cost change method for Entity1
    def link_cost_change(self, to_entity, new_cost):
        common_link_cost_change(self, to_entity, new_cost) 


class Entity2(Entity):
    """Router running a DV algorithm at node 2"""
    def __init__(self):
        super().__init__()
        self.node = 2
        INF = float('inf')

        for i in range(4):
            for j in range(4):
                self.distance_table[i][j] = INF

        self.distance_table[2] = [3, 1, 0, 2]
        
        common_init(self)

    def update(self, packet):
        common_update(self, packet)


class Entity3(Entity):
    """Router running a DV algorithm at node 3"""
    def __init__(self):
        super().__init__()
        self.node = 3
        INF = float('inf')

        for i in range(4):
            for j in range(4):
                self.distance_table[i][j] = INF

        self.distance_table[3] = [7, INF, 2, 0]
        
        common_init(self)

    def update(self, packet):
        common_update(self, packet)