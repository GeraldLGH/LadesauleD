from playwright.sync_api import sync_playwright, TimeoutError

# Login-Daten
USERNAME = "g.luettgens@itergo.com"
PASSWORD = "m00racL.6005"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 1️⃣ Login
    page.goto("https://duesseldorf.ergoladesaeulen.de/wp-login.php?redirect_to=%2F")
    page.fill('input[name="log"]', USERNAME)
    page.fill('input[name="pwd"]', PASSWORD)
    page.press('input[name="pwd"]', 'Enter')

    # 2️⃣ Warten bis Seite geladen ist
    page.wait_for_load_state('networkidle')

    # 3️⃣ Screenshot nach Login
    page.screenshot(path="screenshot_login.png")
    with open("page_login.html", "w", encoding="utf-8") as f:
        f.write(page.content())
    print("Login-Screenshot und HTML gespeichert")

    # 4️⃣ Auf "Morgen" klicken (Teiltext)
    try:
        page.locator("text=Morgen").first.click()
        print('"Morgen" angeklickt')
    except TimeoutError:
        print('Fehler: "Morgen" nicht gefunden')
        browser.close()
        exit(1)

    # 5️⃣ Funktion zur Slot-Auswahl
    def select_slot(first_option_index):
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

        # Prüfen ob Slot frei ist
        slot_frei = "frei" in second_text.lower()
        return first_text, second_text, slot_frei

    # 6️⃣ Erstes Slot-Paar versuchen
    first_text, second_text, slot_frei = select_slot(0)

    # 7️⃣ Wenn nicht frei, zweiten Slot nehmen
    if not slot_frei:
        print("Kein freier Slot im ersten Eintrag, versuche zweiten Eintrag")
        first_text, second_text, slot_frei = select_slot(1)

    # 8️⃣ Screenshot nach Dropdown-Auswahl
    page.screenshot(path="screenshot_dropdown.png")
    with open("page_dropdown.html", "w", encoding="utf-8") as f:
        f.write(page.content())
    print("Dropdown-Screenshot und HTML gespeichert")

    # 9️⃣ Auf "Reservieren" klicken
    try:
        page.locator('button:has-text("Reservieren")').click()
        print('Reservieren angeklickt')
    except TimeoutError:
        print('Fehler: "Reservieren" Button nicht gefunden')
        browser.close()
        exit(1)

    # 10️⃣ Gewählte Slots ins Log
    print(f"Reserviert: {first_text} - {second_text} (frei={slot_frei})")

    # Browser schließen
    browser.close()
