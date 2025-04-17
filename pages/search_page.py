from pages.base_page import BasePage
from playwright.sync_api import Page

class SearchPage(BasePage):
    def __init__(self, page: Page):
        """
        Initializes the SearchPage with Playwright page instance.
        """
        super().__init__(page)
        self.results_root = page.locator('[data-testid="search-results"]')
        self.listings = page.locator('[data-testid="listing-card"]')
        self.reserve_button = page.locator('[data-testid="request-to-book-button"]')
        self.phone_input = page.locator('input[name="phone"]')

    def select_highest_rated_listing(self):
        """
        Selects the highest-rated listing from the search results and clicks on it.
        """
        self.listings.first.wait_for(state="visible", timeout=10000)
        self.listings.first.click()

    def save_reservation_details(self) -> dict:
        """
        Saves the reservation card details displayed on the right side.
        Returns: dict: A dictionary containing the reservation details.
        """
        details = {}
        # Example selectors - need to adjust based on real page
        details['title'] = self.page.locator('[data-testid="title"]').inner_text()
        details['price'] = self.page.locator('[data-testid="price-summary"]').inner_text()
        return details

    def click_reserve(self):
        """
        Clicks the 'Reserve' button.
        """
        self.reserve_button.wait_for(state="visible", timeout=5000)
        self.reserve_button.click()

    def validate_reservation_details(self, expected: dict):
        """
        Validates that the reservation details match the previously saved details.
        Args: expected (dict): The expected reservation details to validate against.
        """
        title = self.page.locator('[data-testid="title"]').inner_text()
        price = self.page.locator('[data-testid="price-summary"]').inner_text()
        assert title == expected['title'], f"Title mismatch: {title} != {expected['title']}"
        assert price == expected['price'], f"Price mismatch: {price} != {expected['price']}"

    def enter_phone_number(self, phone_number: str):
        """
        Enters the provided phone number into the reservation form.
        Args: phone_number (str): The phone number to input.
        """
        self.phone_input.wait_for(state="visible", timeout=5000)
        self.fill(self.phone_input, phone_number)
