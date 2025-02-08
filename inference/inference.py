import base64
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def infer_image(image_url: str):
# Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    print(image_url)
    messages=[{"role": "system", "content": "You are an caregiver that help blind people identifies food. Scan the images to provide detailed nutrition facts for the food items in the image."},
            {"role": "user", "content": [
                {"type": "text", "text": "Identify the food items in this image, categorize them by type (fruit, vegetable, protein, grain, etc.), and provide an estimate of their nutritional values including Calories, Total Fat, Saturated Fat, Trans Fat, Cholesterol, Sodium, Total Carbohydrates, Dietary Fiber, Sugars, Protein, Vitamin D, Calcium, Iron, and Potassium."},
                {"type": "image_url", "image_url": {"url": image_url[0]}}
            ]}]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    return (response.choices[0].message.content)
