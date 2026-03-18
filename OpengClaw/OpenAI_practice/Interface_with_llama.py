import os
import logging
from openai import OpenAI
from openai import APIConnectionError, RateLimitError, APIStatusError

# ==========================================
# 1. 工业级日志配置 (绝不在生产环境使用单纯的 print)
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("WaterIndustrialAI_Agent")

class LocalLLMAgent:
    def __init__(self, model_name="llama3"):
        """
        初始化本地大模型代理
        """
        # ==========================================
        # 2. 配置分离：从环境变量读取配置，绝不将 URL 硬编码在代码中
        # ==========================================
        self.api_base = os.getenv("LLM_API_BASE", "http://localhost:11434/v1")
        # 本地开源模型通常不需要真实的 API Key，但为了格式兼容必须填入占位符
        self.api_key = os.getenv("LLM_API_KEY", "ollama_placeholder") 
        self.model_name = model_name
        
        # ==========================================
        # 3. 初始化客户端，无缝劫持 OpenAI 官方 SDK 指向本地 Linux 服务器
        # ==========================================
        self.client = OpenAI(
            base_url=self.api_base,
            api_key=self.api_key
        )
        logger.info(f"已初始化大模型代理: 模型={self.model_name}, 接口={self.api_base}")

    def analyze_sensor_data(self, sensor_payload):
        """
        核心业务逻辑：分析工业传感器数据并返回诊断建议
        """
        system_prompt = (
            "你是一个资深的智能水务算法工程师。你的任务是保障水务云服务系统的高效运行。"
            "请分析以下传感器数据，判断是否存在设备或水质异常，并给出排查建议。"
        )
        
        try:
            logger.info(f"正在向 {self.model_name} 发送传感器数据进行分析...")
            # .chat.completions.create(...)：按下通讯机的发送按钮，开始聊天生成
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"最新传感器JSON数据：\n{sensor_payload}"}
                ],
                # ==========================================
                # 4. 参数调优：工业场景下调低 temperature 以保证输出的确定性和严谨性
                # ==========================================
                temperature=0.1, 
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            logger.info("成功接收到大模型的诊断分析。")
            return result

        # ==========================================
        # 5. 细粒度异常处理：防止模型服务挂掉导致整个后端崩溃
        # ==========================================
        except APIConnectionError as e:
            logger.error(f"严重错误：大模型服务器连接失败。请检查本地 Ollama 或 vLLM 服务是否已启动: {e}")
        except RateLimitError as e:
            logger.warning(f"触发限流：并发请求过多，建议加入消息队列 (Message Queue): {e}")
        except APIStatusError as e:
            logger.error(f"API 状态错误：返回了错误的状态码 {e.status_code}: {e.response}")
        except Exception as e:
            logger.error(f"发生未知运行时错误: {e}")
            
        return None

# ==========================================
# 6. 模块测试入口
# ==========================================
if __name__ == "__main__":
    # 模拟从物联网设备网关接收到的真实业务数据
    mock_sensor_data = """
    {
        "device_id": "Pump_Station_A1", 
        "pH_level": 4.2, 
        "turbidity_NTU": 15.5, 
        "gpu_temperature_C": 85,
        "timestamp": "2026-03-12T20:10:00"
    }
    """
    
    # 实例化并调用
    water_agent = LocalLLMAgent(model_name="llama3")
    analysis_result = water_agent.analyze_sensor_data(mock_sensor_data)
    
    if analysis_result:
        print("\n=== AI 诊断输出 ===")
        print(analysis_result)
    else:
        print("\nAI 诊断服务当前不可用，已触发降级策略。")