# https: // towardsdatascience.com/k-nearest-neighbor-python-2fccc47d2a55
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import seaborn as sns

sns.set()

# The dataset classifies tumors into two categories (malignant and benign) and
# contains something like 30 features. In the real world, you’d look at the correlations and
# select a subset of features that plays the greatest role in determining whether a tumor is malignant or not.
# However, for the sake of simplicity, we’ll pick a couple at random.
# We must encode categorical data for it to be interpreted by the model (i.e. malignant = 0 and benign = 1).

breast_cancer = load_breast_cancer()
X = pd.DataFrame(breast_cancer.data, columns=breast_cancer.feature_names)
X = X[['mean area', 'mean compactness']]
y = pd.Categorical.from_codes(breast_cancer.target, breast_cancer.target_names)
y = pd.get_dummies(y, drop_first=True)

# As mentioned in another tutorial, the point of building a model, is to classify new data with undefined labels.
# Therefore, we need to put aside data to verify whether our model does a good job at classifying the data.
# By default, train_test_split sets aside 25% of the samples in the original dataset for testing.

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn.fit(X_train, y_train.values.ravel())

# Using our newly trained model, we predict whether a tumor is benign or not given its mean compactness and area.

y_pred = knn.predict(X_test)

sns.scatterplot(
    x='mean area',
    y='mean compactness',
    hue='benign',
    data=X_test.join(y_test, how='outer')
)

plt.scatter(
    X_test['mean area'],
    X_test['mean compactness'],
    c=y_pred,
    cmap='coolwarm',
    alpha=0.7
)
plt.show()

# Another way of evaluating our model is to compute the confusion matrix.
# The numbers on the diagonal of the confusion matrix correspond to correct predictions whereas the others imply false positives and
# false negatives.
# Given our confusion matrix, our model has an accuracy of 121/143 = 84.6%.
# (?) where 143 is the length of one of the arrays (?)
print(confusion_matrix(y_test, y_pred))
