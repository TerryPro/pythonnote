import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def run_frontend():
    os.chdir("frontend")
    subprocess.run(["npm", "run", "serve"], check=True)

def run_backend():
    os.chdir("backend")
    subprocess.run([sys.executable, "main.py"], check=True)

def main():
    # 确保必要的目录存在
    if not os.path.exists("frontend"):
        print("Error: frontend directory not found")
        return
    if not os.path.exists("backend"):
        print("Error: backend directory not found")
        return
        
    print("启动 Python 交互式编程环境...")
    
    # 启动后端服务
    backend_thread = Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # 等待后端服务启动
    time.sleep(2)
    
    # 启动前端服务
    frontend_thread = Thread(target=run_frontend)
    frontend_thread.daemon = True
    frontend_thread.start()
    
    # 等待前端服务启动
    time.sleep(5)
    
    # 打开浏览器
    webbrowser.open("http://localhost:8080")
    
    try:
        # 保持主线程运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在关闭服务...")
        sys.exit(0)

if __name__ == "__main__":
    main() 