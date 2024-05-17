import heapq

def uniform_cost(start, destination, graph):
    pq = [(0, start)]
    visited = set()

    while pq:
        cost, current_node = heapq.heappop(pq)

        if current_node == destination:
            return cost

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            if neighbor not in visited:
                heapq.heappush(pq, (cost + weight, neighbor))

    return float('inf')
