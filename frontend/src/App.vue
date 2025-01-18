<template>
  <div id="app">
    <nav class="navbar">
      <h1>Python 交互式编程环境</h1>
      <div class="toolbar">
        <div class="theme-selector">
          <select v-model="currentTheme" @change="changeTheme" class="theme-select">
            <option v-for="(theme, key) in themes" :key="key" :value="key">
              {{ theme.name }}
            </option>
          </select>
        </div>
        <button @click="createNewNotebook" class="toolbar-btn">新建笔记本</button>
        <button @click="saveNotebook" class="toolbar-btn">保存笔记本</button>
        <button @click="exportPDF" class="toolbar-btn">导出PDF</button>
        <button @click="addCell('code')" class="toolbar-btn">添加代码单元格</button>
        <button @click="addCell('markdown')" class="toolbar-btn">添加Markdown单元格</button>
      </div>
    </nav>
    
    <main class="main-container">
      <div class="file-panel">
        <div class="file-panel-header">
          <h3>文件列表</h3>
        </div>
        <div class="file-list">
          <div v-for="file in files" 
               :key="file.path" 
               @click="openNotebook(file)"
               class="file-item"
               :class="{ active: currentFile === file.path }">
            <i class="fas fa-file-code file-icon"></i>
            <span class="file-name">{{ file.name }}</span>
          </div>
        </div>
      </div>

      <div class="notebook" v-if="cells.length">
        <div class="notebook-cells">
          <div v-for="cellId in cells" :key="cellId" class="cell-wrapper">
            <div class="cell-type-selector">
              <select 
                :value="cellTypes[cellId]" 
                @change="(e) => changeCellType(cellId, e.target.value)"
                class="type-select"
              >
                <option value="code">Python</option>
                <option value="markdown">Markdown</option>
              </select>
              <div class="cell-actions">
                <button 
                  v-if="cellTypes[cellId] === 'code'"
                  @click="() => $refs[`codeCell${cellId}`]?.[0]?.executeCode()" 
                  class="icon-btn" 
                  title="运行"
                >
                  <i class="fas fa-play"></i>
                </button>
                <button 
                  v-else
                  @click="() => $refs[`markdownCell${cellId}`]?.[0]?.toggleEdit()" 
                  class="icon-btn" 
                  :title="markdownEditStates[cellId] ? '预览' : '编辑'"
                >
                  <i :class="markdownEditStates[cellId] ? 'fas fa-eye' : 'fas fa-edit'"></i>
                </button>
                <button @click="() => addCell(cellId)" class="icon-btn" title="添加单元格">
                  <i class="fas fa-plus"></i>
                </button>
                <button 
                  @click="() => moveCellUp(cellId)" 
                  class="icon-btn" 
                  title="向上移动"
                  :disabled="cells.indexOf(cellId) === 0"
                >
                  <i class="fas fa-arrow-up"></i>
                </button>
                <button 
                  @click="() => moveCellDown(cellId)" 
                  class="icon-btn" 
                  title="向下移动"
                  :disabled="cells.indexOf(cellId) === cells.length - 1"
                >
                  <i class="fas fa-arrow-down"></i>
                </button>
              </div>
            </div>
            <CodeCell
              v-if="cellTypes[cellId] === 'code'"
              :ref="`codeCell${cellId}`"
              :cell-id="cellId"
              :content="cellContents[cellId]"
              :output-content="cellOutputs[cellId]"
              @update:content="(v) => cellContents[cellId] = v"
              @update:output="(v) => cellOutputs[cellId] = v"
              @execution-complete="handleExecutionComplete"
            />
            <MarkdownCell
              v-else
              :ref="`markdownCell${cellId}`"
              :cell-id="cellId"
              v-model:content="cellContents[cellId]"
              v-model:isEditing="markdownEditStates[cellId]"
            />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, provide } from 'vue'
import CodeCell from './components/CodeCell.vue'
import MarkdownCell from './components/MarkdownCell.vue'
import { v4 as uuidv4 } from 'uuid'
import { themes, applyTheme } from './themes'

const cells = ref([])
const files = ref([])
const currentFile = ref(null)
const cellContents = ref({})
const cellOutputs = ref({})
const cellTypes = ref({})
const markdownEditStates = ref({})
const currentTheme = ref('light')

// 提供主题变量给子组件
provide('currentTheme', currentTheme)

// 创建新笔记本
const createNewNotebook = async () => {
  // 重置Python上下文
  await fetch('http://localhost:8000/reset_context', { method: 'POST' })
  
  cells.value = []
  cellContents.value = {}
  cellOutputs.value = {}
  cellTypes.value = {}
  markdownEditStates.value = {}  // 重置Markdown编辑状态
  currentFile.value = null
  addCell('code')
}

// 保存笔记本
const saveNotebook = async () => {
  if (!currentFile.value) {
    const fileName = prompt('请输入笔记本名称：')
    if (!fileName) return
    currentFile.value = fileName + '.ipynb'
  }

  const notebook = {
    cells: cells.value.map(cellId => ({
      id: cellId,
      type: cellTypes.value[cellId],
      content: cellContents.value[cellId] || '',
      output: cellTypes.value[cellId] === 'code' ? (cellOutputs.value[cellId] || {
        output: '',
        plot: '',
        plotly_html: '',
        status: 'idle'
      }) : null
    }))
  }

  await fetch('http://localhost:8000/save_notebook', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      filename: currentFile.value,
      notebook: notebook
    })
  })

  loadFileList()
}

// 打开笔记本
const openNotebook = async (file) => {
  try {
    // 重置Python上下文
    await fetch('http://localhost:8000/reset_context', { method: 'POST' })

    const response = await fetch(`http://localhost:8000/load_notebook?filename=${file.path}`)
    const notebook = await response.json()
    
    currentFile.value = file.path
    cells.value = []
    cellContents.value = {}
    cellOutputs.value = {}
    cellTypes.value = {}
    
    if (notebook.cells && Array.isArray(notebook.cells)) {
      notebook.cells.forEach(cell => {
        if (cell && cell.id) {
          cells.value.push(cell.id)
          cellTypes.value[cell.id] = cell.type || 'code'
          cellContents.value[cell.id] = cell.content || ''
          
          if (cell.type === 'code') {
            cellOutputs.value[cell.id] = {
              output: cell.output?.output || '',
              plot: cell.output?.plot || '',
              plotly_html: cell.output?.plotly_html || '',
              status: cell.output?.status || 'idle'
            }
          }
        }
      })
    }

    if (cells.value.length === 0) {
      addCell('code')
    }
  } catch (error) {
    console.error('打开笔记本失败:', error)
    // 如果打开失败，创建一个新的笔记本
    createNewNotebook()
  }
}

// 加载文件列表
const loadFileList = async () => {
  const response = await fetch('http://localhost:8000/list_notebooks')
  files.value = await response.json()
}

const addCell = (type = 'code') => {
  const newCellId = uuidv4()
  cells.value.push(newCellId)
  cellContents.value[newCellId] = ''
  cellTypes.value[newCellId] = type
  if (type === 'code') {
    cellOutputs.value[newCellId] = {
      output: '',
      plot: '',
      plotly_html: '',
      status: 'idle'
    }
  } else if (type === 'markdown') {
    markdownEditStates.value[newCellId] = true
  }
}

const handleExecutionComplete = (cellId) => {
  const index = cells.value.indexOf(cellId)
  if (index === cells.value.length - 1) {
    addCell('code')
  }
}

const changeCellType = (cellId, newType) => {
  if (!cellId || cellTypes.value[cellId] === newType) return
  
  const currentContent = cellContents.value[cellId] || ''
  
  // 更新单元格类型
  cellTypes.value[cellId] = newType
  
  // 如果切换到代码单元格，需要初始化输出
  if (newType === 'code') {
    cellOutputs.value[cellId] = {
      output: '',
      plot: '',
      status: 'idle'
    }
  } else {
    // 如果切换到 Markdown，初始化编辑状态
    markdownEditStates.value[cellId] = true
  }
  
  // 保持内容不变
  cellContents.value[cellId] = currentContent
}

// 导出PDF
const exportPDF = async () => {
  try {
    if (!currentFile.value) {
      const fileName = prompt('请输入PDF文件名：')
      if (!fileName) return
      currentFile.value = fileName
    }

    const notebook = {
      cells: cells.value.map(cellId => ({
        id: cellId,
        type: cellTypes.value[cellId],
        content: cellContents.value[cellId] || '',
        output: cellTypes.value[cellId] === 'code' ? (cellOutputs.value[cellId] || {
          output: '',
          plot: '',
          status: 'idle'
        }) : null
      }))
    }

    const response = await fetch('http://localhost:8000/export_pdf', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        filename: currentFile.value,
        notebook: notebook
      })
    })

    if (!response.ok) {
      throw new Error('PDF导出失败')
    }

    // 获取PDF文件并下载
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${currentFile.value}.pdf`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  } catch (error) {
    console.error('导出PDF失败:', error)
    alert('导出PDF失败: ' + error.message)
  }
}

const moveCellUp = (cellId) => {
  const currentIndex = cells.value.indexOf(cellId)
  if (currentIndex > 0) {
    const temp = cells.value[currentIndex]
    cells.value[currentIndex] = cells.value[currentIndex - 1]
    cells.value[currentIndex - 1] = temp
  }
}

const moveCellDown = (cellId) => {
  const currentIndex = cells.value.indexOf(cellId)
  if (currentIndex < cells.value.length - 1) {
    const temp = cells.value[currentIndex]
    cells.value[currentIndex] = cells.value[currentIndex + 1]
    cells.value[currentIndex + 1] = temp
  }
}

const changeTheme = () => {
  const editorTheme = applyTheme(currentTheme.value)
  // 更新所有代码编辑器的主题
  cells.value.forEach(cellId => {
    const codeCell = document.querySelector(`#codeCell${cellId} .monaco-editor`)
    if (codeCell) {
      // 触发 Monaco Editor 主题更新
      window.monaco?.editor?.setTheme(editorTheme)
    }
  })
}

// 在组件挂载时应用默认主题
onMounted(async () => {
  await loadFileList()
  addCell('code')
  applyTheme(currentTheme.value)
})
</script>

<style>
:root {
  --primary-color: #1976D2;
  --background-color: #f5f7fa;
  --text-color: #2c3e50;
  --border-color: #e0e0e0;
  --cell-background: #ffffff;
  --toolbar-background: #1976D2;
  --toolbar-text: #ffffff;
  --code-background: #f8f9fa;
  --markdown-background: #ffffff;
  --button-hover: #f5f5f5;
  --button-active: #e8e8e8;
  --selection: #e3f2fd;
}

body {
  margin: 0;
  padding: 0;
  background-color: var(--background-color);
  color: var(--text-color);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  line-height: 1.6;
  min-height: 100vh;
  transition: background-color 0.3s ease;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  margin: 0;
  padding: 0;
}

.navbar {
  background-color: var(--toolbarBackground);
  color: var(--toolbarText);
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.navbar h1 {
  margin: 0;
  font-size: 1.5em;
  font-weight: 500;
  color: var(--toolbarText);
  transition: color 0.3s ease;
}

.toolbar {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.toolbar-btn {
  height: 36px;
  padding: 0 1rem;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--toolbarText);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9em;
}

.toolbar-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

.toolbar-btn:active {
  background-color: rgba(255, 255, 255, 0.3);
}

.theme-selector {
  margin-right: 1rem;
}

.theme-select {
  height: 36px;
  padding: 0 1rem;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--toolbarText);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9em;
}

.theme-select:hover {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

.theme-select:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.4);
  background-color: rgba(255, 255, 255, 0.15);
}

.theme-select option {
  background-color: var(--background);
  color: var(--text);
  padding: 8px;
}

.main-container {
  flex: 1;
  display: flex;
  min-height: calc(100vh - 64px);
}

.file-panel {
  width: 250px;
  background: var(--filePanel);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s ease;
}

.file-panel-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  background: var(--filePanel);
  transition: background-color 0.3s ease;
}

.file-panel-header h3 {
  margin: 0;
  font-size: 1.1em;
  color: var(--filePanelText);
}

.file-list {
  flex: 1;
  overflow-y: auto;
  background: var(--filePanel);
  transition: background-color 0.3s ease;
}

.file-item {
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--filePanelText);
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-item:hover {
  background-color: var(--filePanelHover);
}

.file-item.active {
  background-color: var(--filePanelActive);
  border-right: 3px solid var(--primary-color);
}

.file-icon {
  font-size: 1em;
  color: var(--primary-color);
  opacity: 0.8;
  transition: all 0.3s ease;
}

.file-item:hover .file-icon {
  opacity: 1;
  transform: scale(1.1);
}

.file-item.active .file-icon {
  opacity: 1;
  color: var(--primary-color);
}

.file-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notebook {
  flex: 1;
  padding: 1rem;
  background: var(--background);
  overflow-y: auto;
  transition: background-color 0.3s ease;
}

.cell-wrapper {
  margin-bottom: 8px;
  animation: fadeIn 0.3s ease-out;
  padding: 8px;
  background-color: var(--cellBackground);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.cell-wrapper:last-child {
  margin-bottom: 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .navbar {
    padding: 1rem;
  }

  .file-panel {
    width: 200px;
  }

  .notebook {
    padding: 1rem;
  }
}

.cell-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.cell-type-select {
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: white;
  font-size: 0.9em;
  color: var(--text-color);
  cursor: pointer;
  transition: all 0.2s ease;
  height: 32px;
}

.cell-type-select:hover {
  border-color: var(--primary-color);
}

.cell-type-select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
}

.cell-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.cell-action-btn {
  height: 32px;
  padding: 0 0.75rem;
  background-color: white;
  border: 1px solid var(--border-color);
  color: var(--text-color);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9em;
}

.cell-action-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.cell-type-selector {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 4px 0;
  margin-bottom: 2px;
}

.type-select {
  padding: 6px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: var(--cellBackground);
  color: var(--text);
  font-size: 13px;
  cursor: pointer;
  outline: none;
  min-width: 100px;
  transition: all 0.3s ease;
}

.type-select:hover {
  border-color: var(--primary-color);
}

.type-select:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
}

.type-select option {
  background-color: var(--cellBackground);
  color: var(--text);
  padding: 8px;
}

.notebook-cells {
  padding: 0 8px;
}

.editor-container {
  background: var(--cell-background);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.output-container {
  margin-top: 4px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  overflow: hidden;
  background-color: var(--code-background);
  transition: background-color 0.3s ease;
}

.output-text {
  padding: 12px;
  font-family: 'Fira Code', monospace;
  font-size: 13px;
  line-height: 1.5;
  white-space: pre-wrap;
  background-color: var(--code-background);
  color: var(--text-color);
  transition: background-color 0.3s ease, color 0.3s ease;
}

.icon-btn {
  width: 32px;
  height: 32px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: var(--cell-background);
  color: var(--text-color);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.icon-btn:hover:not(:disabled) {
  background: var(--button-hover);
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.icon-btn:active:not(:disabled) {
  background: var(--button-active);
}
</style>
