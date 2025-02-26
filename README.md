# Python数据分析笔记本

一个基于Web的Python数据分析工具，集成了Jupyter笔记本的功能和AI辅助代码生成能力。

## 功能特性

### 系统效果
![系统界面预览](screen/image_1.png)
![系统界面预览](screen/image_2.png)
![系统界面预览](screen/image_3.png)
![系统界面预览](screen/image_4.png)



系统采用现代化的界面设计，主要包括：
- 左侧可折叠的文件管理面板，支持笔记本、数据文件和数据集的管理
- 中间区域为笔记本编辑区，支持代码和Markdown单元格
- 顶部工具栏提供主题切换、文件操作、单元格添加等功能
- 内置AI代码助手，支持自然语言生成代码

### 1. 笔记本基础功能
- Markdown和代码单元格支持
- 实时代码执行
- 执行结果实时显示
- 单元格操作（添加、删除、移动）
- 代码自动补全和语法高亮
- 可调整布局的文件管理面板

### 2. 数据管理功能
- 支持CSV和Excel格式文件上传
- 文件管理（预览、删除）
- 数据基本信息显示
- 数据内容预览
- DataFrame操作和管理
- 折叠式文件和数据集列表

### 3. AI代码生成助手
- 智能代码生成
- DataFrame信息实时展示
- 自然语言转Python代码
- 代码示例一键插入
- 支持数据分析常用操作
- 可配置的AI系统提示词

### 4. 数据可视化支持
- 集成Matplotlib和Seaborn
- 支持多种图表类型
- 可视化代码智能生成
- 图表实时预览

### 5. 系统配置管理
- AI提示词在线配置
- 配置版本控制
- 一键重置默认配置
- 实时保存和加载

## 技术栈

### 前端
- Vue 3
- Element Plus
- Monaco Editor
- TypeScript
- Vite

### 后端
- FastAPI
- Python 3.10+
- Pandas
- NumPy
- Matplotlib
- DeepSeek API

## 安装说明

### 环境要求
- Python 3.10 或更高版本
- Node.js 16 或更高版本
- npm 8 或更高版本

### 后端安装
1. 创建虚拟环境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，设置必要的环境变量
```

### 前端安装
1. 安装依赖：
```bash
cd frontend
npm install
```

## 启动服务

### 开发环境
1. 启动后端服务：
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

2. 启动前端服务：
```bash
cd frontend
npm run serve
```

### 生产环境
1. 构建前端：
```bash
cd frontend
npm run build
```

2. 启动服务：
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 使用指南

### 1. 数据导入
1. 点击工具栏的"上传文件"按钮
2. 选择CSV或Excel文件
3. 等待文件上传和预处理完成

### 2. 数据分析
1. 在代码单元格中编写Python代码
2. 使用AI助手生成代码：
   - 点击AI助手按钮
   - 选择要操作的DataFrame
   - 输入自然语言描述
   - 获取生成的代码

### 3. 数据可视化
1. 使用内置的可视化库创建图表
2. 通过AI助手生成可视化代码
3. 在笔记本中实时查看图表效果

## 版本历史

查看 [CHANGELOG.md](./CHANGELOG.md) 了解详细的版本更新历史。

## 贡献指南

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交改动：`git commit -m 'Add some AmazingFeature'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

# 前端升级说明

## 笔记本状态管理升级

### 背景

在原有实现中，`notebookStore.js` 仅管理当前活动笔记本的状态，在切换笔记本时需要不断更新状态，这种方式存在以下问题：

1. 状态管理不可靠，容易导致数据丢失
2. 切换笔记本时需要手动保存和恢复状态
3. 无法同时管理多个笔记本的状态

### 升级内容

1. **重构 notebookStore.js**
   - 使用 `notebooks` 对象存储所有打开的笔记本状态，格式为 `{ tabId: notebookState }`
   - 添加 `activeNotebookId` 属性，指向当前活动的笔记本
   - 使用 getters 获取当前活动笔记本的状态，保持与原有 API 的兼容性
   - 添加新的方法：`setActiveNotebook`、`closeNotebook`、`getNotebookState` 等

2. **更新 NotebookContainer.vue**
   - 移除手动保存和恢复笔记本状态的逻辑
   - 使用新的 API 切换活动笔记本

3. **更新 useNotebook.js**
   - 修改所有操作笔记本状态的方法，使用新的 API
   - 添加 `closeNotebook` 方法，用于关闭笔记本

4. **更新 TabsManager.vue**
   - 使用 `closeNotebook` 方法关闭标签页，同时清理笔记本状态

### 优势

1. **可靠性提升**：每个笔记本的状态都独立存储，不会因为切换而丢失
2. **性能优化**：避免了频繁的状态保存和恢复操作
3. **代码简化**：移除了手动管理状态的复杂逻辑
4. **功能增强**：支持同时管理多个笔记本的状态

### 使用方法

1. **获取当前笔记本状态**：
   ```js
   const store = useNotebookStore()
   const cells = store.cells // 获取当前活动笔记本的单元格
   ```

2. **切换活动笔记本**：
   ```js
   store.setActiveNotebook(tabId)
   ```

3. **关闭笔记本**：
   ```js
   const { closeNotebook } = useNotebook()
   closeNotebook(tabId)
   ```

4. **获取指定笔记本的状态**：
   ```js
   const notebookState = store.getNotebookState(tabId)
   ```

## 笔记本创建逻辑优化

### 背景

在原有实现中，系统会在以下情况自动创建新的笔记本：
1. 应用初始化时，如果没有打开的标签页
2. 关闭最后一个标签页后
3. 关闭所有标签页后

这种行为可能会导致创建不必要的空白笔记本，增加用户的困惑。

### 升级内容

1. **移除自动创建笔记本的逻辑**
   - 应用启动时不再自动创建笔记本
   - 关闭最后一个标签页后不再自动创建新笔记本
   - 关闭所有标签页后不再自动创建新笔记本

2. **添加空白状态提示**
   - 当没有打开的笔记本时，显示友好的空白状态提示
   - 提供明确的"创建新笔记本"按钮
   - 引导用户从文件面板打开已有笔记本

3. **明确的用户操作入口**
   - 在工具栏上提供"新建笔记本"按钮
   - 在空白状态页面提供"创建新笔记本"按钮
   - 从文件面板打开已有笔记本

### 优势

1. **用户体验改进**：只有在用户明确需要时才创建新的笔记本
2. **减少困惑**：避免创建不必要的空白笔记本
3. **界面清晰**：提供明确的操作引导
4. **资源优化**：减少不必要的资源消耗

### 使用方法

1. **创建新笔记本**：
   - 点击工具栏上的"+"按钮
   - 在空白状态页面点击"创建新笔记本"按钮

2. **打开已有笔记本**：
   - 从左侧文件面板选择并打开已有笔记本

## 后续优化建议

1. **状态持久化**：将笔记本状态保存到 localStorage，在页面刷新后恢复
2. **自动保存**：定时自动保存笔记本内容，防止意外丢失
3. **撤销/重做功能**：记录操作历史，支持撤销和重做
4. **笔记本比较**：支持比较不同版本的笔记本内容
5. **协作编辑**：支持多人同时编辑同一个笔记本
6. **最近打开的笔记本**：在空白状态页面显示最近打开的笔记本列表
