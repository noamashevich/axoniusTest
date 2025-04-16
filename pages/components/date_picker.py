from utils.date_utils import to_airbnb_date_label


class DatePickerComponent:
    def __init__(self, page):
        self.page = page
        self.check_in_button = page.locator('[data-testid="structured-search-input-field-split-dates-0"]')
        self.calendar_root = page.locator('[data-testid="structured-search-input-field-dates-panel"]')
        self.next_month_button = page.locator('button[aria-label="Move forward to switch to the next month."]')
        self.date_cell = lambda date: page.locator(f'button[aria-label*="{date}"]')

    def open(self):
        self.check_in_button.click()
        self.page.wait_for_timeout(500)
        if self.calendar_root.count() == 0:
            self.check_in_button.click()
            self.page.wait_for_timeout(1000)
        assert self.calendar_root.count() > 0, "Calendar is not open after clicking Check in"

    def go_to_month_of(self, date_label):
        for i in range(12):
            if self.date_cell(date_label).is_visible():
                print(f"Found {date_label} in month {i+1}")
                return
            print(f"Moving to next month (attempt {i+1})")
            self.next_month_button.click()
            self.page.wait_for_timeout(1000)

    def select_range(self, check_in: str, check_out: str):
        self.open()
        check_in_label = to_airbnb_date_label(check_in)
        check_out_label = to_airbnb_date_label(check_out)

        for _ in range(5):
            count = self.page.locator("button[aria-label]").count()
            if count > 0:
                break
            self.page.wait_for_timeout(500)

        self.go_to_month_of(check_in_label)
        self.date_cell(check_in_label).click()

        self.go_to_month_of(check_out_label)
        self.date_cell(check_out_label).click()
