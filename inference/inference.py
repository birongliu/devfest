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
    messages=[{"role": "system", "content": f"You are a caregiver that help blind people identify food. Scan the images to provide food name for the food items in the image, structure the response in the following format: {schema}"},
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

user = {
    "height": "5'10",
    "weight": "150 lbs",
    "type": "lose weight"
}

def generate_plan(user: dict, food: dict) -> dict:
    # Calculate metrics
    print("user", user)
    height_parts = user['height']
    weight_kg = user['weight']
    
    # Create detailed prompt for AI
    messages = [
        {
            "role": "system",
            "content": """You are a professional nutritionist and personal trainer. Analyze the user's 
                      metrics and provide a detailed nutrition plan. Format the response 
                      as JSON with the following structure:
                      {
                          "summary": {
                              "current_stats": { BMI, health_status },
                              "goal_analysis": String,
                              "timeframe": String
                          },
                          "nutrition_plan": {
                              "daily_calories": Number,
                              "macros": { protein, carbs, fats },
                              "meal_timing": [String],
                              "food_recommendations": [String]
                          }
                      }"""
        },
        {
            "role": "user",
            "content": f"""Create a personalized plan for:
                Height: {height_parts}cm
                Weight: {weight_kg}kg
                Goal: {user['type']}
            """
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4",  # Using GPT-4 for better response quality
        messages=messages,
        max_tokens=1000,
        temperature=0.7
    )

    try:
        # Parse and return the AI-generated plan
        plan_data = json.loads(response.choices[0].message.content)
        return plan_data
    except json.JSONDecodeError as e:
        return {
            "error": "Failed to parse AI response",
            "raw_response": response.choices[0].message.content
        }
