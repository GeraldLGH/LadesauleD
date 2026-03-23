from playwright.sync_api import sync_playwright

USERNAME = "g.luettgens@itergo.com"
PASSWORD = "m00racL.6005"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    try:
        # Login
        page.goto("https://duesseldorf.ergoladesaeulen.de/wp-login.php?redirect_to=%2F")

        page.fill('input[name="log"]', USERNAME)
        page.fill('input[name="pwd"]', PASSWORD)
        page.press('input[name="pwd"]', 'Enter')

        # Warten
        page.wait_for_timeout(5000)

        # Screenshot 1
        page.screenshot(path="step1_after_login.png")
        print("Screenshot 1 gespeichert")
        print("URL:", page.url)

        # Versuch "Morgen" zu klicken
        try:
            page.locator("text=Morgen").first.click(timeout=5000)
            print("Morgen geklickt")
        except:
            print("Morgen NICHT gefunden")

        page.wait_for_timeout(3000)

        # Screenshot 2
        page.screenshot(path="step2_after_morgen.png")
        print("Screenshot 2 gespeichert")

        # 👉 TAB Navigation
        # Fokus setzen
        page.keyboard.press("Tab")  # erstes Feld
        page.keyboard.press("Tab")  # Zeitslot

        # Dropdown öffnen + erster Eintrag
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")

        print("Erster Dropdown gewählt")

        # Zum nächsten Dropdown
        page.keyboard.press("Tab")

        # Letzten Eintrag wählen (mehrfach runter)
        for _ in range(10):
            page.keyboard.press("ArrowDown")

        page.keyboard.press("Enter")

        print("Zweiter Dropdown gewählt")

        # Screenshot 3
        page.screenshot(path="step3_dropdowns.png")

        # Zum Reservieren Button
        page.keyboard.press("Tab")
        page.keyboard.press("Tab")
        page.keyboard.press("Enter")

        print("Reservieren gedrückt")

        # Screenshot 4
        page.wait_for_timeout(3000)
        page.screenshot(path="step4_result.png")

    except Exception as e:
        print("FEHLER:", str(e))

    finally:
        browser.close()
