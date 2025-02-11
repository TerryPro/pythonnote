# 环境配置指南

## 开发环境配置

### 1. 系统要求
- Python 3.8+
- pip 20.0+
- Git
- Redis 6.0+
- Node.js 14+ (用于前端开发)

### 2. Python环境配置

#### 2.1 创建虚拟环境
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/MacOS
python3 -m venv .venv
source .venv/bin/activate
```

#### 2.2 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 环境变量配置

创建 `.env` 文件：
```ini
# 应用配置
APP_NAME=数据分析助手
DEBUG=True
VERSION=1.0.0

# 安全配置
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI服务配置
DEEPSEEK_API_KEY=your-api-key
DEEPSEEK_CLIENT_TYPE=direct

# Redis配置
REDIS_URL=redis://localhost:6379/0
REDIS_POOL_SIZE=10

# 日志配置
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### 4. Redis配置

#### 4.1 Windows安装
1. 下载Redis for Windows
2. 运行redis-server.exe
3. 验证连接：
```bash
redis-cli ping
```

#### 4.2 Linux安装
```bash
# Ubuntu
sudo apt-get update
sudo apt-get install redis-server

# CentOS
sudo yum install redis
sudo systemctl start redis
```

### 5. 开发工具配置

#### 5.1 VSCode配置
推荐安装以下插件：
- Python
- Pylance
- Python Test Explorer
- Python Docstring Generator
- autoDocstring
- Black Formatter

settings.json配置：
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": [
        "--line-length",
        "120"
    ],
    "editor.formatOnSave": true,
    "editor.rulers": [120],
    "python.analysis.typeCheckingMode": "basic"
}
```

## 生产环境配置

### 1. 系统要求
- Linux服务器 (推荐Ubuntu 20.04 LTS)
- Python 3.8+
- Nginx
- Supervisor
- Redis

### 2. 安装系统依赖
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx supervisor redis-server
```

### 3. 应用部署

#### 3.1 克隆代码
```bash
git clone <repository-url>
cd <project-directory>
```

#### 3.2 配置虚拟环境
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 3.3 生产环境配置文件
创建 `.env.prod`：
```ini
# 应用配置
APP_NAME=数据分析助手
DEBUG=False
VERSION=1.0.0

# 安全配置
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI服务配置
DEEPSEEK_API_KEY=your-production-api-key
DEEPSEEK_CLIENT_TYPE=direct

# Redis配置
REDIS_URL=redis://localhost:6379/0
REDIS_POOL_SIZE=20

# 日志配置
LOG_LEVEL=WARNING
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### 4. Supervisor配置

创建 `/etc/supervisor/conf.d/data_analysis.conf`：
```ini
[program:data_analysis]
directory=/path/to/your/app
command=/path/to/your/app/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/data_analysis/err.log
stdout_logfile=/var/log/data_analysis/out.log
environment=
    PYTHONPATH="/path/to/your/app",
    ENV_FILE=".env.prod"
```

### 5. Nginx配置

创建 `/etc/nginx/sites-available/data_analysis`：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 6. 启动服务
```bash
# 重启Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart data_analysis

# 重启Nginx
sudo ln -s /etc/nginx/sites-available/data_analysis /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 监控配置

### 1. 日志监控
配置日志轮转 `/etc/logrotate.d/data_analysis`：
```
/var/log/data_analysis/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        supervisorctl restart data_analysis
    endscript
}
```

### 2. 性能监控
推荐使用以下工具：
- Prometheus
- Grafana
- StatsD

## 故障排查

### 1. 检查日志
```bash
# 应用日志
tail -f /var/log/data_analysis/out.log
tail -f /var/log/data_analysis/err.log

# Nginx日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 2. 检查服务状态
```bash
# 检查Supervisor状态
sudo supervisorctl status

# 检查Nginx状态
sudo systemctl status nginx

# 检查Redis状态
sudo systemctl status redis
``` 