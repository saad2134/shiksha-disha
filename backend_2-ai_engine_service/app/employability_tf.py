# app/employability_tf.py
import tensorflow as tf
import os

MODEL_PATH = "./models/employability_tf_model"

def build_dummy_model():
    # Input: 5 numeric features (nsqf_level, duration, exp, skill_overlap, region_match)
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(5,)),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Save a dummy model
if not os.path.exists(MODEL_PATH):
    m = build_dummy_model()
    # train on dummy data
    import numpy as np
    X = np.random.rand(100,5)
    y = np.random.randint(0,2,100)
    m.fit(X,y, epochs=3, verbose=0)
    m.save(MODEL_PATH)
