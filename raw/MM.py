import numpy as np

dim = 2
steps = 10

state = [1, 0]
transitionProb = [[0.9, 0.1], [0.3, 0.7]]

state = np.array(state)
transitionProb = np.array(transitionProb)
transitionProb = transitionProb.transpose()

for i in range(steps):
    state = np.dot(transitionProb, state)
    print("Steps: ", i + 1)
    print(state)
    print("-----------------")
    print()
