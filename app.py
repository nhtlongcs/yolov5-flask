"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
import argparse
import io
import os
from PIL import Image
from pathlib import Path
import torch
from flask import Flask, render_template, request, redirect
from flask_ngrok import run_with_ngrok


app = Flask(
    __name__, static_url_path="", static_folder="static", template_folder="templates"
)

run_with_ngrok(app)  # Start ngrok when app is run


@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))

        results = model(img, size=640)
        results.display(save=True, save_dir=Path("static"))

        return render_template("files.html")
        # return redirect(".jpg")
        # return redirect("static/image0.jpg")

    return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    model = torch.hub.load(
        "ultralytics/yolov5", "yolov5s", pretrained=True, force_reload=True
    ).autoshape()  # force_reload = recache latest code
    model.eval()
    app.run()  # debug=True causes Restarting with stat
