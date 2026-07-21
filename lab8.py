from itertools import permutations

INF = float('inf')


def tsp_brute_force(cost, n):
    """Find the optimal TSP tour using brute force."""
    cities = list(range(1, n))
    best_cost = INF
    best_path = None

    for perm in permutations(cities):
        path = [0] + list(perm) + [0]

        total_cost = 0
        valid = True

        for i in range(n):
            if cost[path[i]][path[i + 1]] == INF:
                valid = False
                break
            total_cost += cost[path[i]][path[i + 1]]

        if valid and total_cost < best_cost:
            best_cost = total_cost
            best_path = path

    return best_path, best_cost


# ---------------- Main Program ----------------

n = int(input("Enter number of cities: "))

cities = []
print("\nEnter city names:")
for i in range(n):
    cities.append(input(f"City {i + 1}: "))

print("\nEnter the Cost Matrix")
print("(Enter -1 for INF or diagonal values)")

cost = []

for i in range(n):
    row = list(map(int, input(f"Row {i + 1}: ").split()))

    if len(row) != n:
        print("Error: Enter exactly", n, "values.")
        exit()

    new_row = []

    for value in row:
        if value == -1:
            new_row.append(INF)
        else:
            new_row.append(value)

    cost.append(new_row)


best_path, best_cost = tsp_brute_force(cost, n)

print("\n========== COST MATRIX ==========")

print(f'{"":>6}', end="")
for city in cities:
    print(f"{city:>6}", end="")
print()

for i in range(n):
    print(f"{cities[i]:>6}", end="")
    for j in range(n):
        if cost[i][j] == INF:
            print(f"{'INF':>6}", end="")
        else:
            print(f"{cost[i][j]:>6}", end="")
    print()

print("\n========== RESULT ==========")

if best_path is None:
    print("No valid tour exists.")
else:
    print("Optimal Tour:")
    print(" -> ".join(cities[i] for i in best_path))

    print("\nMinimum Cost:", best_cost)

    print("\nPath Verification:")

    for i in range(n):
        u = best_path[i]
        v = best_path[i + 1]

        print(f"{cities[u]} -> {cities[v]} : Cost = {cost[u][v]}")