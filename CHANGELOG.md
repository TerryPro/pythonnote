# 更新日志
## [v0.0.4.2] - 2025-01-21

### 新增功能
- 实现了系统提示词配置功能
  - 支持通过前端界面配置AI系统提示词
  - 提供默认配置的保存和重置功能
  - 优化了提示词的存储和加载机制
- 优化了左侧面板的布局
  - 使用折叠面板组织笔记本、数据文件和数据集列表
  - 添加面板宽度拖动调整功能
  - 优化了刷新按钮的交互体验

### 优化改进
- 改进了用户界面交互
  - 优化了折叠面板的展开/收起动画
  - 改进了拖动调整宽度的视觉反馈
  - 优化了刷新按钮的加载状态显示
- 完善了配置管理功能
  - 添加了配置文件的版本控制
  - 优化了配置的读取和保存逻辑
  - 改进了配置重置的处理机制

### Bug修复
- 修复了面板折叠时的样式问题
- 修复了拖动调整宽度时的闪烁问题
- 修复了刷新按钮点击事件冒泡问题

## [v0.0.4] - 2025-01-20

### 新增功能
- 实现了AI代码生成助手功能
  - 支持选择要操作的DataFrame
  - 显示DataFrame的基本信息（行数、列数、内存占用）
  - 显示DataFrame的列信息（列名、数据类型、空值数量）
  - 支持通过自然语言描述生成Python代码
  - 生成的代码可直接在Jupyter单元格中执行

### 优化改进
- 优化了DataFrame信息的展示方式
  - 使用卡片式布局展示基本信息
  - 使用表格展示列信息
  - 优化了UI布局和样式
- 改进了AI提示词构建服务
  - 优化了系统提示词，使AI更好地理解数据上下文
  - 改进了用户提示词，确保生成纯Python代码
  - 支持在代码生成时考虑笔记本环境上下文
- 增强了数据处理能力
  - 添加了对特殊数值类型的处理（NaN、Inf等）
  - 支持处理时间序列数据
  - 优化了JSON序列化过程

### Bug修复
- 修复了DataFrame预览时的JSON序列化错误
- 修复了时间戳数据显示格式问题
- 修复了AI对话框重复打开的问题
- 修复了ResizeObserver相关的UI警告 

## [v0.0.3] - 2025-01-20

### 新增
- 优化了工具栏按钮的样式，使用圆形图标按钮
- 为所有工具栏按钮添加了悬浮提示
- 实现了主题切换的下拉菜单功能
- 为单元格添加了复制内容功能
- 优化了代码编辑器的自适应高度

### 优化
- 改进了工具栏的视觉效果和交互体验
- 优化了主题切换的用户界面
- 改进了单元格的操作按钮布局
- 优化了编辑器的显示效果

### 修复
- 修复了编辑器高度不能自适应内容的问题
- 修复了主题切换按钮的显示问题
- 修复了单元格操作按钮的样式问题

## [v0.0.2] - 2025-01-20

### 新增
- 数据文件管理功能
  - 支持上传CSV和Excel格式文件
  - 文件列表显示（文件名、大小、修改时间）
  - 文件删除功能
  - 数据预览功能
- 数据预览功能
  - 文件基本信息显示
  - 数据基本信息显示
  - 数据内容表格预览
  - 优化的信息展示布局
- 代码生成功能
  - 数据加载代码生成
  - 数据分析代码生成
  - 数据可视化代码生成
  - 一键生成所有代码
- 数据可视化支持
  - 集成Matplotlib和Seaborn
  - 支持数值分布图
  - 支持相关性热力图

### 优化
- 改进数据预览对话框布局
- 优化代码生成按钮分组
- 完善错误处理和提示信息
- 改进文件上传体验

### 修复
- 修复临时文件访问冲突问题
- 修复文件上传后预览不更新的问题
- 修复代码生成后对话框未关闭的问题

## [v0.0.1] - 2025-01-19

### 新增
- 基础笔记本功能
  - Markdown和代码单元格支持
  - 代码实时执行
  - 执行结果显示
- 基础界面框架
  - 顶部导航栏
  - 单元格操作按钮
  - 文件列表面板

### 技术特性
- 前端
  - Vue 3框架
  - Element Plus UI组件库
  - Monaco Editor代码编辑器
  - Font Awesome图标
- 后端
  - FastAPI框架
  - Python代码执行环境
  - PDF导出支持
  - 文件系统管理

### 开发工具
- 代码格式化
- ESLint代码检查
- 类型检查
- 跨域支持
- 开发环境热重载

