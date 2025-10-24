import random
import pandas as pd

def generate_dataset(num_samples=10000, output_file="data_10000.csv"):
    # ------------------------
    # 类别和模板
    # ------------------------
    categories = {
        "weather": [
            "今天{}怎么样",
            "明天天气会{}吗",
            "帮我查一下{}的天气",
            "{}会下雨吗",
            "{}气温多少度",
            "请告诉我{}的天气情况"
        ],
        "travel": [
            "订一张从{}到{}的机票",
            "帮我查{}到{}的火车票",
            "我想去{}旅游，订酒店",
            "安排一趟{}到{}的出差行程",
            "请帮我查{}的航班"
        ],
        "stock": [
            "{}今天涨了多少",
            "上证指数现在是多少",
            "{}股票行情怎么样",
            "帮我查一下{}的股价",
            "{}指数今日走势如何"
        ]
    }

    locations = ["北京", "上海", "广州", "深圳", "杭州", "南京", "天津", "重庆", "成都", "西安"]
    weathers = ["晴", "雨", "雪", "阴", "多云", "雾"]
    stocks = ["上证指数", "深证成指", "贵州茅台", "阿里巴巴", "腾讯控股", "比亚迪"]

    # ------------------------
    # 生成数据
    # ------------------------
    data = []
    for _ in range(num_samples):
        category = random.choice(list(categories.keys()))
        template = random.choice(categories[category])

        if category == "weather":
            loc = random.choice(locations)
            weather = random.choice(weathers)
            # 根据模板填充
            text = template.format(loc if "{}" in template else weather)
        elif category == "travel":
            loc1, loc2 = random.sample(locations, 2)
            text = template.format(loc1, loc2)
        else:  # stock
            stock = random.choice(stocks)
            text = template.format(stock)

        data.append({"text": text, "label": category})

    # ------------------------
    # 保存 CSV
    # ------------------------
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"✅ 已生成 {output_file}，包含 {num_samples} 条样本")

# ------------------------
# main 函数
# ------------------------
def main():
    generate_dataset(num_samples=10000, output_file="data_10000.csv")

if __name__ == "__main__":
    main()