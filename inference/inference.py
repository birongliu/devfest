import base64
from openai import OpenAI
import os
from dotenv import load_dotenv
import json 
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

schema = """" 
{                
"food_name": string  
}
"""

def infer_image(image_url: str) -> str:
# Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    print(image_url)
    messages=[{"role": "system", "content": f"You are an caregiver that help blind people identifies food. Scan the images to provide food name for the food items in the image. structured the response in the following format: {schema}"},
            {"role": "user", "content": [
                {"type": "text", "text": "Identify the food items in this image and provide detailed food name."},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]}]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    response_data = json.loads(response.choices[0].message.content)
    return response_data["food_name"]


