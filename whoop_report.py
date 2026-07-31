import os
import requests
from datetime import datetime


TOKEN = os.environ["WHOOP_ACCESS_TOKEN"]

headers = {
    "Authorization": f"Bearer {TOKEN}"
}


def get_whoop(url):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {}

    return response.json()


def get_score(data):
    try:
        return data["records"][0]["score"]
    except:
        return {}


def analyze(recovery, sleep, cycle):

    advice = []

    # Recovery
    recovery_score = recovery.get("score", {}).get("recovery_score")

    if recovery_score:
        if recovery_score >= 70:
            status = "🟢 身体状态良好，适合训练"
            advice.append("今天可以进行力量训练或中高强度训练。")
        elif recovery_score >= 40:
            status = "🟡 身体状态一般，建议控制强度"
            advice.append("建议进行中等强度训练或 Zone 2 有氧。")
        else:
            status = "🔴 身体需要恢复"
            advice.append("建议休息、散步、拉伸，避免高强度训练。")
    else:
        status = "⚪ 暂无恢复评分"


    # Sleep
    sleep_score = sleep.get("score", {}).get("sleep_performance_percentage")

    if sleep_score:
        if sleep_score < 70:
            advice.append("睡眠不足，今晚建议提前30-60分钟睡觉。")
        else:
            advice.append("睡眠表现不错，继续保持规律作息。")


    # Strain
    strain = cycle.get("score", {}).get("strain")

    if strain:
        if strain > 16:
            advice.append("昨日负荷较高，今天注意恢复。")
        elif strain < 8:
            advice.append("昨日活动较少，可以适当增加运动。")
        else:
            advice.append("昨日活动量适中。")


    return status, advice



def main():

    today = datetime.now().strftime("%Y-%m-%d")


    recovery_data = get_whoop(
        "https://api.prod.whoop.com/developer/v2/recovery"
    )

    sleep_data = get_whoop(
        "https://api.prod.whoop.com/developer/v2/activity/sleep"
    )

    cycle_data = get_whoop(
        "https://api.prod.whoop.com/developer/v2/cycle"
    )


    recovery = get_score(recovery_data)
    sleep = get_score(sleep_data)
    cycle = get_score(cycle_data)


    status, advice = analyze(
        recovery,
        sleep,
        cycle
    )


    report = f"""
# 🟢 WHOOP 健康教练日报

日期：
{today}

---

## 今日状态

{status}

---

## 身体数据

### Recovery
{recovery}

### Sleep
{sleep}

### Strain
{cycle}

---

## 今日建议

"""

    for item in advice:
        report += f"- {item}\n"


    report += """

---

## 健康习惯建议

✅ 保持充足饮水  
✅ 早餐补充蛋白质  
✅ 下午减少咖啡因  
✅ 保持固定睡眠时间

---

自动生成：
""" + str(datetime.now())


    with open(
        "WHOOP_Report.md",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(report)


    print(report)



if __name__ == "__main__":
    main()
