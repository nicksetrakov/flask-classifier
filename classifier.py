from PIL import Image
from typing import Any

import tensorflow as tf

IMAGE_SIZE = (150, 150)
THRESHOLD = 0.5


def preprocess_image(image) -> Any:
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = tf.expand_dims(img_array, axis=0)

    return img_array


def load_and_preprocess_image(path: str) -> Any:
    image = tf.keras.preprocessing.image.load_img(
        path, target_size=IMAGE_SIZE
    )

    return preprocess_image(image)


def classify(model, image_path: str) -> tuple[str, int]:
    preprocessed_image = load_and_preprocess_image(image_path)

    predictions = model.predict(preprocessed_image)
    score = predictions[0][0]

    label = "cat" if score <= THRESHOLD else "dog"
    prob = 1 - score if label == "cat" else score

    return label, prob
