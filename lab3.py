import heapq

# ---------- Union-Find for Kruskal ----------
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # Path Compression
        return self.parent[x]

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)

        if rx == ry:
            return False

        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx

        self.parent[ry] = rx

        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        return True


# ---------- Kruskal Algorithm ----------
def kruskal(n, edges):
    edges = sorted(edges)

    uf = UnionFind(n)

    mst = []
    total_cost = 0

    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            total_cost += w

            if len(mst) == n - 1:
                break

    return mst, total_cost


# ---------- Prim Algorithm ----------
def prim(n, adj, start=0):

    visited = [False] * n
    pq = [(0, start, -1)]

    mst = []
    total_cost = 0

    while pq:

        weight, node, parent = heapq.heappop(pq)

        if visited[node]:
            continue

        visited[node] = True

        if parent != -1:
            mst.append((parent, node, weight))
            total_cost += weight

        for neighbour, w in adj[node]:
            if not visited[neighbour]:
                heapq.heappush(pq, (w, neighbour, node))

    return mst, total_cost


# ---------- Graph ----------
n = 7

edges = [
    (7, 0, 1),
    (5, 0, 3),
    (8, 1, 2),
    (9, 1, 3),
    (7, 1, 4),
    (5, 2, 4),
    (15, 3, 4),
    (6, 3, 5),
    (8, 4, 5),
    (9, 4, 6),
    (11, 5, 6)
]

adj = {i: [] for i in range(n)}

for w, u, v in edges:
    adj[u].append((v, w))
    adj[v].append((u, w))

kruskal_mst, kruskal_cost = kruskal(n, edges)
prim_mst, prim_cost = prim(n, adj)

print("===== KRUSKAL'S MST =====")
for u, v, w in kruskal_mst:
    print(f"{u} -- {v}   Weight = {w}")

print("Total Cost =", kruskal_cost)

print("\n===== PRIM'S MST =====")
for u, v, w in prim_mst:
    print(f"{u} -- {v}   Weight = {w}")

print("Total Cost =", prim_cost)