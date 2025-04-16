import requests

url = "https://www.airbnb.com/api/v3/ExploreTabs"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "x-airbnb-api-key": "your-api-key-if-needed"  # רק אם נדרש
}

payload = {
    "checkin": "2025-05-01",
    "checkout": "2025-05-04",
    "adults": 2,
    "children": 1,
    "infants": 0,
    "pets": 0,
    "placeId": "ChIJH3w7GaZMHRURkD-WwKJy-8E",
    "search_type": "filter_change",
    "tab_id": "home_tab"
}
if __name__ == '__main__':

    response = requests.post(url, json=payload, headers=headers)
    print(response.status_code)
    print(response.text)
