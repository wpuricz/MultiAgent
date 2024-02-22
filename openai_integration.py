from openai import OpenAI
import streamlit as st
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
review_model = 'gpt-3.5-turbo-0125'
# model = 'gpt-4'
model = 'gpt-3.5-turbo'

def generate_code(requirements):
    prompt = f"Generate code based on the following requirements:\n{requirements}"

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI trained to generate code based on technical requirements."},
                {"role": "user", "content": prompt},
            ]
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating code: {str(e)}"


def generate_improvements(code, improvements):
    prompt = f"""
    Here are a list of improvements, please improve the following code as per the improvements stated:
    Improvements: 
    {improvements}
    Code:
    {code}"""
    
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI trained to modify and improve code based on specific feedback."},
                {"role": "user", "content": prompt },
            ]
        )
        # logger.info("Received response:", response)
        # Assuming the last message in the response contains the improved code
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating improvements: {str(e)}"

# TODO: only suggested improvements should be contained in best_practices, if there are no more improvements then mark the code as satisfied
def review_code(code):
    
    prompt = f"""Review the following code snippet for quality and suggest improvements. You are an advocate for clean code. 
    The code should be clean and follow best practice programming patterns.  If improvements to the code can be made,
    describe the improvements to implement in the improvements attribute. The output should be the suggested improvements, you do not need to provide sample code. 
    If there are no new suggested improvements, the hasImprovements attribute should be false, otherwise it should be true.
    
    Here is the code:
    {code}"""
    
    try:
        # logger.info(prompt)
        response = client.chat.completions.create(
            model=review_model,
            messages=[
                {"role": "system", "content": 
                 """You are an AI trained to review code for quality and suggest improvements. Do NOT return any code or code fences.
                 Your response should come back in JSON format with the following structure:
                 
                    {
                        improvements: string,
                        hasImprovements: boolean
                    }

                 """
                 },
                {"role": "user", "content": prompt.strip()},
            ],
            # response_format={"type","json_object"}
        )
        # logger.info('got response for')
        # logger.info("Received response:", response)
        # Assuming the last message in the response is the review message
        review_message = response.choices[0].message.content.strip()
        # logger.info(review_message)
        
        # Extract JSON object from the content field
        try:
            review_data = json.loads(review_message)
        except json.JSONDecodeError:
            raise Exception("Failed to parse the JSON response: " + json.JSONDecodeError)

        # # Extract score and best practices from the JSON object
        improvements = review_data["improvements"]
        has_improvements = review_data["hasImprovements"]
        
        # Determine satisfaction based on the review score
        # satisfied = review_score is not None and review_score > score_threshold
        satisfied = True if not has_improvements else False
        
        # Create a string combining the score and best practices
        result_str = f"Improvements: {improvements}"
        
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
        response = client.chat.completions.create(
  model=model,
  messages=[
        {"role": "system", "content": "You are an expert at generating technical requirements for software projects."},
        {"role": "user", "content": prompt},
    ]
)
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating technical requirements: {str(e)}"
    
