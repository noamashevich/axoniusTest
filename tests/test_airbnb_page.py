from utils.date_utils import validate_date_logic

from pages.airbnb_page import AirbnbPage
from pages.components.search_api_analyzer import AirbnbResultsAnalyzer


def test_airbnb_search_and_analyze(page):
    # Arrange
    airbnb = AirbnbPage(page)
    airbnb.go_to_homepage()
    airbnb.enter_location("Tel Aviv")
    check_in = "2025-04-17"
    check_out = "2025-04-20"
    validate_date_logic(check_in, check_out)

    # Act
    airbnb.select_dates(check_in, check_out)
    airbnb.select_guests(adults=2)
    airbnb.search()
    page.wait_for_url(lambda url: "s=" in url)
    page.wait_for_selector('[itemprop="itemListElement"]', timeout=5000)

    # Assert
    airbnb.validate_url_contains({
        "location": "Tel Aviv",
        "checkin": check_in,
        "checkout": check_out,
        "adults": 2
     })

    # # ⏳ מחכים שהעמוד ייטען + ה־API ייקלט
    # page.wait_for_url(lambda url: "s=" in url)
    # page.wait_for_timeout(5000)


    # 📥 שליפת כל התוצאות מה-API
    # analyzer.fetch_api_results()

    # 🎯 תוצאות
    # print("💸 Cheapest:", analyzer.get_cheapest_from_api())
    # print("🏆 Top Rated:", analyzer.get_top_rated_from_api())
    #
