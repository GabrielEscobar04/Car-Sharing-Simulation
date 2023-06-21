import time 
from generador_mapa_eixample import generador_mapa_eixample
from generador_clients import generador_clients

GRAPH = generador_mapa_eixample()
CARS = generate_cars(MAP) # [car1, car2, ...]
# Car: n_passangers, compute_cost(petition), route
# Route: origin, destiny, steps, calculate_time()

clients = generate_clients() # [petition1, petition2, ...]
# Client: origin, destiny, time, is_assigned, is_finished
current_clients = []
processed_clients = []



now = 0

while clients or current_clients:
    
    current_clients = get_current_clients(clients, now)
    clients.remove(current_clients)
    
    for client in current_clients:

        assigned_car = select_optimal_car(client)
        
        assigned_car.list_of_clients.append(client)
        client.is_assigned = True
        
        processed_clients.append(client)
        
    current_clients = []
    
    now += 1
    

def get_current_clients(clients: list,
                        now: int) -> list:
    """
    """
    return [ client for client in clients if (client.time <= now and
                                              not client.is_assigned and
                                              not client.is_finished) ]
    
    
def select_optimal_car(client: Client):
    """
    """
    empty_cars = [ car for car in CARS if not car.list_of_clients]
    occupied_cars = [ car for car in CARS if car.list_of_clients]
    assert len(CARS) == (len(empty_cars) + len(occupied_cars))
    
    # Compute cost for empty cars
    if empty_cars:
        empty_car_cost = { car : car.compute_cost(client) for car in empty_cars }
        optimal_empty_car = min(empty_car_cost, key=empty_car_cost.get)
        optimal_empty_car_cost = min(empty_car_cost.values())
    else:
        optimal_empty_car = None
        optimal_empty_car_cost = -1
    # Compute cost for occupied cars
    if occupied_cars:
        occupied_car_cost = { car : car.compute_cost(client, optimal_empty_car_cost) for car in occupied_cars }
        optimal_occupied_car = min(occupied_car_cost, key=occupied_car_cost.get)
        optimal_occupied_car_cost = min(optimal_occupied_car.values())
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

