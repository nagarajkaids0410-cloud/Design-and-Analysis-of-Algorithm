def first_fit(items, capacity=1.0):
    bins = []              # Remaining space in each bin
    bin_contents = []      # Items in each bin

    for item in items:
        placed = False

        for i, space in enumerate(bins):
            if space >= item:
                bins[i] -= item
                bin_contents[i].append(item)
                placed = True
                break

        if not placed:
            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


def first_fit_decreasing(items, capacity=1.0):
    sorted_items = sorted(items, reverse=True)
    return first_fit(sorted_items, capacity)


def best_fit_decreasing(items, capacity=1.0):
    sorted_items = sorted(items, reverse=True)

    bins = []
    bin_contents = []

    for item in sorted_items:
        best_idx = -1
        best_space = float("inf")

        for i, space in enumerate(bins):
            if space >= item and (space - item) < best_space:
                best_space = space - item
                best_idx = i

        if best_idx != -1:
            bins[best_idx] -= item
            bin_contents[best_idx].append(item)
        else:
            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


def display_bins(label, bin_list):
    print(f"\n{label}: {len(bin_list)} bins")

    for i, b in enumerate(bin_list, start=1):
        used = sum(b)
        bar = "#" * int(used * 20)

        print(f"Bin {i}: {b}")
        print(f"Used: {used:.2f} [{bar:<20}]")


# ---------------- Main Program ----------------

items = list(map(float, input("Enter items (comma separated): ").split(",")))
capacity = float(input("Enter bin capacity: "))

lower_bound = int(-(-sum(items) // capacity))  # Ceiling division

print("\nItems:", items)
print("Capacity:", capacity)
print("Total Size:", sum(items))
print("Lower Bound:", lower_bound)

ff_bins = first_fit(items, capacity)
ffd_bins = first_fit_decreasing(items, capacity)
bfd_bins = best_fit_decreasing(items, capacity)

display_bins("First Fit (FF)", ff_bins)
display_bins("First Fit Decreasing (FFD)", ffd_bins)
display_bins("Best Fit Decreasing (BFD)", bfd_bins)

print("\n========== Summary ==========")
print(f"Lower Bound : {lower_bound}")
print(f"First Fit   : {len(ff_bins)} bins")
print(f"FFD         : {len(ffd_bins)} bins")
print(f"BFD         : {len(bfd_bins)} bins")