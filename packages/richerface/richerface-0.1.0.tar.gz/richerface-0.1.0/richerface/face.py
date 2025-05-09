#!/usr/bin/env python
# coding: utf-8

import os
import cv2
import imghdr
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from tensorflow.keras.metrics import Precision, Recall, BinaryAccuracy

def train_model(data_dir, img_height=256, img_width=256, batch_size=32, epochs=20, logdir='logs', img_path=None):
    # === Enable GPU memory growth (if GPU is present) ===
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

    # === Image Cleanup ===
    image_exts = ['jpeg', 'jpg', 'bmp', 'png']
    for image_class in os.listdir(data_dir):
        for image in os.listdir(os.path.join(data_dir, image_class)):
            image_path = os.path.join(data_dir, image_class, image)
            try:
                img = cv2.imread(image_path)
                tip = imghdr.what(image_path)
                if tip not in image_exts:
                    print(f'Image not in ext list: {image_path}')
                    os.remove(image_path)
            except Exception as e:
                print(f'Issue with image {image_path}: {e}')

    # === Load Data ===
    data = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        image_size=(img_height, img_width),
        batch_size=batch_size
    )

    # === Visualize Batch ===
    data_iterator = data.as_numpy_iterator()
    batch = data_iterator.next()

    fig, ax = plt.subplots(ncols=4, figsize=(20, 20))
    for idx, img in enumerate(batch[0][:4]):
        ax[idx].imshow(img.astype(int))
        ax[idx].title.set_text(batch[1][idx])

    # === Normalize Data ===
    data = data.map(lambda x, y: (x / 255.0, y))

    # === Split Data ===
    dataset_size = len(list(data))
    train_size = int(dataset_size * 0.7)
    val_size = int(dataset_size * 0.2)
    test_size = int(dataset_size * 0.1)

    train = data.take(train_size)
    val = data.skip(train_size).take(val_size)
    test = data.skip(train_size + val_size).take(test_size)

    # === Build Model ===
    model = Sequential([
        Conv2D(16, (3, 3), strides=1, activation='relu', input_shape=(img_height, img_width, 3)),
        MaxPooling2D(),
        Conv2D(32, (3, 3), strides=1, activation='relu'),
        MaxPooling2D(),
        Conv2D(16, (3, 3), strides=1, activation='relu'),
        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')  # Binary classification
    ])

    model.compile(optimizer='adam', loss=tf.losses.BinaryCrossentropy(), metrics=['accuracy'])
    model.summary()

    # === Train Model ===
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)
    hist = model.fit(train, epochs=epochs, validation_data=val, callbacks=[tensorboard_callback])

    # === Plot Training Results ===
    plt.figure()
    plt.plot(hist.history['loss'], color="teal", label='loss')
    plt.plot(hist.history['val_loss'], color='orange', label='val_loss')
    plt.title('Loss')
    plt.legend()
    plt.show()

    plt.figure()
    plt.plot(hist.history['accuracy'], color="teal", label='accuracy')
    plt.plot(hist.history['val_accuracy'], color='orange', label='val_accuracy')
    plt.title('Accuracy')
    plt.legend()
    plt.show()

    # === Evaluate Model ===
    pre = Precision()
    re = Recall()
    acc = BinaryAccuracy()

    for batch in test.as_numpy_iterator():
        X, y = batch
        yhat = model.predict(X)
        pre.update_state(y, yhat)
        re.update_state(y, yhat)
        acc.update_state(y, yhat)

    print(f'Precision: {pre.result().numpy():.4f}, Recall: {re.result().numpy():.4f}, Accuracy: {acc.result().numpy():.4f}')

    # === Predict on a Single Image ===
    if img_path:
        predict_image(model, img_path, img_height, img_width)


def predict_image(model, img_path, img_height, img_width):
    # Read and preprocess the image for prediction
    img = cv2.imread(img_path)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Prediction Image")
    plt.axis('off')
    plt.show()

    # Resize and normalize image before prediction
    resized_img = cv2.resize(img, (img_width, img_height))
    normalized_img = np.expand_dims(resized_img / 255.0, axis=0)

    # Predict the image
    prediction = model.predict(normalized_img)
    print(f'Prediction: {prediction}')
