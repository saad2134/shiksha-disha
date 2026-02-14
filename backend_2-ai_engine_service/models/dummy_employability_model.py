# models/dummy_employability_model.py
import joblib
from sklearn.dummy import DummyClassifier
import os
import numpy as np

X = np.zeros((10,5))  # dummy features
y = np.zeros(10)      # dummy labels
model = DummyClassifier(strategy="uniform")
model.fit(X, y)
os.makedirs("./models", exist_ok=True)
joblib.dump(model, "./models/employability_model.joblib")
