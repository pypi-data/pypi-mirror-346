print(""" 

import numpy as np
import matplotlib.pyplot as plt

# 1. Generate Synthetic Data
def generate_data(n=200):
    X = np.random.rand(n, 2)  # 2D input features
    # Label = 1 if both features > 0.5 (damaged), else 0 (safe)
    y = ((X[:, 0] > 0.5) & (X[:, 1] > 0.5)).astype(int)
    return X, y

# 2. NSA Classifier (Negative Selection Algorithm)
class NSAClassifier:
    def __init__(self, num_detectors=50, radius=0.1):
        self.num_detectors = num_detectors
        self.radius = radius
        self.detectors = []

    def train(self, X_self):
        # Generate detectors far from self (safe) region
        while len(self.detectors) < self.num_detectors:
            candidate = np.random.rand(2)
            if all(np.linalg.norm(candidate - x) > self.radius for x in X_self):
                self.detectors.append(candidate)

    def predict(self, X):
        predictions = []
        for x in X:
            # If within radius of any detector => "damaged" (non-self)
            if any(np.linalg.norm(x - d) <= self.radius for d in self.detectors):
                predictions.append(1)
            else:
                predictions.append(0)  # "safe"
        return np.array(predictions)

# 3. Training and Testing
X, y = generate_data(n=200)
split = int(0.8 * len(X))  # 80% training, 20% testing
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

X_self = X_train[y_train == 0]  # Self class: safe data
clf = NSAClassifier(num_detectors=50, radius=0.1)
clf.train(X_self)

y_pred = clf.predict(X_test)

# 4. Evaluation
accuracy = np.mean(y_pred == y_test)
print(f"Accuracy: {accuracy:.4f}")

# 5. Visualization
plt.figure(figsize=(8, 6))
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_pred, cmap='coolwarm', edgecolor='k', label='Predicted')
plt.scatter(np.array(clf.detectors)[:, 0], np.array(clf.detectors)[:, 1], 
            c='green', marker='x', label='Detectors')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('AIS Damage Classification (Red=Damaged, Blue=Safe)')
plt.legend()
plt.grid(True)
plt.show()


""")