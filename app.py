import streamlit as st

def interpolation_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high and arr[low] <= target <= arr[high]:

        if low == high:
            if arr[low] == target:
                return low
            return -1

        pos = low + int(
            ((target - arr[low]) * (high - low))
            / (arr[high] - arr[low])
        )

        if arr[pos] == target:
            return pos

        elif arr[pos] < target:
            low = pos + 1

        else:
            high = pos - 1

    return -1


st.title("Interpolation Search Visualizer")

numbers = st.text_input(
    "Enter sorted numbers separated by commas",
    "2,5,10,15,23,35,48,60,75,90"
)

target = st.number_input("Target Number", value=35)

if st.button("Search"):

    arr = [int(x.strip()) for x in numbers.split(",")]

    result = interpolation_search(arr, target)

    if result != -1:
        st.success(f"Found at index {result}")
    else:
        st.error("Element not found")