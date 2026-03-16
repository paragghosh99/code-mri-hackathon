import requests
from helper.github_api import fetch_file,headers
from sources.structure_extractor import analyze_file,analyze_code
from sources.firestore_client import save_file_analysis
# from browser_loop import run_crawler


def repo_analyzer(owner, repo):

    repo_id = f"{owner}_{repo}"

    try:

        # FAST PATH — GitHub API
        repo_meta = requests.get(f"https://api.github.com/repos/{owner}/{repo}",headers=headers)

        if repo_meta.status_code != 200:
            raise Exception("GitHub repo not accessible")

        default_branch = repo_meta.json()["default_branch"]

        url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"

        # r = requests.get(url)
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise Exception("GitHub tree fetch failed")

        data = r.json()

        files = data["tree"]

        py_files = [f["path"] for f in files if f["path"].endswith(".py")]

        print("Python files found:", len(py_files))

        for path in py_files:

            code = fetch_file(owner, repo, path)

            if not code:
                continue

            # with open("temp_file.py", "w", encoding="utf-8") as f:
            #     f.write(code)

            # analysis = analyze_file("temp_file.py")

            # # analysis["file"] = path.split("/")[-1]
            # analysis["file"] = path
            analysis = analyze_code(code, path)

            save_file_analysis(repo_id, analysis)

        print("Repo analysis complete (API mode)")

    except Exception as e:

        # print("API mode failed. Falling back to crawler:", e)

        # run_crawler(owner, repo)

        print("API mode failed:", e)
        return {"error": "Repository analysis failed"}
# repo_analyzer(owner="HOGLucifer",repo="code-mri")