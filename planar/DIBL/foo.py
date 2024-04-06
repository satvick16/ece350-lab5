import numpy as np

# Define the parameters
parameters = {
    "barrel_mean": np.array([0.6, 0.25, 0.8]),
    "ped_mean": np.array([0.9, 0.6, 1.9]),
    "child_mean": np.array([0.3, 0.3, 1.15]),
    "deer_mean": np.array([1.3, 0.5, 1.3]),
    "barricade_mean": np.array([1.5, 0.3, 1.6]),
    "car_mean": np.array([3.40, 1.60, 1.60]),
    "sign_mean": np.array([1.0, 0.3, 1.0]),
    "rail_bar_mean": np.array([3.675, 0.75, 1.25])
}

# Function to calculate Euclidean distance between two vectors
def euclidean_distance(vec1, vec2):
    return np.sqrt(np.sum((vec1 - vec2) ** 2))

distances = []

# Calculate distances between each pair of parameters
for param1 in parameters:
    for param2 in parameters:
        if param1 != param2:
            distance = euclidean_distance(parameters[param1], parameters[param2])
            print(f"Distance between {param1} and {param2}: {distance:.3f}")
            distances.append([[param1, param2], distance])

# Sort the 2D array by the value of the second element in each sublist
sorted_array_2d = sorted(distances, key=lambda x: x[1])

# Print the sorted array
for row in sorted_array_2d:
    if row[0][0] == 'sign_mean' or row[0][1] == 'sign_mean':
        print(row)
