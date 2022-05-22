from ipaddress import ip_address
import os
import asyncio
from pyppeteer import launch
from dotenv import load_dotenv

load_dotenv()


async def main():
    browser = await launch(
        ignoreHTTPSErrors=True,
        headless=True,
        executablePath=os.getenv("CHROMIUM_PATH"),
    )
    page = await browser.newPage()
    url = os.getenv("UNIFI_CONTROLLER_URL")
    await page.goto(f"{url}/manage")

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
        await page.waitForXPath("//button/span/span/span[contains(text(), Reconnect)]")
        await page.waitFor(1000)
        reconnectButton = await page.xpath(
            "//button/span/span/span[contains(text(), Reconnect)]"
        )
        await reconnectButton[0].click()

        # Wait for the client to disappear
        await page.waitForFunction(
            f"!document.querySelector(`span[data-label='{ip_address}']`)"
        )
        await page.waitFor(1000)

    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
