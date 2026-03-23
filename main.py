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

        # 4. Enter drücken
        page.press("#user_pass", "Enter")

        # 5. Warten bis Login geladen
        page.wait_for_timeout(5000)
        page.screenshot(path="1_after_login.png", full_page=True)

        # 6. Auf "Morgen" klicken
        # hier zum Test Heute
        try:
            page.get_by_text("Heute", exact=False).click()
        except Exception as e:
            print("Fehler beim Klicken auf 'Morgen':", e)

        time.sleep(3)
        page.screenshot(path="2_after_morgen.png", full_page=True)

        # 8/9 Dropdown Auswahl mit Tab Steuerung

        # Fokus auf erstes Dropdown, wähle ersten "echten" Eintrag (Index 1)
        first_dropdown = page.locator("select").nth(0)
        first_dropdown.focus()
        page.keyboard.press("ArrowDown")  # Zum ersten echten Eintrag springen
        page.keyboard.press("Enter")      # Auswahl bestätigen

        # Tab zum zweiten Dropdown
        page.keyboard.press("Tab")
        page.keyboard.press("ArrowDown")  # Zum ersten echten Eintrag springen
        page.keyboard.press("Enter")      # Auswahl bestätigen

        
        # Optional Screenshot nach Dropdown Auswahl
        time.sleep(1)
        page.screenshot(path="3_after_dropdown.png", full_page=True)

        # 10. Auf RESERVIEREN klicken
        try:
            page.get_by_role("button", name="RESERVIEREN").click()
            time.sleep(3)
            page.screenshot(path="4_after_reservieren.png", full_page=True)
            log_text = "Reservierung: Button geklickt"
        except Exception as e:
            log_text = f"Reservierung: Fehler beim Klick auf RESERVIEREN - {e}"

        print(log_text)
        with open("log.txt", "w", encoding="utf-8") as f:
            f.write(log_text)

        browser.close()

if __name__ == "__main__":
    run()
