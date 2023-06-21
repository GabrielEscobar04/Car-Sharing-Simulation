import random
import networkx
from networkx import (
    Graph,
)
from networkx.classes.function import nodes_with_selfloops
from client import Client


VELOCITY = 10
ALPHA = 0.9
MAX_CLIENTS = 2


class Car():
    """
    """
    def __init__(self,
                 id: str,
                 graph: Graph,
                 pos: dict):
        """
        """
        self.id = id
        self.graph = graph
        self.pos = pos
        self.previous_node = random.choice(list(graph.nodes))
        self.edge_progression = 0       
        self.clients_list = []
        self.route = []

    @property
    def next_node(self):
        if self.route:
            return self.route[0]
        return None

    @property
    def position(self):
        if self.next_node:
            return self.pos[self.previous_node] + self.edge_progression*(self.pos[self.next_node]-self.pos[self.previous_node])
        return self.pos[self.previous_node]

    @property
    def current_route_time(self):
        return self.calculate_route_time(self.route)
    
    @property
    def is_full(self):
        return len(self.clients_list) >= MAX_CLIENTS
    
    def assign_new_client(self,
                          new_client: Client):
        """
        """
        self.route = self.compute_route(new_client)
        self.clients_list.append(new_client)

    def compute_route(self,
                      new_client: Client):
        """
        """
        if not self.clients_list:
            print('Individual')
            if self.previous_node == new_client.origin:
                print("PREVIOUS NODE == ORIGIN")
                self.previous_node = list(self.graph[self.previous_node].keys())[0]
            route = self.calculate_route(self.previous_node, new_client.origin)[1:] + self.calculate_route(new_client.origin, new_client.destiny)[1:]
            return route
        print('Shared')
        optimal_route, _, _ = self.optimal_shared_route(self.clients_list[0], new_client)
        return optimal_route

    def compute_cost(self,
                     new_client: Client,
                     empty_car_cost: float = None) -> tuple:
        """
        """
        if not bool(self.clients_list) == bool(empty_car_cost is not None):
            raise AssertionError("Parameter 'empty_car_cost' mut be specified only whenever car.clients_list is not empty.")
        # Case car is empty or car is already occupied
        if not self.clients_list:
            cost1 = self.calculate_time(self.previous_node, new_client.origin)
            cost2 = self.calculate_time(new_client.origin, new_client.destiny)
            #route = self.calculate_route(self.previous_node, new_client.origin) + self.calculate_route(new_client.origin, new_client.destiny)
            return cost1 + cost2
        else:
            _, t_current, t_new = self.optimal_shared_route(self.clients_list[0], new_client)
            return (t_current - self.current_route_time) + (t_new - empty_car_cost)

    def optimal_shared_route(self,
                             client1: Client,
                             client2: Client):
        """
        This function receives both clients as an input and returns the optimal combined route in a list format and the time it takes for each client to reach their destiny
            o1, d1 = first client origin and destiny
            o2, d2 = second client origin and destiny
            
        This function is only called when 2 costumers are looking for the same car, which leads to two possibilities:
            -First client is already in the car --> In this case, the first client origin will be the same as the car position
            -Car is still on its way to pick up the first client --> In this case, the first client origin will be different to the car position
                In order to simplify this case, we always consider origin 1 as the starting position
             
        Given that cars are always between two nodes, the second node in the car route (the node that the car is directed to), will be the car position 
        """
        o1, d1, o2, d2 = client1.origin, client1.destiny, client2.origin, client2.destiny
        base_time = self.calculate_time(self.previous_node, o1)
        
        if self.clients_list[0].is_in_car:
            base_route = []
            o1 = self.previous_node
        else:
            if self.previous_node == o1:
                print("PREVIOUS NODE == ORIGIN")
                self.previous_node = list(self.graph[self.previous_node].keys())[0]
            base_route = self.calculate_route(self.previous_node, o1)[1:]
            
        # option1 = o1 -> o2 -> d1 -> d2
        times_option1 = self.calculate_time(o1, o2), self.calculate_time(o2, d1), self.calculate_time(d1, d2)
        time_option1 = sum(times_option1)
        # option2 = o1 -> o2 -> d2 -> d1
        times_option2 = self.calculate_time(o1, o2), self.calculate_time(o2, d2), self.calculate_time(d2, d1)
        time_option2 = sum(times_option2)
        # option3 = o1 -> d1 -> o2 -> d2
        times_option3 = self.calculate_time(o1, d1), self.calculate_time(d1, o2), self.calculate_time(o2, d2)
        time_option3 = sum(times_option3)
        
        if time_option1 <= time_option2 and time_option1 <= time_option3:
            route = base_route + self.calculate_route(o1, o2)[1:] + self.calculate_route(o2, d1)[1:] + self.calculate_route(d1, d2)[1:]
            return route, base_time + times_option1[0], base_time + time_option1
        elif time_option2 <= time_option3:
            route = base_route + self.calculate_route(o1, o2)[1:] + self.calculate_route(o2, d2)[1:] + self.calculate_route(d2, d1)[1:]
            return route, base_time + time_option2, base_time + times_option2[0] + times_option2[1]
        else:
            route = base_route + self.calculate_route(o1, d1)[1:] + self.calculate_route(d1, o2)[1:] + self.calculate_route(o2, d2)[1:]
            return route, base_time + times_option3[0] + times_option3[1], base_time + time_option3
    
    def calculate_route(self,
                        origin,
                        destiny) -> list:
        """
        """
        route = networkx.shortest_path(self.graph, origin, destiny)
        return route
    
    def calculate_route_time(self,
                             route: list):
        """
        """
        time = 0
        for i in range(len(route)-1):
            edge = self.graph[route[i]][route[i+1]]
            delta = edge['length'] / (edge['max_velocity'] * (ALPHA**edge['num_cars']))
            if i == 0:
                time += self.edge_progression*delta
            else:
                time += delta
        return time          
            
    def calculate_time(self,
                       origin,
                       destiny):
        """
        """
        return self.calculate_route_time(self.calculate_route(origin, destiny))
    
    def move(self,
             now: float,
             interval: float = 1):
        """
        """
        if not self.next_node:
            return
        edge = self.graph[self.previous_node][self.next_node]
        edge_velocity = edge['max_velocity'] * (ALPHA**edge['num_cars'])
        interval_left = ((1-self.edge_progression)*edge['length']) / edge_velocity
        
        if interval > interval_left:
            self.check_new_node(now + (interval_left))
            return self.move(interval - interval_left)
        else:
            delta = (edge_velocity*interval) / edge['length']
            self.edge_progression += delta
            return

    def check_new_node(self,
                       now: float):
        """
        """
        self.graph[self.previous_node][self.next_node]['num_cars'] -= 1
        self.previous_node = self.route.pop(0)
        self.edge_progression = 0
        if self.route:
            self.graph[self.previous_node][self.next_node]['num_cars'] += 1
        # Check clients
        for i, client in enumerate(self.clients_list):
            if not client.is_in_car:
                if client.origin == self.previous_node:
                    client.is_in_car = True
            elif client.destiny == self.previous_node:
                client.is_finished = True
                client.is_in_car = False
                client.finish_time = now
                self.clients_list.pop(i)
                print(f'Client {client} has finished.')
