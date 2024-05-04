import os

import tensorflow as tf
from flask import Flask, request, render_template, redirect, url_for

from classifier import classify


app = Flask(__name__)

STATIC_FOLDER = "static"
UPLOAD_FOLDER = "static/uploads/"

cnn_model = tf.keras.models.load_model(STATIC_FOLDER + "/models/" + "cat_dog.h5")


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html")


@app.post("/classify")
def classify_file():
    file = request.files["image"]
    upload_image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(upload_image_path)

    label, prob = classify(cnn_model, upload_image_path)

    prob = round((prob * 100), 2)

    return redirect(url_for("result", label=label, probability=prob))


@app.route("/result")
def result():
    label = request.args.get("label")
    probability = request.args.get("probability")
    return render_template("result.html", label=label, probability=probability)


if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)
