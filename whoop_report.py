import os
import requests
from datetime import datetime

WHOOP_TOKEN = os.environ["WHOOP_ACCESS_TOKEN"]

headers = {
    "Authorization": f"Bearer {WHOOP_TOKEN}"
}

def get_whoop_data():
    urls = {
        "recovery": "https://api.prod.whoop.com/developer/v2/recovery",
        "sleep": "https://api.prod.whoop.com/developer/v2/activity/sleep",
        "cycle": "https://api.prod.whoop.com/developer/v2/cycle"
    }

    result = {}

    for name, url in urls.items():
        response = requests.get(url, headers=headers)
        result[name] = response.json()

    return result


if __name__ == "__main__":
    data = get_whoop_data()

    print("WHOOP Daily Report")
    print(datetime.now())
    print(data)
