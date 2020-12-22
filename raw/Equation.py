import numpy as np

coEfficient = [[0.1, -0.3], [1, 1]]
constant = [0, 1]

coEfficient = np.array(coEfficient)
constant = np.array(constant)

solve = np.dot(np.linalg.inv(coEfficient), constant)

print(solve)
