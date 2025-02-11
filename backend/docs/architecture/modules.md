# 模块设计文档

## 1. 模块概览

### 1.1 核心模块关系图
```
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
|   API模块      |<--->|   业务模块     |<--->|   基础模块     |
|                |     |                |     |                |
+----------------+     +----------------+     +----------------+
        |                     |                     |
        v                     v                     v
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
|   工具模块     |<--->|   服务模块     |<--->|   配置模块     |
|                |     |                |     |                |
+----------------+     +----------------+     +----------------+
```

## 2. 模块详细设计

### 2.1 API模块 (`routes/`)
负责处理HTTP请求和响应，实现RESTful API接口。

#### 2.1.1 数据处理API (`data_routes.py`)
```python
@router.get("/api/dataframes/list")
async def get_dataframes() -> List[str]:
    """获取所有可用的DataFrame列表"""
    pass

@router.get("/api/dataframes/info/{name}")
async def get_dataframe_info(name: str) -> Dict[str, Any]:
    """获取指定DataFrame的详细信息"""
    pass

@router.post("/api/dataframes/{name}/save")
async def save_dataframe(name: str, request: SaveDataFrameRequest):
    """保存DataFrame到文件"""
    pass
```

#### 2.1.2 AI服务API (`ai_routes.py`)
```python
@router.post("/api/ai/generate_code")
async def generate_code(request: GenerateCodeRequest):
    """生成Python代码"""
    pass

@router.get("/api/ai/system-prompts")
async def get_system_prompts():
    """获取系统提示词配置"""
    pass
```

### 2.2 业务模块 (`services/`)
实现核心业务逻辑，处理数据分析和AI代码生成。

#### 2.2.1 数据处理服务 (`data_service.py`)
```python
class DataService:
    """数据处理服务"""
    
    async def load_data(self, file_path: str) -> pd.DataFrame:
        """加载数据文件"""
        pass
        
    async def process_data(self, df: pd.DataFrame, operations: List[Dict]) -> pd.DataFrame:
        """处理数据"""
        pass
        
    async def export_data(self, df: pd.DataFrame, format: str) -> str:
        """导出数据"""
        pass
```

#### 2.2.2 AI服务 (`ai_service.py`)
```python
class AIService:
    """AI服务"""
    
    async def generate_code(self, prompt: str, context: Dict) -> str:
        """生成代码"""
        pass
        
    async def validate_code(self, code: str) -> bool:
        """验证代码安全性"""
        pass
```

### 2.3 基础模块 (`core/`)
提供基础功能和工具类。

#### 2.3.1 数据模型 (`models.py`)
```python
class DataFrameInfo(BaseModel):
    """DataFrame信息模型"""
    name: str
    shape: Tuple[int, int]
    columns: List[str]
    dtypes: Dict[str, str]

class CodeGenerationRequest(BaseModel):
    """代码生成请求模型"""
    prompt: str
    context: Optional[Dict] = None
    dataframe_name: Optional[str] = None
```

#### 2.3.2 异常处理 (`exceptions.py`)
```python
class AppException(Exception):
    """应用基础异常类"""
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code

class DataFrameNotFoundError(AppException):
    """DataFrame不存在异常"""
    pass
```

### 2.4 工具模块 (`utils/`)
提供通用工具函数和辅助类。

#### 2.4.1 日志工具 (`logger.py`)
```python
class Logger:
    """日志管理器"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        
    def setup(self):
        """配置日志"""
        pass
        
    def log_request(self, request: Request):
        """记录请求日志"""
        pass
```

#### 2.4.2 缓存工具 (`cache.py`)
```python
class CacheManager:
    """缓存管理器"""
    
    async def get(self, key: str) -> Any:
        """获取缓存"""
        pass
        
    async def set(self, key: str, value: Any, expire: int = 300):
        """设置缓存"""
        pass
```

### 2.5 服务模块 (`services/`)
实现外部服务集成。

#### 2.5.1 DeepSeek服务 (`deepseek_service.py`)
```python
class DeepSeekService:
    """DeepSeek API服务"""
    
    async def generate(self, prompt: str) -> str:
        """生成代码"""
        pass
        
    async def validate(self, code: str) -> bool:
        """验证代码"""
        pass
```

#### 2.5.2 数据存储服务 (`storage_service.py`)
```python
class StorageService:
    """存储服务"""
    
    async def save_file(self, file: UploadFile) -> str:
        """保存上传文件"""
        pass
        
    async def load_file(self, path: str) -> bytes:
        """加载文件"""
        pass
```

### 2.6 配置模块 (`config/`)
管理应用配置和环境变量。

#### 2.6.1 应用配置 (`config.py`)
```python
class Settings(BaseSettings):
    """应用配置类"""
    
    APP_NAME: str = "数据分析助手"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
```

#### 2.6.2 常量配置 (`constants.py`)
```python
class Constants:
    """常量定义"""
    
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".json"}
    CACHE_EXPIRE_TIME = 300  # 5分钟
```

## 3. 模块依赖关系

### 3.1 依赖图
```
API模块 -> 业务模块 -> 基础模块
   |          |          |
   v          v          v
工具模块 <- 服务模块 <- 配置模块
```

### 3.2 依赖规则
1. 上层模块可以依赖下层模块
2. 同层模块可以相互依赖
3. 下层模块不能依赖上层模块
4. 避免循环依赖

## 4. 模块扩展性

### 4.1 扩展点
1. 数据处理器扩展
2. AI模型扩展
3. 存储方式扩展
4. 缓存策略扩展

### 4.2 扩展方式
1. 实现接口
2. 继承基类
3. 注册插件
4. 配置驱动

## 5. 模块测试

### 5.1 单元测试
```python
class TestDataService(unittest.TestCase):
    """数据服务测试"""
    
    def setUp(self):
        self.service = DataService()
        
    def test_load_data(self):
        """测试数据加载"""
        pass
        
    def test_process_data(self):
        """测试数据处理"""
        pass
```

### 5.2 集成测试
```python
class TestAPIIntegration(unittest.TestCase):
    """API集成测试"""
    
    async def test_generate_code(self):
        """测试代码生成流程"""
        pass
        
    async def test_data_processing(self):
        """测试数据处理流程"""
        pass
```

## 6. 性能考虑

### 6.1 性能优化点
1. 数据处理优化
2. 缓存策略优化
3. 并发处理优化
4. 资源管理优化

### 6.2 性能监控
1. 接口响应时间
2. 资源使用情况
3. 缓存命中率
4. 错误率统计 