from utils.date_utils import validate_date_logic
from pages.airbnb_page import AirbnbPage
from pages.components.search_api_analyzer import AirbnbResultsAnalyzer
import pytest

def log_listing(listing: dict, title: str):
    """
    Print listing details in a readable format.
    """
    if listing:
        print(f"\n{title}:")
        print(f"  - ID: {listing.get('id')}")
        print(f"  - Name: {listing.get('name')}")
        print(f"  - Description: {listing.get('description')}")
        print(f"  - Price: {listing.get('price')}")
        print(f"  - Rating: {listing.get('rating')}")
    else:
        print(f"\n{title}: No apartments found.")


@pytest.mark.parametrize("location, check_in, check_out, guests", [
    ("Haifa", "2025-04-17", "2025-04-20", {"adults": 2})
])
def test_airbnb_search_and_analyze(page, location, check_in, check_out, guests):
    # Arrange
    airbnb = AirbnbPage(page)
    airbnb.go_to_homepage()

    airbnb.enter_location(location)
    validate_date_logic(check_in, check_out)
    airbnb.select_dates(check_in, check_out)
    airbnb.select_guests(**guests)

    analyzer = AirbnbResultsAnalyzer(page)
    analyzer.start_capture_api_request()

    # Act
    airbnb.search()
    page.wait_for_url(lambda url: "s=" in url)
    page.wait_for_selector('[itemprop="itemListElement"]', timeout=7000)

    # Assert:
    # Validate URL parameters
    airbnb.validate_url_contains({
        "location": location,
        "checkin": check_in,
        "checkout": check_out,
        **guests
    })

    analyzer.fetch_api_results()
    # Get the cheapest and top-rated listings
    cheapest = analyzer.get_cheapest_from_api()
    top_rated = analyzer.get_top_rated_from_api()

    # Log the details
    log_listing(cheapest, "Cheapest Apartment")
    log_listing(top_rated, "Top Rated Apartment")

    # Validate that both results were found
    assert cheapest is not None, "No cheapest Apartment found."
    assert top_rated is not None, "No top-rated Apartment found."
