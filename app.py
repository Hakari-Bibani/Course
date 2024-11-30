import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# GitHub configuration
GITHUB_REPO = "Hakari-Bibani/Course"  # Replace with your repo
GITHUB_BRANCH = "main"  # Replace with your branch name

# Load GitHub token from Streamlit Secrets
try:
    GITHUB_TOKEN = st.secrets["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"]
    if not GITHUB_TOKEN:
        st.error("GitHub token is empty. Please check your secrets configuration.")
except Exception as e:
    st.error(f"Error accessing GitHub token: {e}")
    GITHUB_TOKEN = None

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
    headers = {"Authorization": f"Bearer {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}"}

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
    response = requests.
