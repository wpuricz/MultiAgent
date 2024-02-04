import openai
import streamlit as st
import json

open_ai_key = ''
# model = 'gpt-3.5-turbo-0125'
model = 'gpt-4'

def generate_code(requirements):
    openai.api_key = open_ai_key  # Use the provided API key
    
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI trained to generate code based on technical requirements."},
                {"role": "user", "content": f"Generate code based on the following requirements:\n{requirements}"},
            ]
        )
        # st.write(str(response))
        # Assuming the last message in the response is the code
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating code: {str(e)}"

    

def review_code(code):
    score_threshold = 97
    openai.api_key = open_ai_key  # Use the provided API key

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI trained to review code for quality and suggest improvements."},
                {"role": "user", "content": f"Review the following code snippet for quality and suggest improvements. You are a stickler for clean code. The code should be clean and follow best practice programming patterns.  Provide a score from 0 to 100 for the quality of the code and describe the best practice changes to implement. The output format should be a JSON object with 2 attributes - score (number), best_practices (string). Everything should be contained in these two attributes. Here is the code:\n\n{code}"},
            ]
        )
        st.write(response['choices'][0]['message']['content'])
        # Assuming the last message in the response is the review message
        review_message = response['choices'][0]['message']['content'].strip()
        
        # Extract JSON object from the content field
        try:
            review_data = json.loads(review_message)
        except json.JSONDecodeError:
            raise Exception("Failed to parse the JSON response: " + json.JSONDecodeError)

        # Extract score and best practices from the JSON object
        review_score = review_data.get("score")
        review_best_practices = review_data.get("best_practices")
        
        # Determine satisfaction based on the review score
        satisfied = review_score is not None and review_score > score_threshold
        
        # Create a string combining the score and best practices
        result_str = f"Score: {str(review_score)}\nBest Practices: {review_best_practices}"
        
        return {"message": result_str, "satisfied": satisfied}
    except Exception as e:
        return {"message": f"Error reviewing code: {str(e)}", "satisfied": False}





def generate_technical_requirements():
    
    openai.api_key = open_ai_key  # Replace with your actual API key

    # Define a prompt for generating technical requirements
    prompt = (
        "Create a detailed list of technical requirements for a task in a software project. "
        "The project should include aspects like user interface design, error handling, "
        "API integrations, and security features. There should be only features that can be implemented in code. "
        "The code should only need to be 50-100 lines of code"
    )

    try:
        response = openai.ChatCompletion.create(
  model=model,
  messages=[
        {"role": "system", "content": "You are an expert at generating technical requirements for software projects."},
        {"role": "user", "content": prompt},
    ]
)
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating technical requirements: {str(e)}"
    
