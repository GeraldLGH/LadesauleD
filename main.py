from playwright.sync_api import sync_playwright
from config import load_config
import time

def run():
    config = load_config()

    with sync_playwright() as p:
        # Browser sichtbar für Test, headless=True für GitHub später
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1. Webseite öffnen
        page.goto(config["url"])

        # 2 + 3. Login ausfüllen
        page.fill("#user_login", config["email"])
        page.fill("#user_pass", config["password"])

        # 4. Enter
        page.press("#user_pass", "Enter")

        # 5. Kurz warten, bis Login-Seite vollständig geladen ist
        page.wait_for_timeout(5000)

        # Screenshot nach Login
        page.screenshot(path="1_after_login.png", full_page=True)

        # 6. Auf "Morgen" klicken (Morgen ist Anfang des Texts)
        try:
            page.get_by_text("Morgen", exact=False).click()
        except Exception as e:
            print("Fehler beim Klicken auf 'Morgen':", e)

        # Kurz warten, damit Seite vollständig lädt
        time.sleep(3)

        # Screenshot nach Klick auf "Morgen"
        page.screenshot(path="2_after_morgen.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    run()
