import os

import streamlit as st
# from dotenv import load_dotenv

# load_dotenv()

# def initiate_session_state():
#     # Env variables
#     if 'token' not in st.session_state:
#         st.session_state.token = os.getenv("DATAROBOT_API_TOKEN")
#     if 'endpoint' not in st.session_state:
#         st.session_state.endpoint = os.getenv("DATAROBOT_API_ENDPOINT")

def initiate_session_state():
    # Env variables
    if 'token' not in st.session_state:
        st.session_state.token = st.secrets["DATAROBOT_API_TOKEN"]
    if 'endpoint' not in st.session_state:
        st.session_state.endpoint = st.secrets["DATAROBOT_API_ENDPOINT"]
