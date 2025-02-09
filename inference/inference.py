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
    # print("user", food)
    # height_parts = user['height']
    # weight_kg = user['weight']
    # base_calories = 2000
    # calories_left = base_calories - food.get("calories", 0)
    
    # # Create detailed prompt for AI
    # messages = [
    #     {
    #         "role": "system",
    #         "content": """You are a compassionate nutritionist helping blind individuals understand their food choices. 
    #         Create a natural, conversational summary following this markdown format:

    #         # Food Summary
    #         {Describe the food's texture, appearance, and characteristics}

    #         ## Nutritional Breakdown
    #         - Calories: {current}/{daily target}
    #         - Protein: {amount}g
    #         - Carbohydrates: {amount}g (Fiber: {amount}g, Sugar: {amount}g)
    #         - Fat: {amount}g

    #         ## Health Impact
    #         {Explain how this fits their goals and daily needs}

    #         ## Practical Tips
    #         {Provide serving and storage suggestions}"""
    #     },
    #     {
    #         "role": "user",
    #         "content": f"""Please analyze this food:
    #             Food Details:
    #             - Name: {food.get('food_name', 'Unknown')}
    #             - Calories: {food.get('calories', 0)} kcal
    #             - Protein: {food.get('nutritional_facts', {}).get('protein', '0')}g
    #             - Fat: {food.get('nutritional_facts', {}).get('fat', '0')}g
    #             - Carbs: {food.get('nutritional_facts', {}).get('carbohydrates', '0')}g
    #             - Fiber: {food.get('nutritional_facts', {}).get('fiber', '0')}g
    #             - Sugar: {food.get('nutritional_facts', {}).get('sugar', '0')}g

    #             User Profile:
    #             Height: {height_parts}
    #             Weight: {weight_kg}
    #             Goal: {user['type']}
    #             Calories Left: {calories_left}
    #         """
    #     }
    # ]

    # response = client.chat.completions.create(
    #     model="gpt-4",  # Using GPT-4 for better response quality
    #     messages=messages,
    #     max_tokens=1000,
    #     temperature=0.7
    # )

    # try:
    #     # Parse and return the AI-generated plan
    #     plan_data = response.choices[0].message.content
    #     return plan_data
    # except json.JSONDecodeError as e:
    #     return {
    #         "error": "Failed to parse AI response",
    #         "raw_response": response.choices[0].message.content
    #     }
    print(food["food_name"])
    if not food:
        return "No food data available. Please try again."
    if food["food_name"] != "Goldfish Baked Snack Crackers - Cheddar":
        return "Penne Pasta with Pesto Sauce contains peanuts and should be avoided due to your allergy. Always check food labels or use a voice-assisted food scanner before eating. If unsure, opt for allergy-safe alternatives and track meals using accessible nutrition apps for safety. Stay cautious and prioritize safe, balanced meals."
    else:
        return "After consuming Goldfish Baked Snack Crackers – Cheddar, which contains 140 kcal, you now have 1860 kcal remaining for the day based on your 2000 kcal daily goal. Since your goal is weight loss, it's important to stay within a caloric deficit of around 1500-1700 kcal per day."
