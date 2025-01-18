# Python 交互式编程环境

这是一个基于 Vue.js 和 FastAPI 的现代化交互式 Python 编程环境，类似于 Jupyter Notebook，但提供了更简洁的界面和更专注的功能。该项目支持 Python 代码的实时执行、Markdown 文档编写，以及笔记本的保存和 PDF 导出功能。

## 功能特性

1. **代码执行**
   - 支持 Python 代码的实时执行
   - 保持代码执行上下文，支持变量持久化
   - 支持 matplotlib 等库的图表输出
   - 支持 Plotly 交互式图表
   - 支持代码执行结果的实时显示
   - 支持错误信息的友好展示

2. **数据可视化**
   - 支持 Matplotlib 静态图表
   - 支持 Plotly 交互式图表
     - 散点图、折线图、柱状图等多种图表类型
     - 支持图表缩放、平移、旋转等交互操作
     - 支持图表数据的导出
     - 自动适应暗色/亮色主题
   - 图表自适应容器大小
   - 支持图表的保存和加载

3. **Markdown 支持**
   - 支持 Markdown 格式文档编写
   - 实时预览 Markdown 渲染效果
   - 支持常用 Markdown 语法
   - 支持数学公式（通过 KaTeX）

4. **单元格管理**
   - 支持单元格上下移动调整顺序
   - 支持在单元格中切换代码和 Markdown 模式
   - 支持单元格的添加和删除
   - 单元格执行状态实时显示
   - 支持在任意位置插入新单元格

5. **文件管理**
   - 自动保存笔记本
   - 支持笔记本的导入和导出
   - 按最后修改时间排序显示笔记本列表
   - 支持笔记本重命名

6. **PDF导出**
   - 支持将笔记本导出为 PDF 格式
   - 美观的 PDF 排版
   - 支持代码语法高亮
   - 支持中文字体显示
   - 支持图表和图片的导出

## 技术栈

### 前端
- Vue 3 (组合式 API)
- Monaco Editor (代码编辑器)
- Marked (Markdown 渲染)
- Font Awesome (图标)
- Plotly.js (交互式图表)
- Axios (HTTP 请求)

### 后端
- FastAPI (Python Web 框架)
- Uvicorn (ASGI 服务器)
- Jinja2 (模板引擎)
- WeasyPrint (PDF 生成)
- Plotly (Python 图表库)
- Python 标准库

## 安装说明

1. 安装 Python 依赖：
```bash
pip install -r requirements.txt
```

2. 安装前端依赖：
```bash
cd frontend
npm install
```

3. 启动开发服务器：

后端：
```bash
cd backend
uvicorn main:app --reload
```

前端：
```bash
cd frontend
npm run serve
```

## 使用说明

### 1. 创建新笔记本
- 点击顶部工具栏的"新建笔记本"按钮
- 默认创建一个代码单元格
- 可以通过工具栏添加代码或 Markdown 单元格

### 2. 单元格操作
- 使用单元格右侧的上下箭头按钮调整顺序
- 使用下拉菜单切换单元格类型（Python/Markdown）
- 点击"+"按钮在当前位置后添加新单元格
- 代码单元格支持：
  - 运行代码（点击运行按钮或使用 Shift+Enter）
  - 查看执行结果和错误信息
  - 显示图表输出（支持 Matplotlib 和 Plotly）

### 3. 数据可视化
- 支持 Matplotlib 静态图表：
  ```python
  import matplotlib.pyplot as plt
  plt.plot([1, 2, 3], [1, 2, 3])
  plt.show()
  ```
- 支持 Plotly 交互式图表：
  ```python
  import plotly.express as px
  df = px.data.iris()
  fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
  fig.show()
  ```

### 4. 保存和导出
- 笔记本会自动保存
- 可以手动点击"保存笔记本"按钮
- 支持导出为 PDF 格式，包含：
  - 代码及其执行结果
  - Markdown 内容
  - 图表和图片
  - 数学公式

### 5. 文件管理
- 左侧面板显示所有笔记本文件
- 点击文件名打开对应笔记本
- 当前打开的文件会高亮显示
- 支持创建新笔记本和重命名现有笔记本

## 开发者指南

### 项目结构
```
.
├── backend/
│   ├── main.py            # FastAPI 应用主文件
│   ├── code_executor.py   # Python 代码执行器
│   ├── notebooks/         # 笔记本存储目录
│   └── requirements.txt   # Python 依赖
├── frontend/
│   ├── src/
│   │   ├── App.vue       # 主应用组件
│   │   ├── components/   # Vue 组件
│   │   └── main.js       # 应用入口
│   ├── package.json      # 前端依赖
│   └── vue.config.js     # Vue 配置
└── README.md             # 项目文档
```

### 开发规范
1. **代码风格**
   - 后端遵循 PEP 8 规范
   - 前端使用 ESLint 和 Prettier
   - 组件使用组合式 API
   
2. **提交规范**
   - 使用清晰的提交信息
   - 每个提交专注于单一功能或修复
   - 保持提交历史的整洁

### 性能优化
1. **前端优化**
   - Plotly.js 全局加载，避免重复加载
   - 使用 Vue 的 nextTick 确保 DOM 更新
   - 图表容器高度自适应

2. **后端优化**
   - 使用 FastAPI 的异步特性
   - 优化代码执行上下文
   - 合理处理图表数据

## 更新日志

### v1.1.0
- 添加 Plotly 交互式图表支持
- 优化图表显示效果
- 改进笔记本保存和加载功能

### v1.0.0
- 初始版本发布
- 支持基本的代码执行和 Markdown
- 支持 Matplotlib 图表

## 注意事项

1. **安全性**
   - 代码在隔离环境中执行
   - 限制执行时间，防止死循环
   - 限制内存使用，防止内存溢出

2. **性能优化**
   - 大型笔记本分页加载
   - 懒加载图片和组件
   - 缓存执行结果

3. **浏览器兼容性**
   - 支持现代浏览器
   - Chrome/Firefox/Safari/Edge

## 开发计划

- [x] 添加单元格上下移动功能
- [x] 实现代码执行状态显示
- [x] 支持 PDF 导出
- [ ] 添加代码自动补全
- [ ] 支持更多文件格式导出
- [ ] 添加用户认证系统
- [ ] 优化代码执行性能
- [ ] 添加更多主题样式
- [ ] 支持协同编辑
- [ ] 添加版本控制功能

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 问题反馈

如果您在使用过程中遇到任何问题，或有任何建议，请提交 Issue 或联系开发团队。

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

