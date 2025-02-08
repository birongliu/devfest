from dotenv import load_dotenv
from flask import Flask, request, jsonify
from inference import inference
load_dotenv()

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Call your model here
    print(data)
    inference.infer_image(image_array=data)
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
