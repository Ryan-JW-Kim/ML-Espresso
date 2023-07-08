import matplotlib.pyplot as plt
from random import randint
import numpy as np

class Clusters:

    max_points = 100000
    all_contours = None
    filtered_contours = None
    start_kmeans = False

    @classmethod
    def find_closest_centroid(cls, X, centroids):
        indices = np.zeros(X.shape, dtype=int)

        for i in range(X.shape[0]):
            distances = []
            for j in range(centroids.shape[0]):
                norm = np.linalg.norm(X[i] - centroids[j])
                distances.append(norm)
            
            indices[i] = np.argmin(distances)
    
        return indices
    
    @classmethod
    def init_centroids(cls, K):

        if Clusters.all_contours is not None:
            cent = np.zeros((K, 2))

            for j in range(K):
                i = randint(0, len(cls.all_contours))
                cent[j] = cls.all_contours[i]

            return cent
        
        else:
            raise Exception(f"Error, called before finding contours")
        
    @classmethod
    def update_centroid_position(cls, X, indicies, K):

        m, n = X.shape
        centroids = np.zeros((K, n))

        for k in range(K):
            points = X[indicies==k]
            centroids[k] = np.mean(points, axis=0)

        return centroids
    
    @classmethod
    def run_kmeans(cls, X, initial_centroids, max_iter=10):
        print(X.shape)
        m, n = X.shape

        K = initial_centroids.shape[0]

        centroids = initial_centroids
        indices = np.zeros(m)
        
        for i in range(max_iter):

            indices = cls.find_closest_centroid(X, centroids)
            centroids = cls.update_centroid_position(X, indices, K)
        
        return centroids, indices