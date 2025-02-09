from dotenv import load_dotenv
from flask import Flask, request, jsonify
from inference import infer_image, generate_plan
from database import AtlasClient
from flask_cors import CORS
import os
load_dotenv()

db = AtlasClient(altas_uri=os.getenv('MOGO_URL'), dbname="devfest")


app = Flask(__name__)
CORS(app, origins="https://10.206.61.53:3000")

user = {
    "height": 161,
    "weight": 53,
    "type": "lose weight",
    "gender": "female",
    "allegy": "peanut"
}

# {
#     "height": 180,
#     "weight": 75,
#     "type": "gain weight",
#     "allegy": "peanut"
# }


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Call your model her
    if 'image' not in data:
        return jsonify({'error': 'no image found'})
    
    infer = infer_image(image_url=data['image'])
    image = get_image(food_name=infer)
    return jsonify({'result': generate_plan(user=user, food=image) })

def get_image(food_name: str):
    try:
        image = db.get_collection("userinfo")
        
        if not food_name:
            return None
            
        result = image.find_one({"food_name": f"{food_name}"})
        
        if result:
            # Convert ObjectId to string for JSON serialization
            print("result", result)
            result['_id'] = str(result['_id'])
            return result
        else:
            return None

            
    except Exception as e:
        return  None
    
if __name__ == '__main__':
        app.run(port=5000, host="0.0.0.0", debug=True, ssl_context=('./ssl-certficates/localhost.pem', './ssl-certficates/localhost-key.pem'))


"""
{
    image: "base64 encoded image"
    userInfo {
        height: 5'10"
        weight: 150 lbs
        type: "lose weight" | "gain weight" | "maintain weight"

    
        generate a plan for the user based on the type of weight loss they want to achieve
        plan: {
            goal: "lose weight"         
        }
    
    }


        
    if 'userInfo' not in data:
        return jsonify({'error': 'no userInfo found'})
    
    if 'height' not in data['userInfo']:
        return jsonify({'error': 'no height found'})
    
    if 'weight' not in data['userInfo']:
        return jsonify({'error': 'no weight found'})
    
    if 'type' not in data['userInfo']:
        return jsonify({'error': 'no type found'})
    
    if 'lose weight' not in data['userInfo']['type'] and 'gain weight' not in data['userInfo']['type'] and 'maintain weight' not in data['userInfo']['type']:
        return jsonify({'error': 'invalid type'})
    


}

"""



