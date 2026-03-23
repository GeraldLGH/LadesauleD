from playwright.sync_api import sync_playwright
from config import load_config
import time

def run():
    config = load_config()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Webseite öffnen
        page.goto(config["url"])

        # 2 + 3. Login ausfüllen
        page.fill("#user_login", config["email"])
        page.fill("#user_pass", config["password"])

        # 4. Enter
        page.press("#user_pass", "Enter")

        # 5. Warten bis Login-Seite fertig geladen
        page.wait_for_load_state("networkidle")

        # Screenshot nach Login
        page.screenshot(path="1_after_login.png", full_page=True)

        # 6. Auf "Morgen" klicken (Morgen ist Anfang des Texts)
        try:
            page.get_by_text("Morgen", exact=False).click()
        except Exception as e:
            print("Fehler beim Klicken auf 'Morgen':", e)

        # Kurze Pause, damit Seite vollständig lädt
        time.sleep(2)

        # Screenshot nach Klick auf "Morgen"
        page.screenshot(path="2_after_morgen.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    run()
