# https://scikit-learn-extra.readthedocs.io/en/latest/generated/sklearn_extra.cluster.KMedoids.html
from sklearn_extra.cluster import KMedoids
import numpy as np

X = np.asarray([[1, 2], [1, 4], [1, 0],
                [4, 2], [4, 4], [4, 0]])
kmedoids = KMedoids(n_clusters=2, random_state=0).fit(X)
print("labels")
print(kmedoids.labels_)

# Predict the closest cluster for each sample in the list of arguments
print("predictions")
print(kmedoids.predict([[0, 0], [4, 4]]))

# Displays the cluster centers, here called medoids, which are points from the original dataset
print("Cluster centers")
print(kmedoids.cluster_centers_)

print("inertia")
print(kmedoids.inertia_)
