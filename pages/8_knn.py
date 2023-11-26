from indicator_functions import *
from st_plot_functions import *
from st_functions import *
from functions import *

from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score

# Generating synthetic dataset
X, y = make_classification(n_samples=100, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1, n_classes=3, random_state=42)


# Generating synthetic dataset with a matrix of features for each instance
num_samples = 4
num_features = 2
mins = 7
num_classes = 3

# Creating X as a list of matrices, where each matrix represents features for an instance
X = []
for _ in range(num_samples):
    instance_matrix = np.random.rand(num_features, mins)  # Example matrix for features
    X.append(instance_matrix)

X

# Creating y as random class labels
y = np.random.randint(0, num_classes, num_samples)

# Convert X to a numpy array
X = np.array(X)

X

# Reshaping X to flatten the matrices into vectors
X_flattened = X.reshape(num_samples, -1)


X_flattened



# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Creating KNN classifier
knn = KNeighborsClassifier()

# Parameters to try in grid search
parameters = {'n_neighbors': [3, 5, 7, 9, 11]}  # You can expand this list for more values of k

# Performing grid search with cross-validation
grid_search = GridSearchCV(knn, parameters, cv=5)
grid_search.fit(X_train, y_train)

# Getting the best k value
best_k = grid_search.best_params_['n_neighbors']

# Using the best k to train the final model
best_knn = KNeighborsClassifier(n_neighbors=best_k)
best_knn.fit(X_train, y_train)

# Making predictions on the test set using the best model
predictions = best_knn.predict(X_test)

# Calculating accuracy
accuracy = accuracy_score(y_test, predictions)
f"Best k: {best_k}"
f"Accuracy of KNN Classifier with best k: {accuracy:.2f}"
