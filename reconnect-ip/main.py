import os
import asyncio
from pyppeteer import launch
from dotenv import load_dotenv

load_dotenv()


async def main():

    browser = await launch(ignoreHTTPSErrors=True, headless=False)
    page = await browser.newPage()
    await page.goto("https://192.168.1.10:8443")

    # Login
    await page.waitForSelector("input[name=username]")
    await page.waitForSelector("input[name=password]")
    await page.type("input[name=username]", os.getenv("USERNAME"))
    await page.type("input[name=password]", os.getenv("PASSWORD"))
    await page.click("#loginButton")
    await page.waitForNavigation()

    # Reconnect client with given ip
    await page.goto("https://192.168.1.10:8443/manage/default/clients")
    await page.waitForSelector(f"span[data-label='{os.getenv('IP_ADDRESS')}']")
    await page.click(f"span[data-label='{os.getenv('IP_ADDRESS')}']")
    await page.waitForSelector("button[name=reconnect-client]")
    await page.waitFor(1000)
    await page.click("button[name=reconnect-client]")

    await page.waitForFunction(
        f"!document.querySelector(`span[data-label='{os.getenv('IP_ADDRESS')}']`)"
    )
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
