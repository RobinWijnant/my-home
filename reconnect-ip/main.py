import os
import asyncio
from pyppeteer import launch
from dotenv import load_dotenv

load_dotenv()


async def main():
    browser = await launch(ignoreHTTPSErrors=True, headless=True, executablePath=os.getenv('CHROMIUM_PATH'))
    page = await browser.newPage()
    await page.goto(os.getenv("UNIFI_CONTROLLER_URL"))

    # Login
    await page.waitForSelector("input[name=username]")
    await page.waitForSelector("input[name=password]")
    await page.type("input[name=username]", os.getenv("USERNAME"))
    await page.type("input[name=password]", os.getenv("PASSWORD"))
    await page.click("#loginButton")

    # Reconnect client with given ip
    await page.waitForSelector("a[href='/manage/default/clients']")
    await page.click("a[href='/manage/default/clients']")
    await page.waitForSelector(f"span[data-label='{os.getenv('IP_ADDRESS')}']")
    await page.click(f"span[data-label='{os.getenv('IP_ADDRESS')}']")
    await page.waitForSelector("button[name=reconnect-client]")
    await page.waitFor(1000)
    await page.click("button[name=reconnect-client]")

    # Wait for the client to disappear
    await page.waitForFunction(
        f"!document.querySelector(`span[data-label='{os.getenv('IP_ADDRESS')}']`)"
    )
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
