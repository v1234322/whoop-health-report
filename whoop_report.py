import os
import requests
from datetime import datetime


TOKEN = os.environ["WHOOP_ACCESS_TOKEN"]

headers = {
    "Authorization": f"Bearer {TOKEN}"
}


def get_whoop(url):
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        return {
            "error": r.text,
            "status": r.status_code
        }

    return r.json()


def main():

    today = datetime.now().strftime("%Y-%m-%d")

    recovery = get_whoop(
        "https://api.prod.whoop.com/developer/v2/recovery"
    )

    sleep = get_whoop(
        "https://api.prod.whoop.com/developer/v2/activity/sleep"
    )

    cycle = get_whoop(
        "https://api.prod.whoop.com/developer/v2/cycle"
    )


    report = f"""
# WHOOP 今日健康报告

日期：{today}

---

## 恢复 Recovery

{recovery}

---

## 睡眠 Sleep

{sleep}

---

## 活动负荷 Strain

{cycle}

---

## 今日建议

根据 WHOOP 数据：

- 如果恢复较高：
  可以进行正常训练。

- 如果恢复偏低：
  建议降低训练强度，加强睡眠和恢复。

- 保持规律睡眠和补充水分。

---
自动生成时间：
{datetime.now()}
"""


    with open("WHOOP_Report.md", "w", encoding="utf-8") as f:
        f.write(report)


    print(report)


if __name__ == "__main__":
    main()
