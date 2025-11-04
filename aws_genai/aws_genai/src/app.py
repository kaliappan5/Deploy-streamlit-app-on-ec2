"""Streamlit app for the AI powered cost query assistant."""
import os
import traceback
import streamlit as st
from kb_retrieve2 import invoke_retrieve_generate
from dotenv import load_dotenv
from htmltemplates import user_template, bot_template

# CSS for the chat interface and responses
st.markdown('''
<style>
.chat-message {padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; \
            display: flex}
.chat-message.user {background-color: #2b313e}
.chat-message.bot {background-color: #475063}
.chat-message .avatar{width:20%}
.chat-message .avatar img{max-width:78px; max-height: 78px; \
            border-radius: 50%; \
            object-fit: cover}
.chat-message .message {width: 80%; padding: 0 1.5rem; color: #fff}
.response, .url {background-colorc: #0f0f0f0; padding: 1rem; \
            border-radius: 0.5rem; \
            margin-bottom: 1rem;}
</style>
''', unsafe_allow_html=True)


SEARCH_TYPES = {
    "DEFAULT": "Default Search",
    "HYBRID": "Hybrid Search",
    "SEMANTIC": "Semantic Search"
}

MODEL_CHOICES = {
    "anthropic.claude-3-haiku-20240307-v1:0": "Claude 3 Haiku",
    "anthropic.claude-3-sonnet-20240229-v1:0": "Claude 3 Sonnet",
    "anthropic.claude-v2:1": "Claude 2.1",
    "anthropic.claude-v2": "Claude 2",
    "anthropic.claude-instant-v1": "Claude Instant 1.2"}


def format_search(option):
    """Formats the search options for display."""
    return SEARCH_TYPES[option]


def format_func(option):
    """Formats the model options for display."""
    return MODEL_CHOICES[option]


# Function to handle chat response
def handle_chat_response(response):
    """Handles the chat response from the Bedrock API."""
    # Extract response
    response_text = response['output']['text']
    print(response_text)

    # Check if there any retrieverd references
    if not response['citations'][0]['retrievedReferences']:
        # No references found, use the response text
        display_text = response_text

    else:
        # Handle normal case with references
        # Extract S3 URI consuming references are present
        s3_uri = response['citations'][0]['retrievedReferences'][0]['location']['s3Location']['uri']
        display_text = f"{response_text}<br><br>Reference:<br>{s3_uri}"
        return display_text


def main():
    """Main function for the Streamlit app."""
    # load environment varialbles
    load_dotenv()
    st.title("AI powered cost query assistant")
    # Create Sidebar for Config and Options
    with st.sidebar:
        st.sidebar.title("Configurations & Options:")

        # Initialize conversation histroy if not present
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []
        search_type = st.radio("Search Type:",
                               list(SEARCH_TYPES.keys()),
                               format_func=format_search)
        print('search_type:', search_type)

        st.subheader("Inference Parameters:")

        # select bedrock model with default value of "claude-3-haiku"
        model_id = st.selectbox("Model:",
                                options=list(MODEL_CHOICES.keys()),
                                format_func=format_func)
        print('selected model:', model_id)

        # select max Tokens parameter with default value of 500
        max_tokens = st.selectbox(label="Tokens:",
                                  index=1,
                                  options=[250, 500, 1000, 2000, 5000])

        # select box for temperature parameter with default value of 0.1
        temperature = st.slider("Temperature:",
                                min_value=0.0,
                                max_value=1.0,
                                value=0.2,
                                step=0.1)

        # select top_p parameter with default value of 0.8
        top_p = st.slider("Top P:",
                          min_value=0.0,
                          max_value=1.0,
                          value=0.7,
                          step=0.1)
        print(top_p)

        st.subheader("Maximum number of retrieved results:")
        # Maximum number of retrieved results in number input
        max_results = st.number_input("Enter a number between 1 and 50",
                                      min_value=1,
                                      max_value=50,
                                      value=2)

    kb_id = os.getenv("KB_ID")
    # handle chat functionlity
    user_input = st.text_input("Ask a Question: ")
    if st.button("Send"):
        print("send clicked")
        print('app4')

        try:
            print('kb_id:', kb_id)
            print('model_id:', model_id)
            print('max_tokens:', max_tokens)
            print('temperature:', temperature)
            print('top_p:', top_p)
            print('max_results:', max_results)
            print('user_input:', user_input)
            # Retrieve and Generate API call
            response = invoke_retrieve_generate(user_input,
                                                kb_id,
                                                model_id,
                                                max_tokens,
                                                temperature,
                                                top_p,
                                                max_results,
                                                search_type)
            print(response)
            display_text = handle_chat_response(response)

            # Insert the reponse at the beginning of the conversation history
            st.session_state.conversation_history.insert(0, ("Assistant", f"<div class='response'>{display_text}</div>"))
            st.session_state.conversation_history.insert(0, ("You", user_input))

            # Display conversation history
            for speaker, text in st.session_state.conversation_history:
                if speaker == "You":
                    st.markdown(user_template.replace("{{MSG}}", text),
                                unsafe_allow_html=True)
                else:
                    st.markdown(bot_template.replace("{{MSG}}", text),
                                unsafe_allow_html=True)
        except Exception as e:
            print(f"An unexpected error occured in retrieve reference: {str(e)}")
            traceback.print_exc()


if __name__ == '__main__':
    main()
