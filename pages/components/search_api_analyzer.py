import requests
from playwright.sync_api import Page

class AirbnbResultsAnalyzer:
    def __init__(self, page: Page):
        self.page = page
        self.api_data = []
        self._captured = {}

    def start_capture_api_request(self):
        """
        Start listening to the ExploreTabs API request before triggering the search.
        """
        def handle_request(request):
            if "ExploreTabs" in request.url and request.method == "POST":
                self._captured["url"] = request.url
                self._captured["headers"] = dict(request.headers)
                self._captured["post_data"] = request.post_data

        self.page.on("request", handle_request)

    def fetch_api_results(self):
        """
        Fetch all paginated results from the captured ExploreTabs API request.
        """
        if "url" not in self._captured:
            raise ValueError("❌ Failed to capture API request. Make sure a search was performed.")

        headers = self._captured["headers"].copy()
        headers.update({
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json"
        })

        all_items = []
        offset = 0

        while True:
            # Update offset in request body
            body = requests.utils.json.loads(self._captured["post_data"])
            body["items_offset"] = offset

            response = requests.post(
                self._captured["url"],
                json=body,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()

            listings = data.get("explore_tabs", [{}])[0].get("sections", [{}])[0].get("listings", [])
            if not listings:
                break

            all_items.extend(listings)
            offset += len(listings)

        self.api_data = all_items

    def get_cheapest_from_api(self):
        cheapest = None
        for item in self.api_data:
            try:
                price = item["pricingQuote"]["rate"]["amount"]
                name = item["listing"].get("name", "")
                if not cheapest or price < cheapest["price"]:
                    cheapest = {"name": name, "price": price}
            except:
                continue
        return cheapest

    def get_top_rated_from_api(self):
        top = None
        for item in self.api_data:
            try:
                rating = item["listing"].get("avgRating", 0)
                name = item["listing"].get("name", "")
                if not top or rating > top["rating"]:
                    top = {"name": name, "rating": rating}
            except:
                continue
        return top
