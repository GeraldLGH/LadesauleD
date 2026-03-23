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

        # 1 "Morgen" klicken
        page.get_by_text("Morgen", exact=False).click()

        page.wait_for_timeout(2000)

        # Screenshot nach "Morgen"
        page.screenshot(path="2_after_morgen.png")

        # Dropdowns holen
        selects = page.locator("select")

        first = selects.nth(0)
        second = selects.nth(1)

        # Optionen auslesen
        first_options = first.locator("option")
        second_options = second.locator("option")

        first_count = first_options.count()
        second_count = second_options.count()

        log_text = ""

        try:
            # 2A erster Eintrag
            first.select_option(index=0)

            # 2B letzter Eintrag
            second.select_option(index=second_count - 1)

            selected_1 = first_options.nth(0).inner_text()
            selected_2 = second_options.nth(second_count - 1).inner_text()

            log_text = f"Freier Slot: {selected_1} -> {selected_2}"

        except Exception:
            # 3A + 3B Fallback
            first.select_option(index=1)
            second.select_option(index=second_count - 1)

            selected_1 = first_options.nth(1).inner_text()
            selected_2 = second_options.nth(second_count - 1).inner_text()

            log_text = f"Fallback Slot: {selected_1} -> {selected_2}"

        # Screenshot nach Auswahl
        page.screenshot(path="3_after_dropdown.png")

        # 4 Reservieren klicken
        page.get_by_role("button", name="Reservieren").click()

        # Log speichern
        with open("log.txt", "w", encoding="utf-8") as f:
            f.write(log_text)

        print(log_text)

        page.wait_for_timeout(3000)
        browser.close()


if __name__ == "__main__":
    run()
