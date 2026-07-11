from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS, cross_origin
from src.cnnClassifer.components.prediction import PredictionPipeline
from src.cnnClassifer.utils.common import decodeImage
import uuid

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL','en_US.UTF-8')

app = Flask(__name__)
CORS(app)

is_training = False

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictionPipeline(self.filename)



@app.route("/", methods= ["GET"])
@cross_origin()
def home():
    return render_template("index.html")



@app.route("/train", methods=['GET','POST'])
@cross_origin()
def trainRoute():
    global is_training
    if request.method == 'GET':
        return render_template("train.html")

    if is_training:
        return jsonify({"status": "error", "message": "Training is already running."})

    # POST: run training (blocking like before)
    is_training = True
    try:
        os.system("python -m dvc repro")
    finally:
        is_training = False
        
    return jsonify({"status": "completed"})



@app.route("/predict", methods=['GET','POST'])
@cross_origin()
def predictRoute():
    global is_training
    if request.method == 'GET':
        return render_template("predict.html")

    if is_training:
        return jsonify({"prediction": "Training in progress. Please try again later.", "confidence": 0})

    os.makedirs("images", exist_ok=True)
    unique_filename = f"images/{uuid.uuid4().hex}.jpg"

    # Accept multipart file upload (from the HTML form) or a base64 JSON payload
    # 1) File upload via FormData (key: 'file')
    if 'file' in request.files:
        file = request.files['file']
        file.save(unique_filename)

    else:
        # 2) JSON body containing base64 image string under 'image'
        image_b64 = None
        if request.is_json:
            data = request.get_json()
            image_b64 = data.get('image')
        else:
            image_b64 = request.form.get('image')

        if not image_b64:
            return jsonify({'error': 'No image provided'}), 400

        decodeImage(image_b64, unique_filename)

    # Call prediction method
    clApp.classifier.filename = unique_filename
    result = clApp.classifier.predict()
    return jsonify(result)



if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host='0.0.0.0', port=8000)