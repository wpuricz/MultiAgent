import streamlit as st
from openai_stories import generate_user_stories, review_user_story, improve_user_story

def main():
    st.title("User Story Conversation")

    with st.form("user_story_form"):
        description = st.text_area("Enter a description for two user stories:")
        submit_button = st.form_submit_button("Generate User Stories")

    if submit_button:
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        # Step 2: Generate user stories
        user_stories = generate_user_stories(description)
        st.session_state["messages"].append(("AI Agent 1", user_stories))
        user_story_1 = user_stories[0]
        user_story_2 = user_stories[1]
        # # Step 3: Review first user story
        feedback_1 = review_user_story(user_story_1)
        st.session_state["messages"].append(("AI Agent 2", feedback_1))

        # # Step 4: Improve first user story
        improved_story_1 = improve_user_story(user_story_1, feedback_1)
        st.session_state["messages"].append(("AI Agent 1", improved_story_1))

        # # Step 5: Review second user story
        feedback_2 = review_user_story(user_story_2)
        st.session_state["messages"].append(("AI Agent 2", feedback_2))

        # # Step 6: Improve second user story
        improved_story_2 = improve_user_story(user_story_2, feedback_2)
        st.session_state["messages"].append(("AI Agent 1", improved_story_2))

        # Step 7: Finalize
        st.session_state["messages"].append(("AI Agent 2", "The user stories are now complete."))

    # Display chat messages
    for author, message in st.session_state.get("messages", []):
        st.write(f"{author}: {message}")

if __name__ == "__main__":
    main()
