from playwright.sync_api import sync_playwright

# Login-Daten
USERNAME = "g.luettgens@itergo.com"
PASSWORD = "m00racL.6005"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Seite aufrufen
    page.goto("hhttps://duesseldorf.ergoladesaeulen.de/wp-login.php?redirect_to=%2F")
    page.fill('input[name="log"]', USERNAME)
    page.fill('input[name="pwd"]', PASSWORD)
    page.press('input[name="pwd"]', 'Enter')

    # 2️⃣ Warten bis die zweite Seite geladen ist
    page.wait_for_load_state('networkidle')


    # Screenshot speichern
    page.screenshot(path="screenshot.png")

    # HTML speichern
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(page.content())

    print("Screenshot und HTML gespeichert")

    # Browser schließen
    browser.close()
