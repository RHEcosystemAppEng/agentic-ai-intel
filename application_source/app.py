import streamlit as st

# Placeholder for your backend function
def submitQuery(query: str) -> str:
    # Replace this with your actual logic
    return f"Echo: {query}"

# Streamlit UI
st.set_page_config(page_title="Minimal Chatbot", layout="centered")

st.markdown(
    """
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .stTextArea > div > textarea {
        font-size: 16px;
        color: #333;
        background-color: #f8f8f8;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("💬 Minimal Chatbot")

query = st.text_input("Type your message:")

if query:
    response = submitQuery(query)
    st.text_area("Response:", value=response, height=100, max_chars=None, key=None)
