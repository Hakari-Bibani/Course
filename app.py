import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Function to save user submission
def save_to_csv(data, username):
    # Create a DataFrame
    df = pd.DataFrame([data])
    # Create CSV file path
    filename = f"{username}_submission.csv"
    # Save the file in the current directory (or adjust the path as needed)
    df.to_csv(filename, index=False)

    # Use GitHub API or Git integration to push to your repository
    st.success("Submission saved successfully!")

# Chemistry test questions
questions = [
    {"question": "What is the atomic number of Hydrogen?", "options": ["1", "2", "3", "4"]},
    {"question": "What is the chemical symbol for Gold?", "options": ["Au", "Ag", "Pb", "Pt"]},
    {"question": "What is the formula for water?", "options": ["H2O", "O2", "CO2", "CH4"]},
    {"question": "What is the pH of a neutral solution?", "options": ["7", "5", "9", "1"]},
    {"question": "Which gas is essential for respiration?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Helium"]},
    {"question": "What is the chemical symbol for Sodium?", "options": ["Na", "K", "Ca", "Mg"]},
    {"question": "Which of these is a noble gas?", "options": ["Argon", "Hydrogen", "Oxygen", "Carbon"]},
    {"question": "What is the chemical formula for table salt?", "options": ["NaCl", "KCl", "MgCl2", "CaCl2"]},
]

# Streamlit app
def main():
    st.title("Chemistry Test")

    # Display an image
    st.image("images/test_image.jpg", caption="Welcome to the Chemistry Test")

    # User details
    name = st.text_input("Name:")
    school = st.text_input("School:")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    # Verify password
    if password == "Hakari":
        st.success("Password verified. You may proceed!")
        
        # Display questions
        answers = {}
        for i, q in enumerate(questions, 1):
            st.write(f"**Q{i}: {q['question']}**")
            answers[f"Q{i}"] = st.radio(f"Select an answer for Q{i}:", q["options"], key=f"q{i}")

        # Submit button
        if st.button("Submit"):
            # Ensure all questions are answered
            if None in answers.values():
                st.error("Please answer all questions!")
            else:
                # Collect user data and answers
                submission_data = {
                    "Name": name,
                    "School": school,
                    "Username": username,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    **answers,
                }

                # Save submission as a CSV file
                save_to_csv(submission_data, username)

    elif password and password != "Hakari":
        st.error("Invalid password! Please try again.")

if __name__ == "__main__":
    main()
