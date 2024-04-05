import streamlit as st
from embedchain import App
import os
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header


#os.environ['OPENAI_API_KEY'] = api.get_key()
#os.environ["OPENAI_API_KEY"] = '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'

OPENAI_KEY = st.secrets["OPENAI_TOKEN"]
os.environ["OPENAI_API_KEY"] = OPENAI_KEY

st.title("My Salesforce Cafe Bot")

articles = st.selectbox("Choose article",[
    'https://en.wikipedia.org/wiki/Nataraja_Temple,_Chidambaram',
    'https://docs.embedchain.ai/get-started/quickstart',
    'https://www.forbes.com/profile/elon-musk',
    'https://en.wikipedia.org/wiki/India',
    'https://youtu.be/ZdFSSapVheg?list=PLQFXjdhnRRn9BDb-jS2w7JHusVa33hV9J',
    'https://youtu.be/K4Ldwk7JDgE?list=PLQFXjdhnRRn9BDb-jS2w7JHusVa33hV9J',
    'https://youtu.be/WCtohZxo7Xs?list=PLQFXjdhnRRn9BDb-jS2w7JHusVa33hV9J'
])


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Function for generating LLM response
def generate_response(prompt, data):
    try:
        chatbot = App()
        print('data::' + data)
        chatbot.add(data)
        response = chatbot.query(prompt)
        return response
    except Exception as e:
        return f"Error generating response: {e}"

# Create containers for user input and responses
user_input_container = st.container()
response_container = st.container()

# User input
with user_input_container:
    user_input = st.chat_input("Type your message here:")

# Process user input
if user_input:    

     # Display user message
    with response_container:
        # Display a spinner while generating the response
        with st.spinner("Generating response..."):
            response = generate_response(user_input, articles)
        
    
    # Display user message
    with response_container:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display chatbot response
    with response_container:
        # Display chatbot response
        with st.chat_message("assistant"):
            st.markdown(response)
    
    # Add chatbot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with response_container:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
