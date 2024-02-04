import streamlit as st
from openai_integration import generate_code, review_code, generate_technical_requirements  # hypothetical modules for OpenAI API integration

placeholder = 'Please create a form for users to input their information. It should contain the following fields - first name, last name, age, date of birth, gender. It should validate the values of each field. They are all required. It should also post the data to a server and display a message to the user on the response. It should also display errors in validation and api calls if necessary.'
max_api_calls = 3
# Function to handle the development flow
def start_development_flow(requirements):
    
    # st.write('starting dev flow')
    
    satisfied = False
    while not satisfied and st.session_state.api_calls < max_api_calls:
        # st.write('about to generate code')
        code = generate_code(requirements)
        if(code.startswith('Error')):
            st.error(code)
            return
        # st.write(code)
        st.session_state.chat_log.append({"role": "developer", "message": code})
        review_result = review_code(code)
        st.session_state.chat_log.append({"role": "reviewer", "message": review_result['message']})
        satisfied = review_result['satisfied']
        st.session_state.api_calls += 2  # Counting both generate and review API calls

    if satisfied:
        st.session_state.chat_log.append({"role": "system", "message": "Review Completed Successfully"})
    else:
        st.session_state.chat_log.append({"role": "system", "message": "Max API calls reached"})


def create_streamlit_app():
    # Initialize session states
    if 'api_calls' not in st.session_state:
        st.session_state.api_calls = 0
    if 'chat_log' not in st.session_state:
        st.session_state.chat_log = []

    # UI Components
    st.title("Multi-Agent AI Application")
    requirements = st.text_area("Enter Technical Requirements", value=placeholder, height=400)
    generate_button = st.button("Generate Requirements")
    submit_button = st.button("Submit Requirements")
    chat_history = st.empty()

    # Handling Generate Button
    if generate_button:
        requirements = generate_technical_requirements()  # hypothetical function to generate requirements
        text_area = requirements
        # st.write(requirements)

    # Handling Submit Button
    if submit_button and requirements:
        # st.write('button pressed')
        st.session_state.api_calls = 0
        st.session_state.chat_log = []
        # st.write('about to start dev flow')
        start_development_flow(requirements)

    # Display Chat History
    # for message in st.session_state.chat_log:
    #     st.text(message)
    # Display Chat History
    # for i, message in enumerate(st.session_state.chat_log):
    #     if i % 2 == 0: # Assuming that Developer messages always start
    #         st.markdown(f'**Developer**: {message}')
    #     else:
    #         st.markdown(f'**Reviewer**: {message}')
    # Display Chat History using st.chat_message
    for message_info in st.session_state.chat_log:
        role = message_info["role"]
        message = message_info["message"]
        with st.chat_message(role if role in ["developer", "reviewer"] else "user"):
            st.write(message)



# Run the Streamlit app
if __name__ == "__main__":
    create_streamlit_app()

