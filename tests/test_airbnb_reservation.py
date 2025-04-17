import pytest
from pages.airbnb_page import AirbnbPage
from pages.search_page import SearchPage


@pytest.mark.parametrize("location, check_in, check_out, guests", [
    ("Tel Aviv", "2025-06-10", "2025-06-15", {"adults": 2, "children": 1}),
])
def test_search_and_reserve_highest_rated(page, location, check_in, check_out, guests):
    """
    Test that searches for apartments and reserves the highest-rated listing.

    Steps:
    1. Navigate to Airbnb.
    2. Search apartments with given parameters.
    3. Validate URL parameters.
    4. Analyze results and pick the top-rated.
    5. Click on the top-rated listing.
    6. Save and print reservation details.
    7. Attempt reservation and validate again.
    """
    # Step 1-2: Navigate and search
    home_page = AirbnbPage(page)
    home_page.go_to_homepage()
    home_page.enter_location(location)
    home_page.select_dates(check_in, check_out)
    home_page.select_guests(**guests)
    home_page.search()

    # Step 3: Validate URL
    home_page.validate_url_contains({"location": location, **guests})

    # Step 4: Analyze search results
    search_page = SearchPage(page)
    top_rated_listing = search_page.get_top_rated_listing()
    assert top_rated_listing, "No top rated listing found"

    # Step 5: Click on the top rated listing
    search_page.click_listing_by_id(top_rated_listing['id'])

    # Step 6: Save reservation details
    reservation_details = search_page.get_reservation_details()
    print("\nReservation Details:")
    for key, value in reservation_details.items():
        print(f"  {key.capitalize()}: {value}")

    # Step 7: Attempt reservation
    search_page.reserve_and_validate(reservation_details, phone_number="+972-501234567")
