"""
QuantumAnomalyDetector
-----------------------
A simple anomaly detection model based on minimum Euclidean distance to training data.

Supports multivariate inputs. Can be used as a classical proxy for quantum behavior.

"""

import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

class QuantumAnomalyDetector:
    """
    A basic anomaly detector that uses distance to the nearest training sample
    as an anomaly score. Thresholding this score allows for classification.
    """

    def __init__(self, threshold=2.5):
        """
        Initialize the detector.

        Parameters:
        ----------
        threshold : float
            The decision threshold above which a score is considered anomalous.
        """
        self.threshold = threshold
        self.training_data = None

    def fit(self, X):
        """
        Fit the model with training data.

        Parameters:
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data assumed to contain only normal samples.
        """
        self.training_data = np.array(X)
        if self.training_data.ndim == 1:
            self.training_data = self.training_data.reshape(-1, 1)

    def predict(self, X, batch_size=512):
        """
        Predict anomaly scores in safe memory-efficient batches.

        Parameters:
        ----------
        X : array-like, shape (n_samples, n_features)
            Test data.
        batch_size : int
            Number of samples per batch (default: 512).

        Returns:
        -------
        scores : ndarray
            Minimum distances to training samples for each test input.
        """
        X = np.array(X)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if self.training_data is None:
            raise ValueError("Model has not been fit yet.")

        scores = []
        for i in range(0, len(X), batch_size):
            batch = X[i:i + batch_size]
            dists = euclidean_distances(batch, self.training_data)
            scores.append(np.min(dists, axis=1))
        return np.concatenate(scores)

    def is_anomalous(self, score):
        """
        Check if a score exceeds the threshold.

        Parameters:
        ----------
        score : float
            Anomaly score for a sample.

        Returns:
        -------
        bool
            True if score > threshold (anomalous), else False.
        """
        return score > self.threshold
