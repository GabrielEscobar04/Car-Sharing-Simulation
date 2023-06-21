import matplotlib.pyplot as plt
import networkx as nx
import csv


AVERAGE_VELOCITY = 10

#Nodes columns index
NODE_ID = 1
NODE_X = 2
NODE_Y = 3

#Edges columns index
EDGE_LENGTH = 3
EDGE_INITIAL_NODE = 6
EDGE_END_NODE = 7
EDGE_DISTRICT_NAME = 9


def generate_graph(edges_filepath: str = r'C:\Users\gaesc\OneDrive\Escritorio\Jesuïtes Casp\TR\ia-aplicada-transport\data\BCN_GrafVial_Trams_ETRS89_CSV.csv',
                   nodes_filepath: str = r'C:\Users\gaesc\OneDrive\Escritorio\Jesuïtes Casp\TR\ia-aplicada-transport\data\BCN_GrafVial_Nodes_ETRS89_CSV.csv',
                   district: str = 'Eixample'):
    """
    """
    G = nx.Graph()
    
    # Read edges and nodes
    with open(edges_filepath) as csv_file:
        edges = csv.reader(csv_file)
        next(edges)
        for edge in edges:
            if edge[EDGE_DISTRICT_NAME] == district:
                initial_node = edge[EDGE_INITIAL_NODE]
                end_node = edge[EDGE_END_NODE]
                G.add_edge(initial_node, end_node)
                G[initial_node][end_node]['length'] = float(edge[EDGE_LENGTH])
                G[initial_node][end_node]['max_velocity'] = AVERAGE_VELOCITY
                G[initial_node][end_node]['num_cars'] = 0
    nodes = list(G.nodes)

    # Read nodes coordinates
    with open(nodes_filepath) as csv_file:
        nodes_positions = csv.reader(csv_file)
        next(nodes_positions)
        pos = {}
        for node in nodes_positions:
            node_id = node[1]
            node_x = float(node[2])
            node_y = float(node[3])
            if node_id in nodes:
                pos[node_id] = (node_x, node_y)   

    return G, pos



if __name__ == '__main__':
    print("Executant...")
    G, pos = generate_graph()
    
    #  No path between N01626I and N10077C.
    print(G['N01626I'])
    
    nx.draw_networkx_nodes(G, pos, node_size=0.5)
    nx.draw_networkx_edges(G, pos, width=0.2, edgelist=G.edges(), arrowsize=2, edge_color="black")
    
    plt.show()
    