from playwright.sync_api import sync_playwright

# Login-Daten (später kannst du das in config.json auslagern)
USERNAME = "g.luettgens@itergo.com"
PASSWORD = "abcdefgh"

with sync_playwright() as p:
    # Browser im Headless-Modus starten
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Webseite aufrufen
    page.goto("https://duesseldorf.ergoladesaeulen.de/wp-login.php")

    # Benutzername eintragen
    page.fill('input[name="log"]', USERNAME)

    # Passwort eintragen
    page.fill('input[name="pwd"]', PASSWORD)

    # Enter drücken (Login absenden)
    page.press('input[name="pwd"]', 'Enter')

    # Optional: warten, bis die nächste Seite geladen ist
    page.wait_for_load_state('networkidle')

    # Seite Titel ausgeben zur Kontrolle
    print("Aktuelle Seite:", page.title())

    browser.close()
