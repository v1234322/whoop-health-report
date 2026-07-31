import os
import requests
import json
from datetime import datetime


WHOOP_ACCESS_TOKEN = os.environ.get("WHOOP_ACCESS_TOKEN")

if not WHOOP_ACCESS_TOKEN:
    raise Exception("没有找到 WHOOP_ACCESS_TOKEN")


headers = {
    "Authorization": f"Bearer {WHOOP_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}


def get_data(name, url):
    response = requests.get(url, headers=headers)

    print("\n==========")
    print(name)
    print("状态码:", response.status_code)

    if response.status_code != 200:
        print(response.text)
        return None

    return response.json()


def main():

    print("WHOOP Daily Report")
    print(datetime.now())

    recovery = get_data(
        "Recovery",
        "https://api.prod.whoop.com/developer/v2/recovery"
    )

    sleep = get_data(
        "Sleep",
        "https://api.prod.whoop.com/developer/v2/activity/sleep"
    )

    cycle = get_data(
        "Cycle",
        "https://api.prod.whoop.com/developer/v2/cycle"
    )


    report = {
        "time": str(datetime.now()),
        "recovery": recovery,
        "sleep": sleep,
        "cycle": cycle
    }


    print("\n===== WHOOP DATA =====")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
