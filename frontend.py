# frontend.py
import streamlit as st
import requests

st.set_page_config(page_title="Engineering Agent Platform", layout="centered")

# This MUST render if Streamlit is working
st.title("Engineering Agent Platform")
st.markdown("Enter your engineering text and choose an agent.")

# Form UI
with st.form("agent_form"):
    user_input = st.text_area("Engineering Text", height=200)
    agent_type = st.selectbox("Select Agent", ["extract", "validate"])
    submitted = st.form_submit_button("Run Agent")

if submitted:
    if user_input.strip() == "":
        st.warning("Please enter some input.")
    else:
        try:
            response = requests.post(
                "http://localhost:8000/run",
                json={"user_input": user_input, "agent_type": agent_type}
            )
            if response.status_code == 200:
                result = response.json().get("result", "")
                st.success("Result:")
                st.code(result)
            else:
                st.error(f"API Error: {response.status_code}")
        except Exception as e:
            st.error(f"Request failed: {e}")
