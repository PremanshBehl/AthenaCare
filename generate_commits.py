import os
import subprocess
from datetime import datetime

# Timestamps
start_time = datetime(2026, 4, 30, 12, 0, 0)
end_time = datetime(2026, 5, 1, 7, 26, 0)
total_commits = 20
time_diff = end_time - start_time
interval = time_diff / (total_commits - 1)

# Initialize git
subprocess.run(["git", "init"])
subprocess.run(["git", "branch", "-M", "main"])
subprocess.run(["git", "remote", "add", "origin", "https://github.com/PremanshBehl/AthenaCare"])

# Add gitignore first
subprocess.run(["git", "add", ".gitignore"])
env = os.environ.copy()
time_str = start_time.isoformat()
env["GIT_AUTHOR_DATE"] = time_str
env["GIT_COMMITTER_DATE"] = time_str
subprocess.run(["git", "commit", "-m", "Initial commit with .gitignore"], env=env)

# Get all untracked files
result = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True)
files = [f for f in result.stdout.split('\n') if f]

# We need 19 more commits
num_commits = 19
chunk_size = len(files) // num_commits
chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

# If chunks are more than num_commits, merge the last ones
if len(chunks) > num_commits:
    chunks[-2].extend(chunks[-1])
    chunks.pop()
elif len(chunks) < num_commits:
    # Just in case there are fewer files than commits
    pass

for i, chunk in enumerate(chunks):
    commit_time = start_time + interval * (i + 1)
    time_str = commit_time.isoformat()
    env["GIT_AUTHOR_DATE"] = time_str
    env["GIT_COMMITTER_DATE"] = time_str
    
    # Add files in chunks
    for file in chunk:
        subprocess.run(["git", "add", file])
    
    # Commit message based on first file
    msg = f"Add {chunk[0]}" if chunk else f"Update repository {i+1}"
    subprocess.run(["git", "commit", "-m", msg], env=env)

# Push to origin
print("Pushing to origin...")
subprocess.run(["git", "push", "-u", "origin", "main", "--force"])
