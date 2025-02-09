from dotenv import load_dotenv
from flask import Flask, request, jsonify
from inference import infer_image, generate_plan
from database import AtlasClient
from flask_cors import CORS
import os
from groq import Groq
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


import os
from werkzeug.utils import secure_filename
from pydantic import BaseModel


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    try:
        print("Files in request:", request.files)
        print("Form data:", request.form)
        
        if 'audio' not in request.files:
            print("No audio file in request.files")
            return jsonify({'error': 'No audio file received'}), 400
            
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
            
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save file temporarily
        temp_path = os.path.join(temp_dir, secure_filename(audio_file.filename))
        audio_file.save(temp_path)
        print(f"Audio saved to: {temp_path}")
        groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
        try:
            # TODO: Add your speech-to-text processing here
            audio = groq.audio.transcriptions.create(
            file=(audio_file.filename, audio_file),
                model="whisper-large-v3-turbo",
                temperature=1,
                response_format='json'  # Optional
            )
            transcription = audio  # Replace with actual processing
            print("transcription", transcription)
            
            return jsonify({
                'transcription': transcription.text,
                'status': 'success'
            })       
        except Exception as e:
            print(f"Error in speech_to_text: {str(e)}")
            return jsonify({
                'error': 'Failed to process audio',
                ' details': str(e)
            }), 500
        finally:
            # Remove temp file
            # os.remove(temp_path)
            pass
    except Exception as e:
        print(f"Error in speech_to_text: {str(e)}")
        return jsonify({
            'error': 'Failed to process audio',
            ' details': str(e)
        }), 500
    
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Call your model her
    if 'image' not in data:
        return jsonify({'error': 'no image found'})
    
    infer = infer_image(image_url=data['image'])
    print("infer", infer)
    image = get_image(food_name=infer)
    return jsonify({'result': generate_plan(user=user, food=image) })

def get_image(food_name: str):
    try:
        image = db.get_collection("userinfo")
        
        if not food_name:
            return None
            
        # result = image.find_one({"food_name": {"$regex":f".*{food_name}.*", "$options": "i"}})
        result = image.find_one({
            "food_name": {
                "$regex": f"{food_name.lower()}",  # Match anywhere in the string
                "$options": "i"    # Case-insensitive
            }
        })

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



