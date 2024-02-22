import streamlit as st
from openai_integration import generate_code, review_code, generate_technical_requirements, generate_improvements  # Hypothetical modules
import logging

placeholder = "Please create a form for users to input their information. This should be in react. It should contain the following fields - \
first name, last name, age, date of birth, gender. It should validate the values of each field. They are all required. \
It should also post the data to a server and display a message to the user on the response. \
It should also display errors in validation and api calls if necessary."

max_api_calls = 8

def start_development_flow(requirements):
    st.session_state.status = "Starting"
    satisfied = False
    last_code = None
    last_review_feedback = None

    while not satisfied and st.session_state.api_calls < max_api_calls:
        st.write(f"Status: {st.session_state.status}")
        st.session_state.status = "Developer is creating code"
        
        # Determine whether to generate new code or improve existing code based on feedback
        if last_code is None:
            code = generate_code(requirements)
        else:
            code = generate_improvements(last_code, last_review_feedback)
        
        if code.startswith('Error'):
            st.error("Error generating code." + code)
            return

        with st.chat_message("Developer:"):
            st.markdown(code)

        st.session_state.status = "Reviewer is reviewing code"
        review_result = review_code(code)
        if "message" in review_result and "satisfied" in review_result:
            with st.chat_message("reviewer"):
                st.markdown(review_result['message'])
                satisfied = review_result['satisfied']
        else:
            st.error("Error in reviewing code. Development flow interrupted.")
            return

        last_code = code  # Store the last successfully generated or improved code
        last_review_feedback = review_result['message']  # Store the last review feedback for potential improvements
        st.session_state.api_calls += 2  # Counting both the generation/improvement and review API calls

    st.session_state.status = "Satisfied" if satisfied else "Max API calls reached"
    # st.write(f"Status: {st.session_state.status}")


def create_streamlit_app():
    # Initialize session states
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    if 'api_calls' not in st.session_state:
        st.session_state.api_calls = 0
    if 'chat_log' not in st.session_state:
        st.session_state.chat_log = []
    if 'status' not in st.session_state:
        st.session_state.status = "Not started"  # Initialize status


    st.title("Multi-Agent AI Application")
    requirements = st.text_area("Enter Technical Requirements", value=placeholder.strip(), height=400)
    # generate_button = st.button("Generate Requirements")
    submit_button = st.button("Submit Requirements")
    # Display Status
    st.subheader("Status:")
    # st.write(st.session_state.status)

    chat_history = st.empty()
    # Display Chat History using st.chat_message
    for message_info in st.session_state.chat_log:
        role = message_info["role"]
        message = message_info["message"]
        with st.chat_message(role if role in ["developer", "reviewer"] else "user"):
            st.markdown(message)

    # Handling Generate Button
    # if generate_button:
        # requirements = generate_technical_requirements()  # Hypothetical function to generate requirements

    # Handling Submit Button
    if submit_button and requirements:
        st.session_state.api_calls = 0
        st.session_state.chat_log = []
        st.session_state.status = "Starting development flow"
        start_development_flow(requirements)

# Run the Streamlit app
if __name__ == "__main__":
    create_streamlit_app()
