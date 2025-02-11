# 快速入门指南

## 1. 项目概述

数据分析助手是一个基于Python的数据分析平台，提供以下核心功能：

- 数据处理和分析
- AI辅助代码生成
- 可视化展示
- 自动化报告生成

## 2. 环境准备

确保您已经完成[环境配置](environment.md)中的所有步骤。

## 3. 第一个数据分析项目

### 3.1 创建项目

```bash
# 克隆项目
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# 安装依赖
pip install -r requirements.txt
```

### 3.2 启动服务

```bash
# 启动后端服务
cd backend
uvicorn main:app --reload

# 新开终端，启动前端服务
cd frontend
npm install
npm run dev
```

### 3.3 使用示例

#### 示例1：数据导入和基础分析

```python
# 导入数据
import pandas as pd
df = pd.read_csv('data/example.csv')

# 查看数据基本信息
df.info()
df.describe()

# 数据清洗
df = df.dropna()  # 处理缺失值
df = df.drop_duplicates()  # 删除重复值
```

#### 示例2：使用AI生成代码

1. 打开Web界面 `http://localhost:3000`
2. 在代码生成区输入：
   ```
   分析销售数据的月度趋势，并生成折线图
   ```
3. AI将生成相应的Python代码：
   ```python
   import pandas as pd
   import matplotlib.pyplot as plt
   
   # 按月份聚合销售数据
   monthly_sales = df.groupby(pd.Grouper(key='date', freq='M'))['sales'].sum()
   
   # 绘制折线图
   plt.figure(figsize=(12, 6))
   monthly_sales.plot(kind='line', marker='o')
   plt.title('月度销售趋势')
   plt.xlabel('日期')
   plt.ylabel('销售额')
   plt.grid(True)
   plt.show()
   ```

## 4. 基础功能

### 4.1 数据处理

- 数据导入导出
- 数据清洗转换
- 数据分析计算
- 数据可视化

### 4.2 AI辅助

- 代码生成
- 分析建议
- 错误修复
- 性能优化

### 4.3 可视化

- 基础图表
- 交互式图表
- 自定义主题
- 导出分享

## 5. 最佳实践

### 5.1 数据处理建议

1. 始终备份原始数据
2. 使用数据验证确保数据质量
3. 采用增量处理处理大数据
4. 合理使用缓存提高性能

### 5.2 AI使用技巧

1. 提供清晰具体的提示词
2. 包含必要的上下文信息
3. 验证生成的代码
4. 适当调整和优化

### 5.3 性能优化

1. 使用异步处理
2. 启用缓存
3. 批量处理
4. 定期清理临时文件

## 6. 常见问题

### 6.1 安装问题

Q: 安装依赖时报错？
A: 检查Python版本是否符合要求，尝试使用`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

Q: 启动服务失败？
A: 检查端口是否被占用，确认环境变量配置正确

### 6.2 使用问题

Q: 数据导入失败？
A: 检查文件格式是否正确，确认文件编码

Q: AI生成的代码有误？
A: 提供更详细的上下文信息，检查输入数据的正确性

## 7. 下一步

- 阅读[API文档](../api/overview.md)了解更多接口
- 查看[开发指南](../development/standards.md)了解开发规范
- 参考[示例代码](https://github.com/yourusername/your-repo/examples)
- 加入[社区讨论](https://github.com/yourusername/your-repo/discussions)

## 8. 帮助和支持

- [问题反馈](https://github.com/yourusername/your-repo/issues)
- [技术支持](https://support.example.com)
- [更新日志](../CHANGELOG.md)
- [常见问题](FAQ.md) 