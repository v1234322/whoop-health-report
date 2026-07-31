import os
import requests
import json
from datetime import datetime, timedelta


TOKEN = os.environ["WHOOP_ACCESS_TOKEN"]

headers = {
    "Authorization": f"Bearer {TOKEN}"
}


HISTORY_FILE = "whoop_history.json"


def get_whoop(url):

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        return {}

    return r.json()



def extract_score(data):

    try:
        return data["records"][0]["score"]
    except:
        return {}



def load_history():

    if os.path.exists(HISTORY_FILE):
        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    return []



def save_history(history):

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            history[-7:],
            f,
            ensure_ascii=False,
            indent=2
        )



def trend_analysis(history):

    if len(history) < 2:
        return "数据不足，需要继续收集。"


    recovery = []
    strain = []
    hrv = []
    sleep = []


    for day in history:

        recovery.append(
            day.get("recovery",0)
        )

        strain.append(
            day.get("strain",0)
        )

        hrv.append(
            day.get("hrv",0)
        )

        sleep.append(
            day.get("sleep",0)
        )


    avg_recovery = sum(recovery)/len(recovery)
    avg_strain = sum(strain)/len(strain)
    avg_sleep = sum(sleep)/len(sleep)


    result = f"""

过去7天趋势：

恢复平均：
{avg_recovery:.1f}

睡眠平均：
{avg_sleep:.1f}

训练负荷平均：
{avg_strain:.1f}

"""


    if avg_recovery >= 70:
        result += "\n🟢 最近恢复状态良好"

    elif avg_recovery <40:
        result += "\n🔴 最近恢复不足，需要增加休息"

    else:
        result += "\n🟡 恢复状态稳定"


    return result



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


    recovery_score = extract_score(
        recovery_data
    )

    sleep_score = extract_score(
        sleep_data
    )

    cycle_score = extract_score(
        cycle_data
    )


    recovery = recovery_score.get(
        "recovery_score",
        0
    )

    hrv = recovery_score.get(
        "hrv_rmssd_milli",
        0
    )


    sleep = sleep_score.get(
        "sleep_performance_percentage",
        0
    )


    strain = cycle_score.get(
        "strain",
        0
    )


    history = load_history()


    history.append({

        "date": today,

        "recovery": recovery,

        "sleep": sleep,

        "strain": strain,

        "hrv": hrv

    })


    save_history(history)


    trend = trend_analysis(history)



    report = f"""
# 🟢 WHOOP 健康教练日报

日期：
{today}


## 今日数据

Recovery:
{recovery}

HRV:
{hrv}

Sleep:
{sleep}

Strain:
{strain}


---

# 📈 最近7天趋势

{trend}


---

# 今日建议

"""

    if recovery >=70:
        report += """
✅ 可以安排训练
✅ 适合力量训练或高质量运动
"""

    elif recovery <40:
        report += """
⚠️ 优先恢复
⚠️ 降低训练强度
"""

    else:
        report += """
🟡 保持中等训练
🟡 注意睡眠
"""


    with open(
        "WHOOP_Report.md",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(report)


    print(report)



if __name__=="__main__":
    main()
