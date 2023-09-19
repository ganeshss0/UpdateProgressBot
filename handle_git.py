import subprocess
import os

# Change directory to 'GitHub Repo'
repo_directory = "my_data"
os.chdir(repo_directory)

# Run the Python script within 'GitHub Repo' (replace 'script.py' with your script's name)
subprocess.run(["python", "visualization.py"])

# Commit and push changes within 'GitHub Repo'
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Update Progress"])
subprocess.run(["git", "push", "origin", "main"])
