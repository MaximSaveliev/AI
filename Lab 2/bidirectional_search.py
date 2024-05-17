import heapq

def bidirectional_search(graph, start, destination):
    # If the start and destination nodes are the same, return the path with a distance of 0
    if start == destination:
        return [start], 0

    # Initialize data structures for forward and backward searches
    forward_open_list = [(0, start)]
    backward_open_list = [(0, destination)]
    forward_came_from = {start: None}
    backward_came_from = {destination: None}
    forward_cost_so_far = {start: 0}
    backward_cost_so_far = {destination: 0}
    meeting_node = None
    meeting_cost = float('inf')

    while forward_open_list and backward_open_list:
        # Forward search step
        forward_cost, forward_node = heapq.heappop(forward_open_list)
        if forward_node in backward_came_from:
            meeting_node = forward_node
            meeting_cost = forward_cost + backward_cost_so_far[forward_node]
            break

        for neighbor, cost in graph[forward_node].items():
            new_cost = forward_cost + cost
            if neighbor not in forward_cost_so_far or new_cost < forward_cost_so_far[neighbor]:
                forward_cost_so_far[neighbor] = new_cost
                forward_came_from[neighbor] = forward_node
                heapq.heappush(forward_open_list, (new_cost, neighbor))

        # Backward search step
        backward_cost, backward_node = heapq.heappop(backward_open_list)
        if backward_node in forward_came_from:
            meeting_node = backward_node
            meeting_cost = backward_cost + forward_cost_so_far[backward_node]
            break

        for neighbor, cost in graph[backward_node].items():
            new_cost = backward_cost + cost
            if neighbor not in backward_cost_so_far or new_cost < backward_cost_so_far[neighbor]:
                backward_cost_so_far[neighbor] = new_cost
                backward_came_from[neighbor] = backward_node
                heapq.heappush(backward_open_list, (new_cost, neighbor))

    # Reconstruct the path if a meeting node is found
    if meeting_node:
        forward_path = reconstruct_path(forward_came_from, meeting_node)
        backward_path = reconstruct_path(backward_came_from, meeting_node)
        backward_path.reverse()  # Reverse the backward path
        return forward_path[:-1] + backward_path, meeting_cost
    else:
        return [], float('inf')

def reconstruct_path(came_from, node):
    path = []
    while node:
        path.append(node)
        node = came_from[node]
    return path[::-1]  # Reverse the path
