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
    Quantum-inspired anomaly detector using average distance to k-nearest training samples.
    """

    def __init__(self, k=5, contamination=0.1):
        """
        Parameters:
        ----------
        k : int
            Number of nearest neighbors to consider.
        contamination : float
            Expected proportion of anomalies (used to compute threshold).
        """
        self.k = k
        self.contamination = contamination
        self.training_data = None
        self.threshold = None

    def fit(self, X):
        """
        Fit the model using training data.

        Parameters:
        ----------
        X : array-like, shape (n_samples, n_features)
            Training data assumed to be mostly normal.
        """
        self.training_data = np.array(X)
        if self.training_data.ndim == 1:
            self.training_data = self.training_data.reshape(-1, 1)

        # Calculate self-scores on training data for automatic threshold
        dists = euclidean_distances(self.training_data, self.training_data)
        np.fill_diagonal(dists, np.inf)
        knn_scores = np.sort(dists, axis=1)[:, :self.k].mean(axis=1)
        self.threshold = np.percentile(knn_scores, 100 * (1 - self.contamination))

    def predict(self, X):
        """
        Predict anomaly scores for new samples.

        Parameters:
        ----------
        X : array-like, shape (n_samples, n_features)
            Input samples.

        Returns:
        -------
        scores : ndarray, shape (n_samples,)
            Average k-NN distance to training data (higher = more anomalous).
        """
        X = np.array(X)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if self.training_data is None:
            raise ValueError("Model has not been fit yet.")

        dists = euclidean_distances(X, self.training_data)
        scores = np.sort(dists, axis=1)[:, :self.k].mean(axis=1)
        return scores

    def is_anomalous(self, score):
        """
        Determine whether a score is anomalous.

        Parameters:
        ----------
        score : float
            Anomaly score for a sample.

        Returns:
        -------
        bool
            True if score exceeds threshold.
        """
        if self.threshold is None:
            raise ValueError("Threshold is not set. Run fit() first.")
        return score > self.threshold
