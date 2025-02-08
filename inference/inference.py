import base64
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def infer_image(image_array: list[str]):
    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    messages = [
        {
            "role": "system",
            "content": (
                "You are a caregiver that helps blind people identify food. "
                "Scan the images to provide detailed nutrition facts for the food items in the image."
            ),
        },
        {
            "role": "user",
            "content": (
                "Identify the food items in this image, categorize them by type "
                "(fruit, vegetable, protein, grain, etc.), and provide an estimate of their "
                "nutritional values including Calories, Total Fat, Saturated Fat, Trans Fat, "
                "Cholesterol, Sodium, Total Carbohydrates, Dietary Fiber, Sugars, Protein, "
                "Vitamin D, Calcium, Iron, and Potassium."
            ),
        }
    ]

    # Append each image as a new user message (inserting the base64 data as a string)
    for encoded_image in image_array:
        messages.append({
            "role": "user",
            "content": json.dumps({
                "type": "image_url",
                "image_url": {"url": f"{encoded_image}"}
            })
        })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    return response.choices[0].message.content


# import base64
# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def infer_image(image_array: list[str]):
# # Function to encode the image
#     def encode_image(image_path):
#         with open(image_path, "rb") as image_file:
#             return base64.b64encode(image_file.read()).decode("utf-8")

#     messages=[{"role": "system", "content": "You are an caregiver that help blind people identifies food. Scan the images to provide detailed nutrition facts for the food items in the image."},
#             {"role": "user", "content": [
#                 {"type": "text", "text": "Identify the food items in this image, categorize them by type (fruit, vegetable, protein, grain, etc.), and provide an estimate of their nutritional values including Calories, Total Fat, Saturated Fat, Trans Fat, Cholesterol, Sodium, Total Carbohydrates, Dietary Fiber, Sugars, Protein, Vitamin D, Calcium, Iron, and Potassium."},
#             ]}]
    
#     for encoded_image in image_array:
#         messages.append({"type": "image_url", "image_url": {"url": f"{encoded_image}"}})

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages,
#     )

#     return (response.choices[0])
