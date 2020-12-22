import numpy as np

dim = 2
steps = 10

state = [0.5, 0.5]
transitionProb = [[0.7, 0.3], [0.3, 0.7]]
emissionProb = [[0.9, 0.1], [0.2, 0.8]]

state = np.array(state)

transitionProb = np.array(transitionProb)
transitionProb = transitionProb.transpose()

emissionProb = np.array(emissionProb)
emissionProb = emissionProb.transpose()


for i in range(steps):
    print("Steps: ", i + 1)
    print("Advance Time")
    state = np.dot(transitionProb, state)
    print(state)
    print("Improve by evidence")
    state = emissionProb[0] * state
    state /= np.sum(state)
    print(state)
    print("----------------------------")
    print()

