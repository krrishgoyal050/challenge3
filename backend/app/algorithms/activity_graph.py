from collections import deque
import heapq


ActivityGraph = dict[str, dict[str, float]]


DEFAULT_GRAPH: ActivityGraph = {
    "transport": {"energy": 2.0, "shopping": 4.0},
    "energy": {"food": 2.5, "waste": 1.5},
    "food": {"waste": 1.0, "shopping": 2.0},
    "shopping": {"waste": 1.2},
    "waste": {},
}


def bfs(graph: ActivityGraph, start: str) -> list[str]:
    seen = {start}
    order: list[str] = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, {}):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return order


def dfs(graph: ActivityGraph, start: str) -> list[str]:
    seen: set[str] = set()
    order: list[str] = []

    def visit(node: str) -> None:
        seen.add(node)
        order.append(node)
        for neighbor in graph.get(node, {}):
            if neighbor not in seen:
                visit(neighbor)

    visit(start)
    return order


def dijkstra(graph: ActivityGraph, start: str, target: str) -> tuple[float, list[str]]:
    distances = {node: float("inf") for node in graph}
    previous: dict[str, str | None] = {node: None for node in graph}
    distances[start] = 0.0
    heap: list[tuple[float, str]] = [(0.0, start)]
    while heap:
        distance, node = heapq.heappop(heap)
        if node == target:
            break
        if distance > distances[node]:
            continue
        for neighbor, weight in graph.get(node, {}).items():
            candidate = distance + weight
            if candidate < distances.get(neighbor, float("inf")):
                distances[neighbor] = candidate
                previous[neighbor] = node
                heapq.heappush(heap, (candidate, neighbor))

    path: list[str] = []
    node: str | None = target
    while node is not None:
        path.append(node)
        node = previous.get(node)
    path.reverse()
    return distances[target], path
