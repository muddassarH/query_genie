import os

import streamlit as st
import requests
from dotenv import load_dotenv

st.title("QueryGenie")
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")


FASTAPI_URL = f"{BACKEND_URL}/ask"  # change if deployed

# prompt = st.text_input("Enter your prompt")
prompt = st.text_area(
    "Enter your prompt",
    height=None,   # let Streamlit auto-adjust height
    placeholder="Type your query here..."
)

if st.button("Send"):
    if prompt.strip():
        with st.spinner("Sending request..."):
            try:
                response = requests.post(FASTAPI_URL, params={"prompt": prompt})

                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status", "unknown")
                    if status.lower() == "success":
                        st.success(f"Status: {status}")
                    else:
                        st.error(f"Status: {status}")

                    # Display SQL query in code block
                    sql = data.get("result", "")
                    if sql:
                        st.code(sql, language="sql")  # syntax highlighting
                else:
                    st.error(f"Server returned: {response.status_code}")
                    st.error(response.text)

            except Exception as e:
                st.error(f"Error contacting server: {e}")