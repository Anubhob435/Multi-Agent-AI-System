# agents/spacex_agent.py

import requests

def run(previous_data: dict) -> dict:
    """
    Fetches next SpaceX launch data.
    """
    url = "https://api.spacexdata.com/v4/launches/next"
    response = requests.get(url)
    data = response.json()

    launch_info = {
        "mission": data.get("name"),
        "date": data.get("date_utc"),
        "location": data.get("launchpad")  # we'll resolve this later
    }

    previous_data.update({"spacex": launch_info})
    return previous_data
