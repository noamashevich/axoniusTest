import difflib

from pages.base_page import BasePage
from pages.components.guests_picker import GuestPickerComponent
from pages.components.date_picker import DatePickerComponent
from playwright.sync_api import Page
import re
import urllib.parse


class AirbnbPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.location_input = page.locator('[data-testid="structured-search-input-field-query"]')
        self.suggestion_by_text = lambda city: page.locator(f'div[role="option"] >> text="{city}"')
        self.search_button = page.locator('[data-testid="structured-search-input-search-button"]')
        self.date_picker = DatePickerComponent(page)
        self.guests_picker = GuestPickerComponent(page)

    def go_to_homepage(self):
        self.navigate("https://www.airbnb.com/")
        self.page.wait_for_load_state("networkidle")

    def enter_location(self, city: str):
        self.click(self.location_input)
        self.fill(self.location_input, city)

        options = self.page.locator('div[role="option"]')
        options.first.wait_for(state="visible", timeout=5000)

        matched = options.filter(has_text=city)

        try:
            matched.first.wait_for(state="visible", timeout=2000)
            matched.first.click()
        except: # No exact match, clicking first option
            options.first.click()

    def select_dates(self, check_in: str, check_out: str):
        self.date_picker.select_range(check_in, check_out)

    def select_guests(self, **kwargs):
        self.guests_picker.set_guests(**kwargs)

    def search(self):
        self.click(self.search_button)

    @staticmethod
    def _slug(txt: str) -> str:
        return re.sub(r"[^a-z0-9-]+", "", txt.lower().replace(" ", "-"))

    def validate_url_contains(self, expected: dict):
        url = urllib.parse.unquote(self.page.url.lower())

        if "location" in expected:
            exp = self._slug(expected["location"])
            m = re.search(r"/s/([\w~\-]+)/homes", url)
            assert m, f"can't extract location from {url!r}"

            seg = m.group(1)  # tel-aviv~yafo--israel
            if exp not in seg:
                # fuzzy fallback: match against each part split by ~ or --
                parts = re.split(r"[~\-]{2}|~", seg)  # ['tel-aviv', 'yafo', 'israel']
                assert any(
                    difflib.SequenceMatcher(None, exp, p).ratio() >= 0.8
                    for p in parts
                ), f"location '{exp}' not found in URL segment '{seg}'"

        for k, v in expected.items():
            if k == "location":
                continue
            val = self._slug(str(v))
            assert f"{k}={val}" in url, f"missing '{k}={val}' in URL: {url}"
