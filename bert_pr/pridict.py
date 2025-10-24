import torch
from transformers import BertTokenizer, BertForSequenceClassification
import joblib
import os

# ------------------------
# 1. 加载模型和标签编码
# ------------------------
model_path = "./model"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"{model_path} 不存在，请先训练模型")

tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
label_encoder = joblib.load(os.path.join(model_path, "label_encoder.pkl"))

# ------------------------
# 2. 推理函数
# ------------------------
def predict(text):
    # 编码文本
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=64
    )
    # 模型预测
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
        pred = torch.argmax(outputs.logits, dim=1).item()
    # 返回类别字符串
    return label_encoder.inverse_transform([pred])[0]

# ------------------------
# 3. 测试示例
# ------------------------
if __name__ == "__main__":
    test_texts = [
        "帮我查下今天的天气",
        "订一张去上海的机票",
        "今天上证指数涨了多少",
        "明天会下雨吗",
        "我要去北京出差订酒店"
    ]

    for text in test_texts:
        label = predict(text)
        print(f"问题: {text} => 分类: {label}")