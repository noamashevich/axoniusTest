import time
from utils.date_utils import to_airbnb_date_label, get_date_from_today
from pages.base_page import BasePage
from playwright.sync_api import Page

class AirbnbPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.location_input = page.locator('input[placeholder*="Search"]')
        self.suggestion_by_text = lambda city: page.locator(f'div[role="option"] >> text="{city}"')

        self.check_in_field = page.get_by_role("button", name="Check in Add dates")
        self.check_out_field = page.get_by_role("button", name="Check out Add dates")

        self.date_cell = lambda date: page.locator(f'button[aria-label*=\"{date}\"]')
        self.search_button = page.locator('button[aria-label="Search"]')
        self.next_month_button = page.locator('button[aria-label="Move forward to switch to the next month."]')
        self.calendar_root = page.locator('[data-testid="structured-search-input-field-dates-panel"]')

    def go_to_homepage(self):
        self.navigate("https://www.airbnb.com/")
        self.page.wait_for_load_state("networkidle")

    def enter_location(self, city: str):
        self.click(self.location_input)
        self.fill(self.location_input, city)
        self.page.locator('div[role="option"]').first.click()

    def go_to_month_of_date(self, date_label: str):
        for i in range(12):
            if self.date_cell(date_label).is_visible():
                print(f"✔ Found {date_label} in month {i+1}")
                break
            print(f"➡ Moving to next month (attempt {i+1})")
            self.click(self.next_month_button)
            self.page.wait_for_timeout(1000)

    def select_dates(self, check_in: str, check_out: str):
        check_in_label = to_airbnb_date_label(check_in)
        check_out_label = to_airbnb_date_label(check_out)

        self.wait_for_element(self.check_in_field)
        self.click(self.check_in_field)

        self.page.wait_for_timeout(1000)
        if self.calendar_root.count() == 0:
            print("📌 Calendar auto-closed. Reopening it...")
            self.click(self.check_in_field)
            self.page.wait_for_timeout(1000)

        assert self.calendar_root.count() > 0, "❌ Calendar is not open after clicking Check in"
        print("✅ Calendar is open.")

        # 🔁 נמתין שהתאריכים באמת יופיעו ב-DOM
        for _ in range(5):
            count = self.page.locator("td[aria-label]").count()
            print("🔁 Date cell count:", count)
            if count > 0:
                break
            self.page.wait_for_timeout(500)

        self.go_to_month_of_date(check_in_label)
        self.wait_for_element(self.date_cell(check_in_label))
        self.click(self.date_cell(check_in_label))

        self.go_to_month_of_date(check_out_label)
        self.wait_for_element(self.date_cell(check_out_label))
        self.click(self.date_cell(check_out_label))

    def search(self):
        self.click(self.search_button)

