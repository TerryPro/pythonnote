from pydantic import BaseSettings, Field
from pathlib import Path
from typing import List
import os

class Settings(BaseSettings):
    """
    应用程序配置类
    使用Pydantic的BaseSettings管理所有配置项
    支持从环境变量加载配置
    """
    # API标题
    API_TITLE: str = "数据分析助手API"
    
    # 基础路径配置
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    EXPORT_DIR: Path = BASE_DIR / "export"
    NOTEBOOKS_DIR: Path = BASE_DIR / "notebooks"    # 笔记本存储目录
    NOTEDATAS_DIR: Path = BASE_DIR / "notedatas"
    DATA_DIR: Path = BASE_DIR / "data"              # 数据文件存储目录
    TEMP_DIR: Path = BASE_DIR / "temp"              # 临时文件目录
    LOGS_DIR: Path = BASE_DIR / "logs"              # 日志文件目录
    EXAMPLES_DIR: Path = BASE_DIR / "examples"      # 代码示例存储目录
    CONFIG_DIR: Path = BASE_DIR / "config"          # 系统，用户提示词存储目录
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # AI配置
    DEEPSEEK_CLIENT_TYPE: str = Field(default="siliconflow", env="DEEPSEEK_CLIENT_TYPE")
    
    DEEPSEEK_API_KEY: str = Field(default="", env="DEEPSEEK_API_KEY")
    DEEPSEEK_API_BASE: str = Field(default="https://api.deepseek.com/v1", env="DEEPSEEK_API_BASE")
    DEEPSEEK_MODEL: str = Field(default="Pro/deepseek-ai/DeepSeek-V3", env="DEEPSEEK_MODEL")

    SILICONFLOW_API_KEY: str = Field(default="", env="SILICONFLOW_API_KEY")
    SILICONFLOW_API_BASE: str = Field(default="https://api.siliconflow.com/v1", env="SILICONFLOW_API_BASE")
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        """Pydantic配置类"""
        case_sensitive = True
        env_file = ".env"
        
    def setup_directories(self):
        """
        创建必要的目录
        """
        self.EXPORT_DIR.mkdir(exist_ok=True)
        self.NOTEBOOKS_DIR.mkdir(exist_ok=True)
        self.DATA_DIR.mkdir(exist_ok=True)
        self.TEMP_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)  # 创建日志目录
        self.EXAMPLES_DIR.mkdir(exist_ok=True)  # 创建示例目录
        
    @property
    def cors_settings(self):
        """
        获取CORS配置
        """
        return {
            "allow_origins": self.CORS_ORIGINS,
            "allow_credentials": self.CORS_ALLOW_CREDENTIALS,
            "allow_methods": self.CORS_ALLOW_METHODS,
            "allow_headers": self.CORS_ALLOW_HEADERS,
        }

# 创建全局配置实例
settings = Settings() 