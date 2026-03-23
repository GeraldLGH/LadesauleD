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

        # 5. Warten bis Login geladen
        page.wait_for_timeout(5000)
        page.screenshot(path="1_after_login.png", full_page=True)

        # 6. Auf "Morgen" klicken
        try:
            page.get_by_text("Morgen", exact=False).click()
        except Exception as e:
            print("Fehler beim Klicken auf 'Morgen':", e)

        time.sleep(3)
        page.screenshot(path="2_after_morgen.png", full_page=True)

        # 8. Dropdowns für freien Slot auswählen
        selects = page.locator("select")
        first_dropdown = selects.nth(0)
        second_dropdown = selects.nth(1)

        first_options = first_dropdown.locator("option")
        second_options = second_dropdown.locator("option")
        first_count = first_options.count()
        second_count = second_options.count()

        log_text = ""

        try:
            # 8A + 8B: erster Eintrag + letzter Eintrag
            first_dropdown.select_option(index=0)
            second_dropdown.select_option(index=second_count - 1)
            selected_1 = first_options.nth(0).inner_text()
            selected_2 = second_options.nth(second_count - 1).inner_text()
            log_text = f"Freier Slot: {selected_1} -> {selected_2}"
        except Exception:
            # 9A + 9B: Fallback
            first_dropdown.select_option(index=1)
            second_dropdown.select_option(index=second_count - 1)
            selected_1 = first_options.nth(1).inner_text()
            selected_2 = second_options.nth(second_count - 1).inner_text()
            log_text = f"Fallback Slot: {selected_1} -> {selected_2}"

        # 8C / 9C Screenshot nach Auswahl
        time.sleep(1)
        page.screenshot(path="3_after_dropdown.png", full_page=True)

        # Log ausgeben
        print(log_text)
        with open("log.txt", "w", encoding="utf-8") as f:
            f.write(log_text)

        browser.close()

if __name__ == "__main__":
    run()
