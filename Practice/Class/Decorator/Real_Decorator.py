import time
import functools

def retry_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        attempts = 3  # 设置最大重试次数
        
        for i in range(attempts):
            # wrapper 里的 try: 就像是在面前竖起了一面防爆盾。它在监控 func(*args, **kwargs) 这一行。
            try:
                # 尝试执行原函数
                print(f"🔄 [第 {i+1} 次尝试] 正在执行: {func.__name__}...")
                result = func(*args, **kwargs) # 如果 func(*args) 里面 raise 了一个错误，Python 解释器会说：“停！出事了！” 它会跳过 func 后面所有的代码，也会跳过 wrapper 中 try 块里剩下的代码（也就是跳过那个 print("✅ ...") 和 return result）。 它会直接瞬移到 except 块里
                
                # 如果成功，直接返回结果，结束循环
                print("✅ 执行成功！")
                return result
            
            # 这里的变量 e，就是你在原函数里 raise 出来的那个 ConnectionError("网络断开") 对象！
            except Exception as e:
                # 如果报错，不要立刻崩溃，而是打印错误并重试
                print(f"❌ 第 {i+1} 次失败: {e}")
                if i < attempts - 1: # 如果不是最后一次，就休息一下再试
                    print(i)
                    time.sleep(1)
                else:
                    # 如果试了3次还是不行，那就真的抛出异常
                    print("🚫 彻底失败，停止重试。")
                    raise e
                    
    return wrapper

# --- 实战测试 ---

@retry_decorator
def connect_to_server(status):
    """模拟连接服务器，如果 status 是 'bad' 就报错"""
    if status == 'bad':
        raise ConnectionError("网络断开")
    return "连接成功数据包"

# 1. 测试自动重试（会失败3次然后报错）
try:
    connect_to_server("bad")
except Exception:
    print("--- 捕获到最终异常 ---\n")

# 2. 测试成功情况
#print(connect_to_server("good"))