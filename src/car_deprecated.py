import networkx as nx
from generador_mapa_eixample import generador_mapa_eixample


GRAPH = generador_mapa_eixample()[0]
NODES = list(GRAPH.nodes())


class Car:
    
    def __init__(self,
                 graph=GRAPH):
        """
        """
        self.graph = graph
        self.position = graph.random_node()
        self.list_of_clients = []
        self.route = []
        
    def compute_cost(self,
                     new_client: Client,
                     empty_car_cost: Optional[float]):
        """
        """
        # Comprovar que tinc cost empty si el cotxe esta opccupied
        if not bool(self.list_of_clients) == bool(empty_car_cost):
            raise AssertionError()
        
        if not self.list_of_clients:
            cost1 = self.calculate_time(self.position, new_client.origin)
            cost2 = self.calculate_time(new_client.origin, new_client.destiny)
            return cost1 + cost2
        
        else:
            optimal_route, t_current, t_new = self.optimal_shared_route(self.list_of_clients[0], new_client)
            return (t_current - self.current_time) + (t_new - empty_car_cost)

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
        base_time = self.calculate_time(self.position, o1)
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
            route = self.calculate_route(o1, o2) + self.calculate_route(o2, d1) + self.calculate_route(d1, d2)
            return route, base_time + times_option1[0], base_time + time_option1
        elif time_option2 <= time_option3:
            route = self.calculate_route(o1, o2) + self.calculate_route(o2, d2) + self.calculate_route(d2, d1)
            return route, base_time + time_option2, base_time + times_option2[0] + times_option2[1]
        else:
            route = self.calculate_route(o1, d1) + self.calculate_route(d1, o2) + self.calculate_route(o2, d2)
            return route, base_time + times_option3[0] + times_option3[1], base_time + time_option3
    
    def calculate_route(self,
                        origin: node,
                        destiny: node) -> list:
        """
        """
        nx.find_shortest_path(self.graph, origin, destiny)
        return self.route

    def calculate_route_time(self,
                             route: list):
        """
        """
        time = 0
        for i, step in enumerate(route):
            if i < len(route)-1:
                edge = self.graph.get_edge(step[i], step[i+1])
                time += edge.time
        return time
            
    def calculate_time(self,
                       origin: node,
                       destiny: node):
        """
        """
        return self.calculate_route_time(self.calculate_route(origin, destiny))
            
    @property
    def current_time(self):
        return self.calculate_route_time(self.route)

    def move(self):
        pass
    