import asyncio
import base64
import requests
from playwright.async_api import async_playwright

API_URL = "http://127.0.0.1:8000"


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


async def plan_action(analysis):

    payload = {
        "analysis": analysis
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
    coords = action.get("coordinates")

    if act == "CLICK":
        if coords:
            await page.mouse.click(coords["x"], coords["y"])

    elif act == "OPEN_FILE":
        if coords:
            await page.mouse.click(coords["x"], coords["y"])

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
        page = await browser.new_page()

        await page.goto("https://github.com/fastapi/fastapi")

        for _ in range(10):

            print("\n===== LOOP START =====")

            screenshot_base64 = await take_screenshot(page)
            print("Screenshot taken")

            analysis = await analyze_repo(screenshot_base64)
            print("Analysis received:", analysis)

            action = await plan_action(analysis)
            print("Action received:", action)

            await execute_action(page, action)

            await asyncio.sleep(2)   # ← delay between cycles

            print("===== LOOP END =====\n")


asyncio.run(main())