from ais import ais_predict
import numpy as np

data = np.random.rand(100, 10)
labels = np.random.randint(0, 2, 100)

acc = ais_predict(data, labels)
print(f"Accuracy: {acc:.2f}")
