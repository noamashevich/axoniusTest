from pages.airbnb_page import AirbnbPage


def test_airbnb_search(page):
    airbnb = AirbnbPage(page)
    airbnb.go_to_homepage()
    airbnb.enter_location("Tel Aviv")
    airbnb.select_dates("2025-04-17", "2025-04-20")
    airbnb.search()
    page.wait_for_url(lambda url: "s=" in url)
    print(dir(airbnb))
    assert "Tel-Aviv" in page.url or "search" in page.url