# ais/core.py
import numpy as np


def ais_predict(data, labels, detector_count=10, split_ratio=0.8):
    split = int(split_ratio * len(data))
    X_train, X_test = data[:split], data[split:]
    y_train, y_test = labels[:split], labels[split:]

    idx = np.random.choice(len(X_train), detector_count, replace=False)
    detectors = X_train[idx]
    detector_labels = y_train[idx]

    predictions = []
    for x in X_test:
        i = np.argmin(np.linalg.norm(detectors - x, axis=1))
        predictions.append(detector_labels[i])

    acc = np.mean(predictions == y_test)
    return acc
