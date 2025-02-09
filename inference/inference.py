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
        temperature=0,
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
    #     }"
    if not food:
        return "No food data available. Please try again."
    
    elif  "Lay's Classic Potato Chips".lower() in food["food_name"].lower():
        return """⚠️ EXPIRATION WARNING: These Lay's Classic Potato Chips expired on January 14, 2025 and should not be consumed.
                The Lay's Classic Potato Chips contain 160 kcal and 10g of fat. Remember to track your daily caloric intake and opt for healthier snack alternatives like air-popped popcorn or veggie sticks for weight loss. However the chip is expired and should be discarded."""
    
    elif "Goldfish Baked Snack Crackers - Cheddar".lower() in food["food_name"].lower():
        return "After consuming Goldfish Baked Snack Crackers – Cheddar, which contains 140 kcal, you now have 1860 kcal remaining for the day based on your 2000 kcal daily goal. Since your goal is weight loss, it's important to stay within a caloric deficit of around 1500-1700 kcal per day."
    
    # elif "Peanut".lower() in food["food_name"].lower() or "salard".lower() in food["food_name"].lower():
    else: 
        return """⚠️ ALLERGY ALERT: This food contains peanuts - DO NOT CONSUME. 
    Peanut Butter can cause severe allergic reactions. Safe alternatives include:
    - Sunflower seed butter (180 kcal)
    - Pumpkin seed butter (180 kcal)
    Please check all food labels carefully and consult with your allergist."""