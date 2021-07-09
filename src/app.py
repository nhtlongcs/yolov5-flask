"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
import argparse
import io
import os
from types import MethodDescriptorType

import pandas as pd
from UI import generate
from PIL import Image
from pathlib import Path
import torch
from flask import Flask, render_template, request, redirect
from flask import Response
import sys


app = Flask(
    __name__, static_url_path="", static_folder="static", template_folder="templates"
)

DETECTION_URL = "/api/detect"
model = torch.hub.load(
    "/path/to/this/repo/model/module", "custom", path="best.pt", source="local",
).autoshape()  # force_reload = recache latest code
model.eval()


@app.route("/files", methods=["GET"])
def reload():
    print("load files")
    content = generate(None)
    return Response(content, mimetype="text/html")


@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            if "file" not in request.files:
                return redirect(request.url)
            file = request.files["file"]
            save_dir = Path("static/shared")
            save_dir.parent.mkdir(parents=True, exist_ok=True)
            print(file.filename)
            if not file:
                return redirect("404.html")

            img_bytes = file.read()
            img = Image.open(io.BytesIO(img_bytes))

            results = model(img, size=640)
            # results.names = ["cay xuong rong", "cay hoa do", "cay hoa vang"]
            results.files[0] = file.filename
            results.display(save=True, save_dir=save_dir)
        except:
            return redirect("404.html")
        return redirect("/files")

    return render_template("index.html")  # render dung cho nhung file dang template


@app.route(DETECTION_URL, methods=["POST"])
def json_predict():
    if not request.method == "POST":
        return

    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()

        img = Image.open(io.BytesIO(image_bytes))

        results = model(img, size=640)
        data = results.pandas().xyxy[0].to_json(orient="records")
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    parser.add_argument("--ngrok", default=False, action="store_true")

    args = parser.parse_args()

    if args.ngrok:
        from flask_ngrok import run_with_ngrok

        run_with_ngrok(app)  # Start ngrok when app is run

        app.run(threaded=True)  # debug=True causes Restarting with stat
    else:
        app.run(
            host="0.0.0.0", port=args.port, threaded=True
        )  # debug=True causes Restarting with stat
