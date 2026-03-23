from playwright.sync_api import sync_playwright

URL = "https://duesseldorf.ergoladesaeulen.de/wp-login.php?redirect_to=%2F"

EMAIL = "g.luettgens@itergo.com"
PASSWORD = "m00racL.6005"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # True = ohne UI
        page = browser.new_page()

        # 1 Seite öffnen
        page.goto(URL)

        # 2 + 3 Login
        page.fill("#user_login", EMAIL)
        page.fill("#user_pass", PASSWORD)

        # 4 Enter
        page.press("#user_pass", "Enter")

        # Warten bis neue Seite geladen ist
        page.wait_for_load_state("networkidle")

        # Screenshot nach Login
        page.screenshot(path="1_after_login.png")

        

        # Log speichern
        with open("log.txt", "w", encoding="utf-8") as f:
            f.write(log_text)

        print(log_text)

        page.wait_for_timeout(3000)
        browser.close()


if __name__ == "__main__":
    run()
