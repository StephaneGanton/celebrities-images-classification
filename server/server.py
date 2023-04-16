from urllib import response
import util
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/classify_image', methods=['GET,POST'])
def classify_image():

    image_data = request.form['image_data'] #based64 format
    response = jsonify(util.classify_image(image_data))

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    print("Starting Python Flask server for Celebrity Images Classification")
    util.load_saved_artifacts()
    app.run(port=5000)