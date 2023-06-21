import time
from graph import (
    generate_graph,
)
from car import (
    Car,
)
from client import (
    Client,
    generate_clients,
)


GRAPH, POS = generate_graph()
NODES = list(GRAPH.nodes())
EDGES = list(GRAPH.edges())

NUM_CARS = 50
MAX_PASSENGERS = 2
NUM_CLIENTS = 50

T_MAX = 24*60*60
INTERVAL = 5


"""
Helper functions
"""
def clock_format(s):
    return '{:02}:{:02}:{:02}'.format(s // 3600, s // 60 % 60, s % 60)

def show_info(clients: list,
              cars: list):
    """
    clients: han demanat / 50, estan en cotxe / 50, han acabar / 50
    per cada client: cotxe assignat, origen, desti, route del cotxe (ordenat per cotxe, millor)
    
    cars: quants client assignat / 50, quants tenen client / 50, quants estan plens / 50
    """
    assigned_clients = [client for client in clients if client.is_assigned]
    clients_in_car = [[client for client in clients if client.is_in_car]]
    finished_clients = [client for client in assigned_clients if client.is_finished]
    
    assigned_clients_oa = str(len(assigned_clients)) + "/" + str(len(clients))
    clients_in_car_oa = str(len(clients_in_car)) + "/" + str(len(clients))
    finished_clients_oa = str(len(finished_clients)) + "/" + str(len(clients))
    
    print("| Assigned Clients | Clients in Car | Finished Clients |")
    print(f"| {assigned_clients_oa} {' '*(15-len(assigned_clients_oa))} | {clients_in_car_oa} {' '*(13-len(clients_in_car_oa))} | {finished_clients_oa} {' '*(15-len(finished_clients_oa))} |")




"""
Program execution
"""  
def get_current_clients() -> list:
    """
    """
    global now
    return [ client for client in clients if (client.petition_time <= now and
                                              not client.is_assigned and
                                              not client.is_finished) ]

    
def select_optimal_car(client: Client):
    """
    """
    if not any([not car.is_full for car in cars]):
        return None
    
    empty_cars = [ car for car in cars if not car.clients_list and not car.is_full]
    occupied_cars = [ car for car in cars if car.clients_list and not car.is_full]
    assert len([car for car in cars if not car.is_full]) == (len(empty_cars) + len(occupied_cars))
    
    # Compute cost for empty cars
    if empty_cars:
        empty_car_cost = { car : car.compute_cost(client) for car in empty_cars }
        optimal_empty_car = min(empty_car_cost, key=empty_car_cost.get)
        optimal_empty_car_cost = min(empty_car_cost.values())
    else:
        optimal_empty_car = None
        optimal_empty_car_cost = -1
    # Compute cost for occupied cars
    print(optimal_empty_car_cost)
    if occupied_cars:
        occupied_car_cost = { car : car.compute_cost(client, optimal_empty_car_cost) for car in occupied_cars }
        optimal_occupied_car = min(occupied_car_cost, key=occupied_car_cost.get)
        optimal_occupied_car_cost = min(occupied_car_cost.values())
    else:
        optimal_occupied_car = None
        optimal_occupied_car_cost = -1
        
    # Select best car
    ## No cars of one type
    if not optimal_empty_car:
        return optimal_occupied_car
    elif not optimal_occupied_car:
        return optimal_empty_car
    # Cars of both types
    elif optimal_empty_car_cost < optimal_occupied_car_cost:
        return optimal_empty_car
    else:
        return optimal_occupied_car




"""
MAIN.
Client generation
Car generation
"""
clients = generate_clients(GRAPH, n=NUM_CLIENTS)
cars = [Car(f'car-{i}', GRAPH, POS) for i in range(NUM_CARS)]
print('CLIENTS:')
for client in clients:
    print(f'{client.petition_time}  --  {client.origin}, {client.destiny}')
print('\nCARS:')
for car in cars:
    print(f'{car.previous_node}')


assigned_clients = []
finished_clients = []
global now
now = 0
i = 0

print('\nStarting simulation')
while len(finished_clients) < len(clients):# and now <= T_MAX:
    
    # Process clients that have been activated and not yet assigned
    current_clients = get_current_clients()
    #if current_clients:
        #print('\nNEW ITERATION')
        #print(f'Time: {clock_format(now)}. Assigned clients: {len(assigned_clients)}/{NUM_CLIENTS}. Finished clients: {len(finished_clients)}/{NUM_CLIENTS}.')
        #print(f'New clients: {len(current_clients)}:')
    for client in current_clients:
        #print(f'  * {clock_format(client.petition_time)} -- {client.origin}, {client.destiny}')
        assigned_car = select_optimal_car(client)
        assigned_car.assign_new_client(client)
        client.assigned_car = assigned_car
        client.is_assigned = True
        assigned_clients.append(client)
        #print(f'     Assigned car initial node: {assigned_car.previous_node}')
        #print(f'     Assigned car route {assigned_car.route}')
    current_clients = []
    # Move finished clients from assigned to finished
    finished_clients = [client for client in assigned_clients if client.is_finished]
    assigned_clients = [client for client in clients if client.is_assigned]
    
    for car in cars:
        car.move(now, INTERVAL)
    # Update the time
    now += INTERVAL
    i += 1
    if i % 48*8 == 0:
        #print([len(car.route) for car in cars])
        print('\nNEW ITERATION')
        print(f'Time: {clock_format(now)}. Assigned clients: {len(assigned_clients)}/{NUM_CLIENTS}. Finished clients: {len(finished_clients)}/{NUM_CLIENTS}.')
        print(f'Clients in car: {len([client for client in clients if client.is_in_car])}')
        print(len([client for client in clients if (client.is_assigned and not client.is_in_car and not client.is_finished and not (client.origin in client.assigned_car.route))]))
        print(len([car for car in cars if car.is_full]))
        show_info(clients, cars)
        #time.sleep(0.001)


  



