import requests
import json
from playwright.sync_api import Page

class AirbnbResultsAnalyzer:
    def __init__(self, page: Page):
        """
        Initializes the AirbnbResultsAnalyzer with a Playwright page instance.
        Args: page (Page): Playwright Page object for intercepting network requests.
        """
        self.page = page
        self.api_data = []
        self._requests = []

    def start_capture_api_request(self):
        """
        Starts listening for the Airbnb 'StaysSearch' POST requests
        so that their payload and headers can later be reused to fetch data.
        """
        def capture_request(request):
            if "StaysSearch" in request.url and request.method == "POST":
                self._requests.append({
                    "url": request.url,
                    "headers": dict(request.headers),
                    "post_data": request.post_data
                })

        self.page.on("request", capture_request)
        self.page.on("requestfinished", capture_request)

    def fetch_api_results(self):
        """
        Sends a POST request based on the captured StaysSearch data
        to retrieve Airbnb search results from the backend API.
        """
        for req in self._requests:
            try:
                headers = {**req["headers"], "User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
                body = json.loads(req["post_data"])
                res = requests.post(req["url"], json=body, headers=headers)
                if res.status_code != 200:
                    continue

                data = res.json().get("data", {}).get("presentation", {}).get("staysSearch", {})
                self.api_data = (
                    data.get("sections", [{}])[0].get("items") or
                    data.get("results", {}).get("searchResults")
                ) or []
                return
            except Exception:
                continue

    def _extract(self, item):
        """
        Extracts relevant fields (ID, name, description, price, rating, and URL suffix) from a listing item.
        Args: item (dict): Raw listing dictionary from Airbnb API response.
        Returns: dict: Simplified dictionary containing listing details.
        """
        listing = item.get("listing", item)
        demand = item.get("demandStayListing", listing.get("demandStayListing", {}))

        id_ = demand.get("id")
        name = listing.get("title") or item.get("title") or "Unnamed Listing"
        description = demand.get("description", {}).get("name", {}).get("localizedStringWithTranslationPreference", "")
        price_str = item.get("structuredDisplayPrice", {}).get("primaryLine", {}).get("discountedPrice") or ""
        rating_str = item.get("avgRatingLocalized") or item.get("avgRatingA11yLabel")

        return {
            "id": id_,
            "name": name,
            "description": description,
            "price": float(price_str.replace("₪", "").replace(",", "")) if price_str else None,
            "rating": float(rating_str.split("(")[0]) if rating_str and "(" in rating_str else None
        }

    def get_cheapest_from_api(self):
        """
        Finds the listing with the lowest price from the search results.
        Returns: dict or None: Listing with the lowest price or None if not available.
        """
        return min(
            (self._extract(item) for item in self.api_data if self._extract(item)["price"] is not None),
            key=lambda x: x["price"],
            default=None
        )

    def get_top_rated_from_api(self):
        """
        Finds the highest-rated listing from the search results that also has a price.
        Returns: dict or None: Listing with the highest rating and a price, or None if not available.
        """
        return max(
            (
                self._extract(item)
                for item in self.api_data
                if self._extract(item)["rating"] is not None and self._extract(item)["price"] is not None
            ),
            key=lambda x: x["rating"],
            default=None
        )
