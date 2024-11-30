import streamlit as st
import pandas as pd
import requests
import base64
from io import StringIO  # Import StringIO to handle string-based file reading
from datetime import datetime
from question import questions
from style import set_style, show_header_image

# GitHub configuration
GITHUB_REPO = "Hakari-Bibani/Course"
GITHUB_BRANCH = "main"
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
FILE_NAME = "submissions.csv"  # Single CSV file for all submissions

# Function to calculate grade
def calculate_grade(answers):
    total_marks = 0
    for i, q in enumerate(questions):
        if answers.get(f"Q{i + 1}") == q["correct"]:
            total_marks += q["marks"]
    return total_marks

# Function to fetch existing CSV file from GitHub
def fetch_existing_data():
    github_api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_NAME}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    response = requests.get(github_api_url, headers=headers)
    if response.status_code == 200:
        content = response.json().get("content")
        sha = response.json().get("sha")
        decoded_content = base64.b64decode(content).decode("utf-8")
        existing_df = pd.read_csv(StringIO(decoded_content))  # Use StringIO for reading CSV content
        return existing_df, sha
    elif response.status_code == 404:
        # File does not exist
        return None, None
    else:
        st.error(f"Failed to fetch existing file from GitHub: {response.json()}")
        return None, None

# Function to save data to GitHub as a single CSV file
def save_to_github(new_data):
    # Fetch existing data
    existing_df, sha = fetch_existing_data()
    if existing_df is not None:
        # Append new data to existing data
        updated_df = pd.concat([existing_df, new_data], ignore_index=True)
    else:
        # If no existing data, create new DataFrame
        updated_df = new_data

    # Convert updated data to CSV
    csv_content = updated_df.to_csv(index=False)
    # Encode CSV content in Base64
    encoded_content = base64.b64encode(csv_content.encode()).decode()

    # Prepare GitHub API payload
    github_api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_NAME}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    payload = {
        "message": "Update submissions",
        "content": encoded_content,
        "branch": GITHUB_BRANCH,
    }

    if sha:
        # Include SHA if file exists
        payload["sha"] = sha

    # Make a PUT request to upload the file
    response = requests.put(github_api_url, json=payload, headers=headers)

    if response.status_code in [200, 201]:
        st.success("Thank you for participation!")
    else:
        st.error(f"Failed to save submission to GitHub: {response.json()}")

# Main Streamlit app
def main():
    set_style()  # Apply custom styling
    st.title("تاقیکردنەوەی بەندی دووەم - کیمیا- مامۆستا هەکاری")
    show_header_image()

    # User details
    st.header("زانیاری")
    name = st.text_input(":ناو")
    school = st.text_input(":ناوی قوتابخانە")
    username = st.text_input("ناوی بەکارهاتوو:")
    password = st.text_input(":کۆد", type="password")

    # Verify password
    if password == "Hakari":
        st.success("کۆدەکەت دروستە!")

        # Display questions
        st.header("وەڵامی هەموو پرسیارەکانی خوارەوە بدەرەوە")
        answers = {}
        for i, q in enumerate(questions, 1):
            st.write(f"**Q{i}: {q['question']}**")
            answers[f"Q{i}"] = st.radio(f"Select an answer for Q{i}:", q["options"], key=f"q{i}")

        # Submit button
        if st.button("ناردن"):
            # Ensure all questions are answered
            if None in answers.values():
                st.error("Please answer all questions!")
            else:
                # Calculate grade
                total_marks = calculate_grade(answers)

                # Collect user data and answers
                submission_data = pd.DataFrame([{
                    "Name": name,
                    "School": school,
                    "Username": username,
                    "Total Marks": total_marks,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    **answers,
                }])

                # Save submission to GitHub
                save_to_github(submission_data)

    elif password and password != "Hakari":
        st.error("هەڵەیە، کۆدی دروست بنووسە.")

if __name__ == "__main__":
    main()
