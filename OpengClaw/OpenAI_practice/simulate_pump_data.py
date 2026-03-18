from openai import OpenAI
import json

# 1. 建立脑机连接（直接越过框架，连接底层的本地 Qwen 大脑）
client = OpenAI(
    base_url="http://172.27.0.1:11434/v1", 
    api_key="ollama_local"  # 本地部署无需真实密码
)

# 2. 编写下发给 AI 的工业指令
system_prompt = """
你现在是水务智能算法助手。请直接输出一段 Python 代码，不要有任何多余的解释文字。
任务要求：使用 random 库，模拟生成【三号泵站】过去 24 小时的水压（正常范围 0.3-0.5 MPa）和水温数据，并故意制造一个水压低于 0.2 MPa 的异常点。
"""

print("正在向边缘计算节点发送指令，请稍候...")

# 3. 发送请求并获取 AI 生成的代码
response = client.chat.completions.create(
    model="qwen2.5:1.5b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "请开始编写三号泵站的模拟代码。"}
    ],
    temperature=0.1 # 降低温度，让 AI 输出更严谨的代码
)

# 4. 打印出大模型的思考结果
ai_generated_code = response.choices[0].message.content
print("\n========== AI 自动生成的工业代码 ==========\n")
print(ai_generated_code)
print("\n===========================================")