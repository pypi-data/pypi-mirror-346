import numpy as np
from typing import Optional

class QuantumAnomalyDetector:
    """
    QuantumAnomalyDetector class for quantum-based anomaly detection.

    Attributes:
        threshold (float): Threshold above which a score is considered anomalous.
        reference_mean (float): Mean of the training data used as a baseline.
    """

    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
        self.reference_mean = 0.0

    def fit(self, X: np.ndarray):
        """
        Fit the detector to training data.

        Args:
            X (np.ndarray): Normal training data.
        """
        self.reference_mean = np.mean(X)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Compute anomaly scores (distance from mean).

        Args:
            X (np.ndarray): Input test data.

        Returns:
            np.ndarray: Anomaly scores.
        """
        return np.abs(X - self.reference_mean)

    def is_anomalous(self, score: float) -> bool:
        """
        Determine if the score is above threshold.

        Args:
            score (float): Anomaly score.

        Returns:
            bool: True if anomalous, False otherwise.
        """
        return score > self.threshold
