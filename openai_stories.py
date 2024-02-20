from openai import OpenAI
import streamlit as st
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# model = 'gpt-3.5-turbo'
model = 'gpt-3.5-turbo-0125'

def generate_user_stories(description):
    # return 'here are the user stories, story 1:\n story 2'
    
    prompt = f"Generate two user stories based on the following description: {description}."
    response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a product manager that is an expert at creating user stories for agile development in software applications. You are a product manager that is an expert at creating user stories for agile development in software applications. The output format should be in JSON and should be an array of 2 strings, each string should contain one user story. Here is the json format: ['',''] "},
                {"role": "user", "content": prompt },
            ]
        )
    try:
        stories = json.loads(response.choices[0].message.content.strip())
    except json.JSONDecodeError:
        raise Exception("Failed to parse the JSON response: " + json.JSONDecodeError)
    
    logger.info(stories)
    return stories
    

def review_user_story(user_story):
    # return 'here is the feedback for the user story'

    prompt = f"Review the following user story and provide feedback: {user_story}. The user stories should following the INVEST framework principles. They should also include acceptance criteria and gherkin scenarios"
    response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a product manager that is an expert at assessing user stories and recommending improvements."},
                {"role": "user", "content": prompt },
            ]
        )
    logger.info(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()

def improve_user_story(user_story, feedback):
    # return 'here are the improvements to the user story'
    

    prompt = f"Improve the following user story based on the feedback: {user_story} Feedback: {feedback}"
    response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a product manager that is an expert at creating user stories for agile development in software applications."},
                {"role": "user", "content": prompt },
            ]
        )
    logger.info(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()
