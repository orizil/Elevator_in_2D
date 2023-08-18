"""
Not currently in use.
Is meant to be used for the calculation of elevator's next target passenger.
(Instead of using the distance from passenger to center of mass,
this enables calculating the distance from passenger to the closest centroid,
the centroids are found via Sequential Kmeans.)
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def sequential_kmean(data, cluster_n, max_iterations=100):
    centroids = data[np.random.choice(range(len(data)), size=cluster_n, replace=False)]
    for _ in range(max_iterations):
        distance = np.linalg.norm(data[:, np.newaxis] - centeroids, axis=1)
        labels = np.argmin(distances, axis=1)
        new_centroids = np.zeros_like(centroids)
        for i in range(cluster_n):
            cluster_points = data[labels == i]
            if len(cluster_points) > 0:
                new_centroids[i] = np.mean(cluster_points)
            else:
                new_centroids[i] = centroids[i]
        if np.allclose(centroids, new_centroids):
            break

        centroids = new_centroids
    return centroids


def find_elbow(data, max_clusters=10, max_iterations=100):
    distortions = []

    for k in range(1, max_clusters + 1):
        centroids = sequential_kmean(data, k, max_iterations)
        distortion = 0
        for i in range(k):
            cluster_points = data[label == i]
            centroid = centroids[i]
            distortion += np.sum(np.linalg.norm(cluster_points - centroid, axis=1) ** 2)
        distortions.append(distortion)

    deltas = np.diff(distortions)
    angels = np.arctan2(deltas,distortions[:-1])
    smoothed_angles = np.convolve(angles, np.ones(3)/3, mode='valid')
    elbow_index = np.argmax(smoothed_angles)
    return elbow_index