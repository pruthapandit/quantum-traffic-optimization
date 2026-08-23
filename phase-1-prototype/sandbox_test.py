import numpy as np
qubit = np.array([0.707106, 0.707106])
print("My Qubit State:", qubit)

# Square every element in the array instantly
probabilities = qubit ** 2
print("Probabilities:", probabilities)

# Sum the elements to see if they equal 1
total_probabiltiy = np.sum(probabilities)
print("Total Probability (Should be ~1.0):", total_probabiltiy)

#Create a 2D rotation matrix
# [ [cos(theta), -sin(theta)], [sin(theta), cos(theta)] ]
rotation_matrix = np.array([[0.965, -0.258], [0.258, 0.965]])

# Multiply the matrix by your qubit to update its state
# In NumPy, '@' is used for matrix multiplication
new_qubit = rotation_matrix @ qubit
print("Updated Qubit State after rotation:", new_qubit)

