from playwright.sync_api import sync_playwright, TimeoutError

# Login-Daten
USERNAME = "g.luettgens@itergo.com"
PASSWORD = "m00racL.6005"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 1️⃣ Login
    page.goto("https://duesseldorf.ergoladesaeulen.de/wp-login.php")
    page.fill('input[name="log"]', USERNAME)
    page.fill('input[name="pwd"]', PASSWORD)
    page.press('input[name="pwd"]', 'Enter')

    # 2️⃣ Warten bis die zweite Seite geladen ist
    page.wait_for_load_state('networkidle')


    ### zum Test
    # page.screenshot(path="screenshot.png")
    # print("Screenshot gespeichert: screenshot.png")

    page.screenshot(path="screenshot.png")
with open("page.html", "w", encoding="utf-8") as f:
    f.write(page.content())
page.wait_for_timeout(3000)
print("Screenshot und HTML gespeichert")



    browser.close()
