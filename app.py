import streamlit as st
import pandas as pd
import requests
import base64  # Import for Base64 encoding
from datetime import datetime
from question import questions  # Import questions with marks and correct answers

# GitHub configuration
GITHUB_REPO = "Hakari-Bibani/Course"
GITHUB_BRANCH = "main"
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]

# Function to calculate grade
def calculate_grade(answers):
    total_marks = 0
    for i, q in enumerate(questions):
        if answers.get(f"Q{i + 1}") == q["correct"]:
            total_marks += q["marks"]
    return total_marks

# Function to save data to GitHub as a CSV file
def save_to_github(data, username):
    if not GITHUB_TOKEN:
        st.error("GitHub token is not set. Please configure your environment.")
        return

    # Create a DataFrame
    df = pd.DataFrame([data])
    csv_content = df.to_csv(index=False)
    # Encode the CSV content in Base64
    encoded_content = base64.b64encode(csv_content.encode()).decode()

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
            "content": encoded_content,
            "branch": GITHUB_BRANCH,
            "sha": sha,
        }
    elif response.status_code == 404:
        # If the file does not exist, create a new one
        payload = {
            "message": f"Add submission by {username}",
            "content": encoded_content,
            "branch": GITHUB_BRANCH,
        }
    else:
        st.error(f"Failed to fetch file status from GitHub: {response.json()}")
        return

    # Make a PUT request to upload the file
    response = requests.put(github_api_url, json=payload, headers=headers)

    if response.status_code in [200, 201]:
        st.success(f"Submission saved to GitHub as {file_name}")
    else:
        st.error(f"Failed to save submission to GitHub: {response.json()}")

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
                # Calculate grade
                total_marks = calculate_grade(answers)

                # Display total marks
                st.success(f"Your total marks: {total_marks}")

                # Collect user data and answers
                submission_data = {
                    "Name": name,
                    "School": school,
                    "Username": username,
                    "Total Marks": total_marks,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    **answers,
                }

                # Save submission to GitHub
                save_to_github(submission_data, username)

    elif password and password != "Hakari":
        st.error("Invalid password! Please try again.")

if __name__ == "__main__":
    main()
