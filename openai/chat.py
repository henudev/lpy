import openai
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置 OpenAI 客户端
print(f"API Key loaded: {os.getenv('OPENAI_API_KEY') is not None}")
print(f"Base URL: {os.getenv('OPENAI_BASE_URL')}")

openai.api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

def test_chat_completion():
    """
    测试 OpenAI Chat Completions API 的基本功能
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个 helpful assistant."},
                {"role": "user", "content": "你好，介绍一下你自己"}
            ],
            max_tokens=150,
            temperature=0.7
        )

        # 输出响应结果
        print("=== 基本对话测试 ===")
        print(f"模型: {response.model}")
        print(f"完成原因: {response.choices[0].finish_reason}")
        print(f"助手回复: {response.choices[0].message.content}")
        print(f"总token数: {response.usage.total_tokens}")
        print()

        return response

    except Exception as e:
        print(f"基本对话测试失败: {e}")
        return None

def test_streaming_response():
    """
    测试流式响应功能
    """
    try:
        print("=== 流式响应测试 ===")
        stream = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "给我讲一个关于编程的笑话"}
            ],
            stream=True,
            max_tokens=100
        )

        print("流式响应内容:")
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print("\n")

    except Exception as e:
        print(f"流式响应测试失败: {e}")

def test_function_calling():
    """
    测试函数调用功能
    """
    try:
        print("=== 函数调用测试 ===")
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "获取指定位置的当前天气",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "城市名，例如：北京"
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"]
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        ]

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "今天北京的天气怎么样？"}
            ],
            tools=tools,
            tool_choice="auto"
        )

        print(f"是否需要工具调用: {bool(response.choices[0].message.tool_calls)}")
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            print(f"工具名称: {tool_call.function.name}")
            print(f"参数: {tool_call.function.arguments}")
        else:
            print(f"直接回复: {response.choices[0].message.content}")
        print()

    except Exception as e:
        print(f"函数调用测试失败: {e}")

def main():
    """
    主测试函数
    """
    print("开始测试 OpenAI Chat Completions API...\n")

    # 测试基本对话功能
    test_chat_completion()

    # 测试流式响应
    test_streaming_response()

    # 测试函数调用
    test_function_calling()

    print("所有测试完成!")

if __name__ == "__main__":
    main()
