import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# GitHub configuration
GITHUB_REPO = "Hakari-Bibani/Course"  # Replace with your repo
GITHUB_BRANCH = "main"  # Replace with your branch name
GITHUB_TOKEN = os.getenv("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")  # Store your token as an environment variable

# Function to save data to GitHub as a CSV file
def save_to_github(data, username):
    if not GITHUB_TOKEN:
        st.error("GitHub token is not set. Please configure your environment.")
        return

    # Create a DataFrame
    df = pd.DataFrame([data])
    csv_content = df.to_csv(index=False)

    # Prepare the GitHub API URL and headers
    file_name = f"{username}_submission.csv"
    github_api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_name}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    # Check if the file already exists
    response = requests.get(github_api_url, headers=headers)
    if response.status_code == 200:
        # If the file exists, get the SHA for updating
        sha = response.json().get("sha")
        payload = {
            "message": f"Update submission by {username}",
            "content": csv_content.encode("utf-8").decode("latin1"),
            "branch": GITHUB_BRANCH,
            "sha": sha,
        }
    else:
        # If the file does not exist, create a new one
        payload = {
            "message": f"Add submission by {username}",
            "content": csv_content.encode("utf-8").decode("latin1"),
            "branch": GITHUB_BRANCH,
        }

    # Make a PUT request to upload the file
    response = requests.put(github_api_url, json=payload, headers=headers)

    if response.status_code in [200, 201]:
        st.success(f"Submission saved to GitHub as {file_name}")
    else:
        st.error(f"Failed to save submission to GitHub: {response.json()}")

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

                # Save submission to GitHub
                save_to_github(submission_data, username)

    elif password and password != "Hakari":
        st.error("Invalid password! Please try again.")

if __name__ == "__main__":
    main()
