import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.preprocessing import LabelEncoder
from datasets import Dataset
import joblib
import os

def main():
    # ------------------------
    # 1. 加载数据
    # ------------------------
    data_path = "data_10000.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"{data_path} 不存在，请先准备数据文件")
    data = pd.read_csv(data_path)

    # ------------------------
    # 2. 标签编码
    # ------------------------
    label_encoder = LabelEncoder()
    data["label_id"] = label_encoder.fit_transform(data["label"])

    # ------------------------
    # 3. 删除原字符串列，保留整数标签
    # ------------------------
    data = data.drop(columns=["label"])
    data = data.rename(columns={"label_id": "label"})

    # ------------------------
    # 4. 构建 Dataset
    # ------------------------
    dataset = Dataset.from_pandas(data, preserve_index=False)

    # ------------------------
    # 5. 加载分词器
    # ------------------------
    tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")

    # ------------------------
    # 6. 数据编码函数
    # ------------------------
    def tokenize_function(examples):
        tokenized = tokenizer(
            examples["text"], padding="max_length", truncation=True, max_length=64
        )
        tokenized["labels"] = examples["label"]  # 确保 labels 为整数
        return tokenized

    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    # ------------------------
    # 7. 划分训练/验证集
    # ------------------------
    tokenized_dataset = tokenized_dataset.train_test_split(test_size=0.25)

    # ------------------------
    # 8. 加载模型
    # ------------------------
    num_labels = len(label_encoder.classes_)
    model = BertForSequenceClassification.from_pretrained(
        "bert-base-chinese", num_labels=num_labels
    )

    # ------------------------
    # 9. 训练参数
    # ------------------------
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_dir="./logs",
        load_best_model_at_end=True
    )

    # ------------------------
    # 10. 定义 Trainer
    # ------------------------
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["test"],
    )

    # ------------------------
    # 11. 开始训练
    # ------------------------
    print("🚀 开始训练...")
    trainer.train()

    # ------------------------
    # 12. 保存模型和标签编码
    # ------------------------
    os.makedirs("./model", exist_ok=True)
    model.save_pretrained("./model")
    tokenizer.save_pretrained("./model")
    joblib.dump(label_encoder, "./model/label_encoder.pkl")

    print("✅ 训练完成，模型已保存到 ./model 目录")

if __name__ == "__main__":
    main()