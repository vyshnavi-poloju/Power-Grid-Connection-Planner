from graph import graph

# ---------------- KRUSKAL ----------------
parent = {}
rank = {}

def find(node):
    if parent[node] != node:
        parent[node] = find(parent[node])
    return parent[node]

def union(u, v):
    root_u = find(u)
    root_v = find(v)

    if root_u != root_v:
        if rank[root_u] > rank[root_v]:
            parent[root_v] = root_u
        else:
            parent[root_u] = root_v
            if rank[root_u] == rank[root_v]:
                rank[root_v] += 1

def kruskal(graph):
    edges = []

    for u in graph:
        for v in graph[u]:
            edges.append((graph[u][v], u, v))

    edges.sort()

    for node in graph:
        parent[node] = node
        rank[node] = 0

    mst = []
    total_cost = 0

    for cost, u, v in edges:
        if find(u) != find(v):
            union(u, v)
            mst.append((u, v, cost))
            total_cost += cost

    return mst, total_cost


# ---------------- DIJKSTRA ----------------
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    pq = [(0, start)]

    while pq:
        current_dist, node = heapq.heappop(pq)

        for neighbor in graph[node]:
            distance = current_dist + graph[node][neighbor]

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances


# ---------------- VISUALIZATION ----------------
def draw_graph(graph, title="Graph"):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()

    for u in graph:
        for v in graph[u]:
            G.add_edge(u, v, weight=graph[u][v])

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000)

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title(title)
    plt.show()


# ---------------- MAIN ----------------
if __name__ == "__main__":

    # ---- ORIGINAL GRAPH ----
    print("\n========== ORIGINAL NETWORK ==========")
    draw_graph(graph, "Original Power Grid")

    # ---- MST ----
    mst, total_cost = kruskal(graph)

    print("\n--- Minimum Cost Power Network (MST) ---")
    for u, v, cost in mst:
        print(f"{u} ➝ {v}  | Cost = {cost}")

    print("Total Cost =", total_cost)

    # ---- SHORTEST PATH ----
    print("\n--- Shortest Paths from A ---")
    distances = dijkstra(graph, 'A')
    for node in distances:
        print(f"A ➝ {node} = {distances[node]}")

    # ---- FAILURE SIMULATION ----
    print("\n========== FAILURE: Removing B-D ==========")

    # Remove edge
    graph['B'].pop('D')
    graph['D'].pop('B')

    draw_graph(graph, "After Failure (B-D Removed)")

    print("\n--- New Shortest Paths from A ---")
    new_distances = dijkstra(graph, 'A')
    for node in new_distances:
        print(f"A ➝ {node} = {new_distances[node]}")
