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


# =========================================================
# 1. AIS (Artificial Immune System) using Python.
# import numpy as np

# # Sample input (you should replace these with actual data)
# data = np.random.rand(100, 5)
# labels = np.random.randint(0, 2, 100)
# detector_count = 10
# split_ratio = 0.8

# # Split data
# split = int(split_ratio * len(data))
# X_train, X_test = data[:split], data[split:]
# y_train, y_test = labels[:split], labels[split:]

# # Select detectors
# idx = np.random.choice(len(X_train), detector_count, replace=False)
# detectors = X_train[idx]
# detector_labels = y_train[idx]

# # Predict
# predictions = []
# for x in X_test:
#     i = np.argmin(np.linalg.norm(detectors - x, axis=1))
#     predictions.append(detector_labels[i])

# # Accuracy
# acc = np.mean(predictions == y_test)
# print("Accuracy:", acc)

# ===============================

# ART NN
# pip install tensorflow tensorflow_hub opencv-python matplotlib
# import tensorflow_hub as hub
# import tensorflow as tf
# import numpy as np
# import cv2
# import matplotlib.pyplot as plt

# def load_img(path):
#     img = tf.io.read_file(path)
#     img = tf.image.decode_image(img, channels=3)
#     img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, :]
#     return img

# # Load model and images
# model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
# content = load_img('profile.jfif')
# style = load_img('monet.jpeg')

# # Stylize and display
# result = model(tf.constant(content), tf.constant(style))[0]
# plt.imshow(np.squeeze(result))
# plt.axis('off')
# plt.show()

# # Save image
# out = np.squeeze(result) * 255
# cv2.imwrite('generated_img.jpg', cv2.cvtColor(out.astype(np.uint8), cv2.COLOR_RGB2BGR))
