import openai
import streamlit as st

open_ai_key = ''
model = 'gpt-3.5-turbo-0125'

def generate_code(requirements):
    openai.api_key = open_ai_key  # Use the provided API key
    # st.write('generating code')
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
    openai.api_key = open_ai_key  # Use the provided API key

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI trained to review code for quality and suggest improvements. Provide a score from 0 to 100 for the quality of the code and describe the best practice changes to implement. Put a newline after the score and before the best practices"},
                {"role": "user", "content": f"Review the following code snippet for quality and suggest improvements. You are a stickler for clean code. The code should be clean and follow best practice programming patterns. Here is the code:\n\n{code}"},
            ]
        )
        # Assuming the last message in the response is the review message
        review_message = response['choices'][0]['message']['content'].strip()
        
        # Extract the score from the message
        score_start = review_message.find("Score:") + len("Score:")
        score_end = review_message.find("\n", score_start)
        review_score = int(review_message[score_start:score_end])
        
        # Extract the best practice changes description
        description_start = review_message.find("Best Practice Changes:") + len("Best Practice Changes:")
        review_description = review_message[description_start:]
        
        # Determine satisfaction based on the review score
        satisfied = review_score > 80
        return {"message": review_message, "satisfied": satisfied, "score": review_score, "description": review_description}
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
    
