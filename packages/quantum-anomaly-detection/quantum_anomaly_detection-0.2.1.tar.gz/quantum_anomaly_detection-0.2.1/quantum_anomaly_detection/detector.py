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
    Quantum-inspired anomaly detector using LOF-style normalized k-NN distance.
    """

    def __init__(self, k=10, contamination=0.05):
        """
        Parameters:
        ----------
        k : int
            Number of neighbors to use.
        contamination : float
            Proportion of outliers expected (used to set threshold).
        """
        self.k = k
        self.contamination = contamination
        self.training_data = None
        self.threshold = None

    def fit(self, X):
        """
        Fit the model to the training data and compute dynamic threshold.

        Parameters:
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data (assumed to be mostly normal).
        """
        self.training_data = np.array(X)
        if self.training_data.ndim == 1:
            self.training_data = self.training_data.reshape(-1, 1)

        # Self-score on training data for threshold calibration
        train_scores = self._lof_score(self.training_data)
        self.threshold = np.percentile(train_scores, 100 * (1 - self.contamination))

    def predict(self, X):
        """
        Predict anomaly scores for test data.

        Parameters:
        ----------
        X : array-like of shape (n_samples, n_features)

        Returns:
        -------
        scores : ndarray
            LOF-style anomaly scores (higher = more anomalous)
        """
        return self._lof_score(X)

    def is_anomalous(self, score):
        """
        Determine if a score is anomalous.

        Parameters:
        ----------
        score : float

        Returns:
        -------
        bool
        """
        if self.threshold is None:
            raise ValueError("Model must be fit before calling is_anomalous.")
        return score > self.threshold

    def _lof_score(self, X):
        """
        Compute LOF-style score for each sample in X.

        Returns:
        -------
        scores : ndarray
        """
        X = np.array(X)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if self.training_data is None:
            raise ValueError("Model has not been fit yet.")

        dists = euclidean_distances(X, self.training_data)
        knn_dist_X = np.sort(dists, axis=1)[:, :self.k].mean(axis=1)

        # For normalization, compute density of nearest neighbors too
        train_dists = euclidean_distances(self.training_data, self.training_data)
        np.fill_diagonal(train_dists, np.inf)
        knn_dist_neighbors = np.sort(train_dists, axis=1)[:, :self.k].mean(axis=1)

        # Take mean of all training densities for normalization
        ref_density = np.mean(knn_dist_neighbors)

        # Score = how much more distant than typical local density
        scores = knn_dist_X / (ref_density + 1e-10)
        return scores