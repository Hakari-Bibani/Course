# style.py

import streamlit as st

def set_style():
    # Set custom Streamlit page configuration
    st.set_page_config(
        page_title="Chemistry Test",
        page_icon="🧪",
        layout="centered",
    )
    
    # Apply CSS for better UI
    st.markdown(
        """
        <style>
        .main {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def show_header_image():
    # Display a header image
    st.image("images/test_image.jpg", caption="Welcome to the Chemistry Test")
