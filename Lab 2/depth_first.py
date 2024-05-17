def depth_first(start, destination, graph):
    stack = [(start, [start])]

    while stack:
        current, path = stack.pop()
        if current == destination:
            return path
        for neighbor in graph[current]:
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor]))

    return []
