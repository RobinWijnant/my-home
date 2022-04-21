from ipaddress import ip_address
import os
import asyncio
from pyppeteer import launch
from dotenv import load_dotenv

load_dotenv()


async def main():
    browser = await launch(
        ignoreHTTPSErrors=True,
        headless=False,
        executablePath=os.getenv("CHROMIUM_PATH"),
    )
    page = await browser.newPage()
    await page.goto(os.getenv("UNIFI_CONTROLLER_URL"))

    # Login
    await page.waitForSelector("input[name=username]")
    await page.waitForSelector("input[name=password]")
    await page.type("input[name=username]", os.getenv("USERNAME"))
    await page.type("input[name=password]", os.getenv("PASSWORD"))
    await page.click("#loginButton")

    # Navigate to clients overview page
    await page.waitForSelector("a[href='/manage/default/clients']")
    await page.click("a[href='/manage/default/clients']")

    ip_addresses = os.getenv("IP_ADDRESS").split(",")
    for ip_address in ip_addresses:
        # Reconnect client with given ip
        await page.waitForSelector(f"span[data-label='{ip_address}']")
        await page.click(f"span[data-label='{ip_address}']")
        await page.waitForSelector("button[name=reconnect-client]")
        await page.waitFor(1000)
        await page.click("button[name=reconnect-client]")

        # Wait for the client to disappear
        await page.waitForFunction(
            f"!document.querySelector(`span[data-label='{ip_address}']`)"
        )
        await page.waitFor(1000)

    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
