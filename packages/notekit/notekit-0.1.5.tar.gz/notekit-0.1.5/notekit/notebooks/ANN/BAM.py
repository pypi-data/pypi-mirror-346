import numpy as np

# Define sign function (to handle bipolar outputs)
def sign(x):
    return np.where(x >= 0, 1, -1)

# Two pairs of vectors (bipolar: elements are -1 or 1)
X1 = np.array([1, -1, 1])
Y1 = np.array([1, 1, -1])

X2 = np.array([-1, 1, -1])
Y2 = np.array([-1, -1, 1])

# Stack pairs into matrices
X = np.vstack([X1, X2])
Y = np.vstack([Y1, Y2])

# Compute weight matrix (outer product sum)
W = np.zeros((X.shape[1], Y.shape[1]))
for i in range(len(X)):
    W += np.outer(X[i], Y[i])

print("Weight Matrix W:")
print(W)

# Function to recall Y from X
def recall_Y(x_input):
    return sign(np.dot(x_input, W))

# Function to recall X from Y
def recall_X(y_input):
    return sign(np.dot(W, y_input))

# Test recall
print("\nRecall Y from X1:")
print(recall_Y(X1))

print("\nRecall Y from X2:")
print(recall_Y(X2))

print("\nRecall X from Y1:")
print(recall_X(Y1))

print("\nRecall X from Y2:")
print(recall_X(Y2))
