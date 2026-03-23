from playwright.sync_api import sync_playwright

URL = "https://duesseldorf.ergoladesaeulen.de/wp-login.php?redirect_to=%2F"

EMAIL = "g.luettgens@itergo.com"
PASSWORD = "m00racL.6005"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1 Seite öffnen
        page.goto(URL)

        # 2 + 3 Felder ausfüllen
        page.fill("#user_login", EMAIL)
        page.fill("#user_pass", PASSWORD)

        # 4 Enter drücken
        page.press("#user_pass", "Enter")

        # Warten bis Seite geladen ist
        page.wait_for_load_state("networkidle")

        # 5 Screenshot
        page.screenshot(path="login_result.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    run()
