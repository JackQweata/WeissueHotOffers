from pyppeteer import launch


async def run_pyppeteer():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.82 Safari/537.36'
    }

    browser = await launch({"headless": True, "args": ["--start-maximized"]})
    page = await browser.newPage()
    await page.setExtraHTTPHeaders(headers)

    return browser, page
