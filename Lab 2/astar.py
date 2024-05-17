import heapq

def astar(graph, start, destination, heuristic):
    open_list = [(0, start)]
    closed_list = set()
    costs = {start: 0}
    came_from = {}

    while open_list:
        current_cost, current_node = heapq.heappop(open_list)

        if current_node == destination:
            # Reconstruct path
            path = []
            while current_node != start:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            path.reverse()
            return current_cost, path, closed_list

        if current_node in closed_list:
            continue

        closed_list.add(current_node)

        for neighbor, distance in graph[current_node].items():
            tentative_cost = costs[current_node] + distance
            if neighbor not in costs or tentative_cost < costs[neighbor]:
                costs[neighbor] = tentative_cost
                total_cost = tentative_cost #+ heuristic[neighbor]
                heapq.heappush(open_list, (total_cost, neighbor))
                came_from[neighbor] = current_node

    return float('inf'), [], closed_list
