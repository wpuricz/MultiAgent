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
                {"role": "system", "content": "You are an AI trained to review code for quality and suggest improvements."},
                {"role": "user", "content": f"Review the following code snippet for quality and suggest improvements. You are a stickler for clean code. The code should be clean and follow best practice programming patterns. Here is the code:\n\n{code}"},
            ]
        )
        # Assuming the last message in the response is the review
        review_text = response['choices'][0]['message']['content'].strip()
        # Determining satisfaction based on review text is more nuanced in a chat context
        satisfied = "improvement" not in review_text.lower()  # Example logic, adjust as needed
        return {"message": review_text, "satisfied": satisfied}
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
    
