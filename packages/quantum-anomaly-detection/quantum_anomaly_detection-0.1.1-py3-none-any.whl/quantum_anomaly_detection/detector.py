from typing import Optional
import numpy as np
from qiskit_aer import Aer
from qiskit import Aer, QuantumCircuit, transpile, assemble, execute
from qiskit.visualization import plot_histogram

class QuantumAnomalyDetector:
    """
    QuantumAnomalyDetector class for quantum-based anomaly detection.
    
    Attributes:
        backend (str): The quantum simulator backend.
        threshold (float): The threshold above which a data point is considered anomalous.
        reference_mean (float): Mean of the reference (normal) dataset.
    """
    
    def __init__(self, backend: str = 'aer_simulator', threshold: float = 0.5):
        self.backend = backend
        self.threshold = threshold
        self.reference_mean = 0.0

    def _encode(self, x: float) -> QuantumCircuit:
        """
        Encode a single value into a quantum circuit using Ry encoding.

        Args:
            x (float): The value to encode.
        
        Returns:
            QuantumCircuit: The circuit encoding the value.
        """
        qc = QuantumCircuit(1)
        qc.ry(x, 0)
        qc.measure_all()
        return qc

    def fit(self, X: np.ndarray):
        """
        Fit the detector to a dataset by learning the average pattern (mean).

        Args:
            X (np.ndarray): 1D array of training data (normal behavior).
        """
        self.reference_mean = np.mean(X)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Compute anomaly scores as the absolute difference from reference mean.

        Args:
            X (np.ndarray): 1D array of input data.

        Returns:
            np.ndarray: Anomaly scores for each data point.
        """
        return np.abs(X - self.reference_mean)

    def is_anomalous(self, score: float) -> bool:
        """
        Decide if a score indicates an anomaly.

        Args:
            score (float): Anomaly score.

        Returns:
            bool: True if anomalous, False otherwise.
        """
        return score > self.threshold
