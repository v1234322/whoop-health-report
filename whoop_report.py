import os
import requests
import json
from datetime import datetime
from openai import OpenAI


WHOOP_TOKEN = os.environ["WHOOP_ACCESS_TOKEN"]
OPENAI_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_KEY)

headers = {
    "Authorization": f"Bearer {WHOOP_TOKEN}"
}


def get_whoop(url):
    r = requests.get(url, headers=headers)
    return r.json()


def main():

    recovery = get_whoop(
        "https://api.prod.whoop.com/developer/v2/recovery"
    )

    sleep = get_whoop(
        "https://api.prod.whoop.com/developer/v2/activity/sleep"
    )

    cycle = get_whoop(
        "https://api.prod.whoop.com/developer/v2/cycle"
    )


    data = {
        "recovery": recovery,
        "sleep": sleep,
        "cycle": cycle
    }


    prompt = f"""
你是WHOOP健康教练。

根据以下数据生成今天健康报告：

{json.dumps(data)}

输出：
1. 今日恢复评分分析
2. 睡眠分析
3. 训练建议
4. 饮食建议
5. 晚间恢复建议

用中文回答。
"""


    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    report = response.choices[0].message.content

    print("===== WHOOP 今日健康报告 =====")
    print(report)


if __name__ == "__main__":
    main()
