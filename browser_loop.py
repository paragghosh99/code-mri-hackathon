import asyncio
import base64
import requests
from playwright.async_api import async_playwright
from helper.github_api import fetch_file
from helper.get_current_folder import get_current_folder
import sys
sys.stdout.reconfigure(encoding="utf-8")

API_URL = "http://127.0.0.1:8000"


visited_files = set()
visited_folders = set()


async def take_screenshot(page):

    await page.screenshot(path="repo.jpg")

    with open("repo.jpg", "rb") as f:
        return base64.b64encode(f.read()).decode()


async def analyze_repo(image_base64):

    payload = {
        "instruction": "Analyze this GitHub repository layout",
        "image_base64": image_base64
    }

    r = requests.post(f"{API_URL}/analyze", json=payload)

    print("Analyze status:", r.status_code)
    print("Analyze raw response:", r.text[:500])

    try:
        return r.json()["analysis"]
    except Exception as e:
        print("Analyze JSON parse error:", e)
        return {}


async def plan_action(analysis, files):

    payload = {
                "analysis": analysis,
                "files": files,
                "visited_files": list(visited_files),
                "visited_folders": list(visited_folders),
                "instruction": """
                Choose the next action.

                Rules:
                - Never choose files already in visited_files
                - Never choose folders already in visited_folders
                - Prefer unexplored Python files
                """
            }

    r = requests.post(f"{API_URL}/plan", json=payload)

    print("Plan status:", r.status_code)
    print("Plan raw response:", r.text[:500])

    try:
        return r.json()["action_plan"]
    except Exception as e:
        print("Plan JSON parse error:", e)
        return {"action": "SCROLL"}


async def execute_action(page, action):

    print("Executing:", action)

    act = action.get("action", "SCROLL")

    # coords = action.get("coordinates")

    if act == "CLICK":

        target = action.get("target")
        # normalize repo path → filename
        if "/" in target:
            target = target.split("/")[-1]

        if not target:
            return

        current_folder = get_current_folder(page.url)

        next_folder = f"{current_folder}/{target}" if current_folder != "root" else target

        if next_folder in visited_folders:
            print("Folder already explored:", next_folder)
            return

        link = page.locator(
            f"tbody a.Link--primary[title='{target}']"
        )

        if await link.count() == 0:
            print("Folder not found in current view:", target)

            # move to parent directory
            parent = page.locator("a[title='..']")

            if await parent.count() > 0:
                href = await parent.first.get_attribute("href")

                if href:
                    await page.goto(f"https://github.com{href}")
                    await page.wait_for_load_state("networkidle")

                print("Moved to parent directory")

            return

        href = await link.first.get_attribute("href")

        if href:
            await page.goto(f"https://github.com{href}")

        await page.wait_for_load_state("networkidle")

        visited_folders.add(next_folder)

        print("Entered folder:", next_folder)

    elif act == "OPEN_FILE":

        target = action.get("target")
        # normalize repo path → filename
        if "/" in target:
            target = target.split("/")[-1]

        if not target:
            return

        if target in visited_files:
            print("Already parsed:", target)
            return

        visited_files.add(target)

        # Confirm the file exists in the current folder view
        file_link = page.locator(
            f"tbody a.Link--primary[title='{target}']"
        ).first

        if await file_link.count() == 0:
            print("File not found in current view:", target)
            return

        # -------------------------------
        # Extract repo info dynamically
        # -------------------------------

        url = page.url
        parts = url.split("/")

        owner = parts[3]
        repo = parts[4]

        # -------------------------------
        # Determine current folder path
        # -------------------------------

        folder = ""

        if "tree/" in url:
            folder = url.split("tree/")[1]
            folder = "/".join(folder.split("/")[1:])


        # Build the file path inside repo
        path = f"{folder}/{target}" if folder else target

        # -------------------------------
        # Fetch file using GitHub API
        # -------------------------------

        code = fetch_file(owner, repo, path)

        if not code:
            print("Failed to fetch file from GitHub API")
            return


        print("Fetched code preview:")
        print(code[:500].encode("ascii", "ignore").decode())

        # -------------------------------
        # Save temporary file
        # -------------------------------

        with open("temp_file.py", "w", encoding="utf-8") as f:
            f.write(code)

        # -------------------------------
        # Analyze structure
        # -------------------------------

        from sources.structure_extractor import analyze_file

        analysis = analyze_file("temp_file.py")
        analysis["file"] = target

        print("Parsed structure:", analysis)

        # -------------------------------
        # Store in Firestore
        # -------------------------------

        from sources.firestore_client import save_file_analysis

        save_file_analysis(f"{owner}_{repo}", analysis)

    elif act == "SCROLL":
        # await page.mouse.wheel(0, 800)
        await page.evaluate("window.scrollBy(0, 1000)")

    elif act == "SEARCH":
        print("Search not implemented yet")

    print("Executed:", act)


async def main(owner, repo):

    print("Starting browser agent")

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(
            viewport={"width": 1600, "height": 1000}
        )

        # await page.goto("https://github.com/paragghosh99/task_app_auth_testing")
        repo_url = f"https://github.com/{owner}/{repo}"

        print("Opening repo:", repo_url)

        await page.goto(repo_url)

        for _ in range(20):

            print("\n===== LOOP START =====")

            screenshot_base64 = await take_screenshot(page)
            print("Screenshot taken")

            # await page.wait_for_selector('[data-testid="tree-item-file-name"]')
            files = list(set(await page.locator("tbody a.Link--primary").all_inner_texts()))

            if not files:
                print("No more files to explore. Stopping crawler.")
                break

            # prefer python files
            py_files = [f for f in files if f.endswith(".py")]

            # otherwise explore folders
            folders = [f for f in files if "." not in f]
            # ignore GitHub parent navigation
            folders = [f for f in folders if f != ".."]

            # prefer unexplored folders first (repo exploration)
            current_folder = get_current_folder(page.url)

            files = []

            for f in folders:
                candidate = f"{current_folder}/{f}" if current_folder != "root" else f
                if candidate not in visited_folders:
                    files.append(f)

            # if no folders left, parse python files
            if not files:
                files = [f for f in py_files if f not in visited_files]

            print("Filtered files:", files)

            if not files:
                print("Nothing left to explore here. Going back.")
                await page.go_back()
                continue

            analysis = await analyze_repo(screenshot_base64)
            print("Analysis received:", analysis)

            action = await plan_action(analysis, files)
            print("Action received:", action)

            await execute_action(page, action)

            await asyncio.sleep(2)   # ← delay between cycles

            print("===== LOOP END =====\n")


# asyncio.run(main())
def run_crawler(owner, repo):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(owner, repo))