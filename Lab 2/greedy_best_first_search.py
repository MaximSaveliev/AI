import heapq

def greedy_best_first_search(graph, start, destination, heuristic):
    open_list = [(heuristic[start], start)]
    came_from = {}
    cost_so_far = {start: 0}

    while open_list:
        _, current_node = heapq.heappop(open_list)

        if current_node == destination:
            # Reconstruct path and calculate total cost
            path = []
            total_cost = 0
            while current_node != start:
                path.append(current_node)
                total_cost += heuristic[current_node]
                current_node = came_from[current_node]
            path.append(start)
            path.reverse()
            return path, total_cost

        for neighbor in graph[current_node]:
            new_cost = cost_so_far[current_node] + heuristic[neighbor]
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                heapq.heappush(open_list, (heuristic[neighbor], neighbor))
                came_from[neighbor] = current_node
                cost_so_far[neighbor] = new_cost

    return [], float('inf')
