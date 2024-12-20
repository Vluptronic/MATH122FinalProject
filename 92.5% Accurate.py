import sklearn.cluster
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

training_set = pd.read_csv('Training_Set.csv')
testing_set = pd.read_csv('Test_Set.csv')

training_data = training_set.drop(columns=['TYPE'])
diagnoses = training_set['TYPE'].unique()
models = []
centroids = []

for i in diagnoses:
    ind_diagnosis_set = training_set[training_set['TYPE'] == i]
    red_ind_diagnosis_set = ind_diagnosis_set.drop(columns=['TYPE']).values
    if i == "COLD":
        kmean = sklearn.cluster.KMeans(n_clusters=2, init='k-means++', n_init='auto', max_iter=500, tol=0.000001, verbose=0, random_state=None, 
                                  copy_x=True, algorithm='lloyd').fit(red_ind_diagnosis_set)
    elif i == "COVID":
        kmean = sklearn.cluster.KMeans(n_clusters=2, init='k-means++', n_init='auto', max_iter=500, tol=0.000001, verbose=0, random_state=None, 
                                  copy_x=True, algorithm='lloyd').fit(red_ind_diagnosis_set)
    else:
        kmean = sklearn.cluster.KMeans(n_clusters=1, init='k-means++', n_init='auto', max_iter=300, tol=0.000001, verbose=0, random_state=None, 
                                  copy_x=True, algorithm='lloyd').fit(red_ind_diagnosis_set)
    models.append(kmean)
    centroids.append(kmean.cluster_centers_)
    plt.scatter(red_ind_diagnosis_set[:, 0], red_ind_diagnosis_set[:, 1], s=10)
    plt.scatter(kmean.cluster_centers_[0, 0], kmean.cluster_centers_[0, 0], s=200, marker='x', c='red')

plt.title('Diagnoses Clusters')
plt.legend()
plt.show()

test_data = testing_set.drop(columns=['TYPE'])
test_diagnosis_check = testing_set['TYPE'].values
test_data = test_data.values
predicted_labels = []

for test_point in test_data:
    distances = [np.linalg.norm(test_point - centroid) for centroid in centroids]
    predicted_label = diagnoses[np.argmin(distances)]
    predicted_labels.append(predicted_label)

overall_accuracy = np.mean(np.array(predicted_labels) == test_diagnosis_check)
print(f"\nOverall Clustering-based Prediction Accuracy: {overall_accuracy:.4f}")
