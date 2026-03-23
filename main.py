from playwright.sync_api import sync_playwright

# Login-Daten (später kannst du das in config.json auslagern)
USERNAME = "g.luettgens@itergo.com"
PASSWORD = "m00racL.6005"

from playwright.sync_api import sync_playwright, TimeoutError

# Login-Daten
USERNAME = "g.luettgens@itergo.com"
PASSWORD = "abcdefgh"

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

    # 3️⃣ Auf "morgen" klicken
    page.click('button:has-text("morgen")')

    # 4️⃣ Funktion zum Slot auswählen
    def select_slot(first_option_index):
        # Dropdowns
        first_dropdown = page.locator('select[name="Zeitslot"]')
        second_dropdown = page.locator('select[name="Säulenr."]')

        # Erste Auswahl
        first_dropdown.select_option(index=first_option_index)

        # Zweite Auswahl: letzter Eintrag
        options_count = second_dropdown.locator('option').count()
        second_dropdown.select_option(index=options_count - 1)

        # Ausgewählte Texte
        first_text = first_dropdown.locator('option:checked').inner_text()
        second_text = second_dropdown.locator('option:checked').inner_text()

        # Prüfen ob Slot frei ist (falls Text "frei" enthält)
        slot_frei = "frei" in second_text.lower()
        return first_text, second_text, slot_frei

    # 4A/4B: Erstes Slot-Paar versuchen
    first_text, second_text, slot_frei = select_slot(0)

    # 5A/5B: Wenn nicht frei, zweites Slot-Paar
    if not slot_frei:
        print("Kein freier Slot im ersten Eintrag, versuche zweiten Eintrag")
        first_text, second_text, slot_frei = select_slot(1)

    # 6️⃣ Auf Reservieren klicken
    page.click('button:has-text("Reservieren")')

    # 7️⃣ Loggen der gewählten Slots
    print(f"Reserviert: {first_text} - {second_text} (frei={slot_frei})")

    browser.close()
