<template>
  <div id="app">
    <nav class="navbar">
      <div class="navbar-left">
        <h1>Python 交互式编程环境</h1>
        <span class="version">v0.0.1</span>
      </div>
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
               class="file-item"
               :class="{ active: currentFile === file.path }">
            <div class="file-content" @click="openNotebook(file)">
              <i class="fas fa-file-code file-icon"></i>
              <span class="file-name">{{ file.name }}</span>
            </div>
            <div class="file-actions">
              <button 
                @click="renameNotebook(file)"
                class="icon-btn"
                title="重命名">
                <i class="fas fa-edit"></i>
              </button>
              <button 
                @click="confirmDelete(file)"
                class="icon-btn delete-btn"
                title="删除">
                <i class="fas fa-trash"></i>
              </button>
            </div>
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
                <button 
                  @click="() => confirmDeleteCell(cellId)" 
                  class="icon-btn delete-btn" 
                  title="删除单元格"
                >
                  <i class="fas fa-trash"></i>
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

    <!-- 添加重命名对话框 -->
    <el-dialog
      v-model="renameDialogVisible"
      title="重命名笔记本"
      width="30%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <el-form :model="renameForm" label-width="0px">
        <el-form-item>
          <el-input
            v-model="renameForm.newName"
            placeholder="请输入新的文件名"
            @keyup.enter="handleRename"
          >
            <template #append>.ipynb</template>
          </el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="renameDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleRename">确认</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 添加删除确认对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="删除笔记本"
      width="30%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <div class="delete-dialog-content">
        <el-alert
          title="此操作将永久删除该笔记本，是否继续？"
          type="warning"
          :closable="false"
          show-icon
        />
        <div class="file-info">
          <span class="label">文件名：</span>
          <span class="value">{{ deleteFile?.name }}</span>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="handleDelete">确定删除</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 添加删除单元格确认对话框 -->
    <el-dialog
      v-model="deleteCellDialogVisible"
      title="删除单元格"
      width="30%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <div class="delete-dialog-content">
        <el-alert
          title="确定要删除这个单元格吗？此操作不可恢复。"
          type="warning"
          :closable="false"
          show-icon
        />
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteCellDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="handleDeleteCell">确定删除</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, provide } from 'vue'
import CodeCell from './components/CodeCell.vue'
import MarkdownCell from './components/MarkdownCell.vue'
import { v4 as uuidv4 } from 'uuid'
import { themes, applyTheme } from './themes'
import { ElMessage } from 'element-plus'

const cells = ref([])
const files = ref([])
const currentFile = ref(null)
const cellContents = ref({})
const cellOutputs = ref({})
const cellTypes = ref({})
const markdownEditStates = ref({})
const currentTheme = ref('light')

// 添加重命名相关的响应式变量
const renameDialogVisible = ref(false)
const renameForm = ref({
  newName: '',
  file: null
})

// 添加删除相关的响应式变量
const deleteDialogVisible = ref(false)
const deleteFile = ref(null)

// 添加删除单元格相关的响应式变量
const deleteCellDialogVisible = ref(false)
const deleteCellId = ref(null)

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

// 修改重命名笔记本函数
const renameNotebook = (file) => {
  renameForm.value.newName = file.name.replace('.ipynb', '')
  renameForm.value.file = file
  renameDialogVisible.value = true
}

// 处理重命名确认
const handleRename = async () => {
  if (!renameForm.value.newName.trim()) {
    ElMessage.warning('文件名不能为空')
    return
  }
  
  const newFilename = renameForm.value.newName.endsWith('.ipynb') 
    ? renameForm.value.newName 
    : `${renameForm.value.newName}.ipynb`
  
  try {
    const response = await fetch('http://localhost:8000/rename_notebook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        old_filename: renameForm.value.file.path,
        new_filename: newFilename
      })
    })
    
    const result = await response.json()
    if (result.status === 'success') {
      // 如果当前打开的文件被重命名，更新currentFile
      if (currentFile.value === renameForm.value.file.path) {
        currentFile.value = newFilename
      }
      // 重新加载文件列表
      await loadFileList()
      renameDialogVisible.value = false
      ElMessage.success('重命名成功')
    } else {
      ElMessage.error(result.message || '重命名失败')
    }
  } catch (error) {
    console.error('重命名失败:', error)
    ElMessage.error('重命名失败: ' + error.message)
  }
}

// 确认删除
const confirmDelete = (file) => {
  deleteFile.value = file
  deleteDialogVisible.value = true
}

// 处理删除
const handleDelete = async () => {
  try {
    const response = await fetch(`http://localhost:8000/delete_notebook?filename=${deleteFile.value.path}`, {
      method: 'DELETE'
    })
    
    const result = await response.json()
    if (result.status === 'success') {
      // 如果删除的是当前打开的文件，创建新笔记本
      if (currentFile.value === deleteFile.value.path) {
        await createNewNotebook()
      }
      // 重新加载文件列表
      await loadFileList()
      deleteDialogVisible.value = false
      ElMessage.success(result.message)
    } else {
      ElMessage.error(result.message || '删除失败')
    }
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败: ' + error.message)
  }
}

// 确认删除单元格
const confirmDeleteCell = (cellId) => {
  deleteCellId.value = cellId
  deleteCellDialogVisible.value = true
}

// 处理删除单元格
const handleDeleteCell = () => {
  const index = cells.value.indexOf(deleteCellId.value)
  if (index > -1) {
    // 从数组中移除单元格ID
    cells.value.splice(index, 1)
    // 删除相关的内容和状态
    delete cellContents.value[deleteCellId.value]
    delete cellOutputs.value[deleteCellId.value]
    delete cellTypes.value[deleteCellId.value]
    delete markdownEditStates.value[deleteCellId.value]
    
    // 如果删除后没有单元格了，添加一个新的代码单元格
    if (cells.value.length === 0) {
      addCell('code')
    }
    
    deleteCellDialogVisible.value = false
    ElMessage.success('单元格已删除')
  }
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
  height: 100vh;
  margin: 0;
  padding: 0;
  overflow: hidden;
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
  z-index: 100;
  flex-shrink: 0;
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
  height: calc(100vh - 72px); /* 减去navbar的高度 */
  overflow: hidden;
}

.file-panel {
  width: 250px;
  background: var(--filePanel);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s ease;
  flex-shrink: 0;
}

.file-panel-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  background: var(--filePanel);
  transition: background-color 0.3s ease;
  flex-shrink: 0;
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
  justify-content: space-between;
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
  background: var(--background);
  overflow-y: auto;
  transition: background-color 0.3s ease;
  position: relative;
}

.notebook-cells {
  padding: 1rem;
  height: 100%;
  overflow-y: auto;
}

/* 添加滚动条样式 */
.notebook-cells::-webkit-scrollbar,
.file-list::-webkit-scrollbar {
  width: 8px;
}

.notebook-cells::-webkit-scrollbar-track,
.file-list::-webkit-scrollbar-track {
  background: transparent;
}

.notebook-cells::-webkit-scrollbar-thumb,
.file-list::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.notebook-cells::-webkit-scrollbar-thumb:hover,
.file-list::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.2);
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

.file-content {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.file-actions {
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.file-item:hover .file-actions {
  opacity: 1;
}

.file-actions .icon-btn {
  padding: 0;
  width: 24px;
  height: 24px;
  font-size: 12px;
}

/* 添加对话框相关样式 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.el-dialog__body {
  padding: 20px;
}

.delete-btn {
  color: #f56c6c;
}

.delete-btn:hover {
  background: #fef0f0;
  border-color: #f56c6c;
  color: #f56c6c;
}

.delete-dialog-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.file-info {
  margin-top: 8px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 4px;
  font-size: 14px;
}

.file-info .label {
  color: #606266;
  margin-right: 8px;
}

.file-info .value {
  color: #303133;
  font-weight: 500;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.version {
  font-size: 0.9em;
  opacity: 0.8;
  padding: 2px 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  cursor: help;
  transition: all 0.3s ease;
}

.version:hover {
  opacity: 1;
  background: rgba(255, 255, 255, 0.2);
}
</style>
