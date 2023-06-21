import random
from networkx import Graph


SECONDS_IN_HOUR = 3600
T_MAX = 24*SECONDS_IN_HOUR
HOURS = list(range(24))
HOUR_WEIGHTS = (0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.4, 0.6, 0.6, 0.6, 0.4, 0.2, 0.2, 0.3, 0.4, 0.6, 0.6, 0.6, 0.4, 0.4, 0.2, 0.2, 0.1)
NUM_CLIENTS = 50

     
def generate_clients(graph: Graph,
                     n: int = NUM_CLIENTS,
                     t_max: int = T_MAX):
    """
    """
    clients = []
    for _ in range(n):
        nodes = list(graph.nodes)
        origin = random.choice(nodes)
        nodes.remove(origin)
        destiny = random.choice(nodes)
        petition_time = random.choices(HOURS, weights=HOUR_WEIGHTS)[0]*SECONDS_IN_HOUR + random.randrange(0, SECONDS_IN_HOUR)
        client = Client(origin, destiny, petition_time)
        clients.append(client)
    return clients


class Client():
    """
    """
    def __init__(self,
                 origin: int,
                 destiny: int,
                 petition_time: int):
        """
        """
        self.origin = origin
        self.destiny = destiny
        self.petition_time = petition_time

        self.is_assigned = False
        self.is_finished = False
        self.assigned_car = None
        self.is_in_car = False

        self.finish_time = None
        
    @property
    def node(self):
        if self.in_car:
            return self.assigned_car.node
        if self.is_finished:
            return self.destiny
        return self.origin
    
    @property
    def duration(self):
        if not self.finish_time:
            return None
        return self.finish_time - self.petition_time

        
