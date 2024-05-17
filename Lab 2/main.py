import os
import csv
import networkx as nx
import matplotlib.pyplot as plt
from astar import astar
from breadth_first import breadth_first
from bidirectional_search import bidirectional_search
from depth_first import depth_first
from greedy_best_first_search import greedy_best_first_search
from uniform_cost import uniform_cost

def load_graph_from_csv(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        cities = next(reader)  # Get the list of cities
        for city in cities:
            graph[city] = {}
        for i, row in enumerate(reader):
            for j, value in enumerate(row):
                if value != '-1' and value != '0':
                    graph[cities[i]][cities[j]] = int(value)
    return graph

def print_graph(graph):
    for city, neighbors in graph.items():
        print(f"{city}:")
        for neighbor, distance in neighbors.items():
            print(f"  -> {neighbor}: {distance}")

def visualize_graph(graph):
    G = nx.Graph()
    for city, neighbors in graph.items():
        for neighbor, distance in neighbors.items():
            G.add_edge(city, neighbor, weight=distance)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, font_size=10)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

def visualize_graph_with_path(graph, path, visited):
    G = nx.Graph()
    for city, neighbors in graph.items():
        for neighbor, distance in neighbors.items():
            G.add_edge(city, neighbor, weight=distance)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, font_size=10)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    nx.draw_networkx_nodes(G, pos, nodelist=visited, node_color='r', node_size=700)
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='b', node_size=700)
    
    nx.draw_networkx_edges(G, pos, edgelist=[(path[i], path[i+1]) for i in range(len(path)-1)], edge_color='b', width=2)
    plt.show()

def main():
    file_name = 'map.csv'
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    graph = load_graph_from_csv(file_path)

    print("Graph:")
    print_graph(graph)

    print("Visualizing Graph:")
    visualize_graph(graph)

    start = input("Enter the start city: ")
    destination = input("Enter the destination city: ")

    heuristic = {
        "Arad": 366,
        "Bucharest": 0,
        "Craiova": 160,
        "Drobita": 242,
        "Eforie": 161,
        "Fagaras": 176,
        "Giurgiu": 77,
        "Hirsova": 151,
        "Iasi": 226,
        "Lugoj": 244,
        "Mehedia": 241,
        "Neamt": 234,
        "Oradea": 380,
        "Pitesti": 100,
        "RM": 193,
        "Sibiu": 253,
        "Timisoara": 329,
        "Urziceni": 80,
        "Vaslui": 199,
        "Zerind": 374
    }

    shortest_distance, astar_path , visited = astar(graph, start, destination, heuristic)
    breadth_first_path = breadth_first(graph, start, destination)
    bidirectional_search_path, bidirectional_search_total_cost = bidirectional_search(graph, start, destination)
    depth_first_path = depth_first(start, destination, graph)
    greedy_best_first_search_path, greedy_best_first_search_total_cost = greedy_best_first_search(graph, start, destination, heuristic)
    uniform_cost_path = uniform_cost(start, destination, graph)

    print(f"A-star Path: {astar_path}. The shortest distance from {start} to {destination} is {shortest_distance}")
    print(f"Breadth First Path: {breadth_first_path}. The shortest distance from {start} to {destination} is {shortest_distance}")
    print(f"Bidirectional Search Path: {bidirectional_search_path}. The shortest distance from {start} to {destination} is {bidirectional_search_total_cost}")
    print(f"Depth First Path: {depth_first_path}. The shortest distance from {start} to {destination} is {shortest_distance}")
    print(f"Greedy Best First Search Path: {greedy_best_first_search_path}. The shortest distance from {start} to {destination} is {greedy_best_first_search_total_cost}")
    print(f"Uniform Cost Path: {uniform_cost_path}. The shortest distance from {start} to {destination} is {shortest_distance}")

    print(f"The shortest distance from {start} to {destination} is {shortest_distance}. Path:{astar_path }")

    print("Visited cities:", visited)

    print("Visualizing Graph with Path:")
    visualize_graph_with_path(graph, astar_path, visited)

if __name__ == "__main__":
    main()
