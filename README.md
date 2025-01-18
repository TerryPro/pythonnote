# Python 交互式编程环境

一个基于Web的Python交互式编程环境，支持实时代码执行、Markdown编辑、数据可视化等功能。

## 主要功能

### 笔记本编辑
- 支持Python代码和Markdown混合编辑
- 实时代码执行
- matplotlib和plotly图表支持
- 单元格管理（添加、删除、移动、类型切换）

### 文件管理
- 创建、保存、打开笔记本
- 文件重命名
- 文件删除
- PDF导出

### 界面特性
- 多主题支持（浅色、深色、护眼模式）
- 响应式布局
- 美观的代码编辑器
- 实时预览

## 技术栈

### 前端
- Vue 3
- Element Plus
- Monaco Editor
- Font Awesome

### 后端
- FastAPI
- Python 3.8+
- WeasyPrint (PDF导出)
- Jupyter Kernel

## 开始使用

1. 克隆项目
```bash
git clone [项目地址]
```

2. 安装依赖
```bash
# 后端依赖
cd backend
pip install -r requirements.txt

# 前端依赖
cd frontend
npm install
```

3. 启动服务
```bash
# 启动后端服务
cd backend
uvicorn main:app --reload

# 启动前端服务
cd frontend
npm run serve
```

4. 访问应用
打开浏览器访问 `http://localhost:8080`

## 版本历史

查看 [CHANGELOG.md](./CHANGELOG.md) 了解详细的版本历史。

## 开发计划

- [ ] 支持更多图表库
- [ ] 代码自动补全
- [ ] 变量查看器
- [ ] 协作编辑
- [ ] 导入/导出更多格式
- [ ] 单元测试支持

## 贡献指南

欢迎提交问题和功能建议！如果您想贡献代码，请：

1. Fork 项目
2. 创建您的特性分支
3. 提交您的改动
4. 确保代码符合规范
5. 提交 Pull Request

## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件

