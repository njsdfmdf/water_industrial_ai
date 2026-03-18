from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

# 1. 实例化 FastAPI 应用（这就是你的网络服务主体）
app = FastAPI(title="北控水务 AI 算法中台 API", version="1.0")

# 2. 配置本地大模型连接
client = OpenAI(
    base_url="http://172.27.0.1:11434/v1", 
    api_key="ollama_local"
)

# 3. 定义前端传过来的数据格式（用 Pydantic 规范化）
class PumpRequest(BaseModel):
    pump_name: str
    target_pressure: float

# 4. 核心：写一个接口！
# @app.post 意思是这个网址接收 POST 方法的请求。"/generate_code" 是接口的具体路径
@app.post("/generate_code")
async def generate_pump_code(request: PumpRequest):
    # 将前端传来的设备名，动态塞进提示词里
    system_prompt = f"""
    你现在是水务智能算法助手。请直接输出 Python 代码，不要解释文字。
    任务要求：使用 random 库，模拟生成【{request.pump_name}】过去 24 小时的水压数据，
    并故意制造一个水压低于 {request.target_pressure} MPa 的异常点。
    """
    
    # 呼叫大模型
    response = client.chat.completions.create(
        model="qwen2.5:1.5b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "请开始编写模拟代码。"}
        ],
        temperature=0.1
    )
    
    # 将结果作为 JSON 返回给前端
    return {
        "status": "success",
        "device": request.pump_name,
        "ai_code": response.choices[0].message.content
    }