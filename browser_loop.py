import asyncio
import base64
import requests
from playwright.async_api import async_playwright

API_URL = "http://127.0.0.1:8000"


visited_files = set()


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
        "instruction": "Only choose from these files. Prefer Python source files and folders containing source code. Avoid README.md."
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

        if target:

            link = page.locator(
                f"tbody a.Link--primary[title='{target}']"
            ).first

            href = await link.get_attribute("href")

            if href:
                await page.goto(f"https://github.com{href}")

            await page.wait_for_load_state("networkidle")

    elif act == "OPEN_FILE":

        target = action.get("target")

        if not target:
            return

        if target in visited_files:
            print("Already parsed:", target)
            return

        visited_files.add(target)

        if target:

            file_link = page.locator(
                f"tbody a.Link--primary[title='{target}']"
            ).first

            if await file_link.count() == 0:
                print("File not found in current view:", target)
                return

            href = await file_link.get_attribute("href")

            if href:
                await page.goto(f"https://github.com{href}")

            await page.wait_for_load_state("networkidle")
            await page.wait_for_selector("table.js-file-line-container")

        locator = page.locator("table.js-file-line-container")

        if await locator.count() == 0:
            print("No code table found — file probably not opened.")
            return

        code = await locator.inner_text()

        with open("temp_file.py","w", encoding="utf-8") as f:
            f.write(code)

        from sources.structure_extractor import analyze_file

        analysis = analyze_file("temp_file.py")

        print("Parsed structure:", analysis)

        from sources.firestore_client import save_file_analysis

        save_file_analysis("fastapi_repo", analysis)

        # go back to folder view
        await page.go_back()
        await page.wait_for_load_state("networkidle")

    elif act == "SCROLL":
        # await page.mouse.wheel(0, 800)
        await page.evaluate("window.scrollBy(0, 1000)")

    elif act == "SEARCH":
        print("Search not implemented yet")

    print("Executed:", act)


async def main():

    print("Starting browser agent")

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(
            viewport={"width": 1600, "height": 1000}
        )

        await page.goto("https://github.com/fastapi/fastapi")

        for _ in range(4):

            print("\n===== LOOP START =====")

            screenshot_base64 = await take_screenshot(page)
            print("Screenshot taken")

            # await page.wait_for_selector('[data-testid="tree-item-file-name"]')
            files = list(set(await page.locator("tbody a.Link--primary").all_inner_texts()))

            # prefer python files
            py_files = [f for f in files if f.endswith(".py")]

            # otherwise explore folders
            folders = [f for f in files if "." not in f]

            if py_files:
                files = py_files
            elif folders:
                files = folders

            print("Filtered files:", files)

            analysis = await analyze_repo(screenshot_base64)
            print("Analysis received:", analysis)

            action = await plan_action(analysis, files)
            print("Action received:", action)

            await execute_action(page, action)

            await asyncio.sleep(2)   # ← delay between cycles

            print("===== LOOP END =====\n")


asyncio.run(main())