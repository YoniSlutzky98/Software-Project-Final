import sys
import numpy as np
import pandas as pd
import spkmeansmodule as spk
np.random.seed(0)
MAT_OPS = ("wam", "ddg", "lnorm", "jacobi") # designated words for matrix operations.

'''
The function receives the input from the user, validates its length and validates the goal requested.
'''
def receive_input():
    assert len(sys.argv) == 4
    try:
        k = int(sys.argv[1])
    except:
        assert 1 == 0
    assert((sys.argv[2] in MAT_OPS) or (sys.argv[2] == "spk")) # Validate the goal
    return k, sys.argv[2], sys.argv[3]

'''
The function finds the distance of the closest centroid to x.
The distance is measured using the euclidean distance.
The function assumes the dimension of the centroids and of x is the same.
'''
def find_closest_distance(x, centroids):
    minimal_distance = sum((x-centroids[0]) ** 2)
    for i in range(1, len(centroids)):
        minimal_distance = min(minimal_distance, sum((x-centroids[i]) ** 2))
    return minimal_distance

'''
The function implements the kmeans++ algorithm.
The function uses weights to randomly choose the first K centroids from the observations.
The weights are assigned with regards to the euclidean distance from current centroids.
'''
def kmeanspp(k, obs):
    indices = [np.random.choice(range(len(obs)))]
    centroids = np.array([obs[indices[0]]])
    for i in range(1, k):
        distances = np.array([find_closest_distance(obs[j], centroids) for j in range(len(obs))])
        s = sum(distances)
        probs = distances / s
        rand_index = np.random.choice(range(len(obs)), p=probs)
        indices.append(rand_index)
        centroids = np.append(centroids, np.array([obs[rand_index]]), axis = 0)
    return centroids, indices

'''
The function receives a matrix, and prints it row by row using a comma as a delimiter between elements.
'''
def print_mat(mat):
    for i in range(len(mat)):
        print(','.join(["%.4f" % elem for elem in mat[i]]))
        
def main():
    try:
        k, goal, file_path = receive_input() # Receive and validate input
    except(AssertionError):
        print("Invalid Input!")
        return
    try:
        obs = pd.read_csv(file_path, header=None)
        obs = obs.to_numpy()
        n, d = obs.shape[0], obs.shape[1]
        assert(-1 < k < n)
    except(AssertionError):
        print("Invalid Input!")
        return
    except:
        print("An Error Has Occurred")
        return
    if goal in MAT_OPS: # If a matrix operation is desired
        result = spk.apply_mat_ops(goal, n, d, obs.tolist())
        try:
            assert(result != None)
            print_mat(result)
        except(AssertionError):
            print("An Error Has Occurred")
            return
    else: # Else, full normalized spectral kmeans is desired
        lnorm = spk.apply_mat_ops("lnorm", n, d, obs.tolist()) # Calculate lnorm
        try:
            assert(lnorm != None)
        except(AssertionError):
            print("An Error Has Occurred")
            return
        jacobi = spk.apply_mat_ops("jacobi", n, n, lnorm) # Calculate e-values and e-vectors
        try:
            assert(jacobi != None)
        except(AssertionError):
            print("An Error Has Occurred")
            return
        T = spk.apply_kmeans_prep(n, k, jacobi) # Normalize e-vectors and find best heuristic k
        try:
            assert(T != None)
        except(AssertionError):
            print("An Error Has Occurred")
            return
        try:
            k = len(T[0])
            initial_centroids, indices = kmeanspp(k, T) # Initialize kmeans++ with T and k
            print(",".join([str(elem) for elem in indices])) # Print initial indices
            final_centroids = spk.apply_kmeans(len(T), len(T[0]), k, 300, 0.0, 
                                                initial_centroids.tolist(), T) # Perform kmeans
            assert(final_centroids != None)
            print_mat(final_centroids)
            return
        except(AssertionError):
            print("An Error Has Occurred")
            return

if __name__ == "__main__":
    main()