import requests
import base64

def fetch_file(owner, repo, path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    headers = {
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("GitHub API error:", response.status_code)
        return None

    data = response.json()

    content = data.get("content", "")

    decoded = base64.b64decode(content).decode("utf-8")

    return decoded