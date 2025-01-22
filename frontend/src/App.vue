<template>
  <div id="app">
    <nav class="navbar">
      <div class="navbar-left">
        <h1>Python 交互式编程环境</h1>
        <span class="version">{{ version }}</span>
      </div>
      <div class="toolbar">
        <el-dropdown @command="handleThemeChange" trigger="click">
          <el-button class="toolbar-btn" type="primary" plain>
            <i class="fas fa-palette"></i>
            <el-tooltip
              class="box-item"
              effect="light"
              content="选择主题"
              placement="bottom"
            >
              <template #default>
                <span class="el-dropdown-link"></span>
              </template>
            </el-tooltip>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item 
                v-for="(theme, key) in themes" 
                :key="key"
                :command="key"
                :class="{ 'is-active': currentTheme === key }"
              >
                <i class="fas fa-check" v-if="currentTheme === key"></i>
                {{ theme.name }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        
        <el-tooltip content="新建笔记本" placement="bottom" :hide-after="0">
          <button @click="createNewNotebook" class="toolbar-btn">
            <i class="fas fa-plus"></i>
          </button>
        </el-tooltip>

        <el-tooltip content="保存笔记本" placement="bottom" :hide-after="0">
          <button @click="showSaveDialog" class="toolbar-btn">
            <i class="fas fa-save"></i>
          </button>
        </el-tooltip>

        <el-tooltip content="导出PDF" placement="bottom" :hide-after="0">
          <button @click="exportPDF" class="toolbar-btn">
            <i class="fas fa-file-pdf"></i>
          </button>
        </el-tooltip>

        <el-tooltip content="系统配置" placement="bottom" :hide-after="0">
          <button @click="showSystemConfig" class="toolbar-btn">
            <i class="fas fa-cog"></i>
          </button>
        </el-tooltip>

        <el-tooltip content="添加代码单元格" placement="bottom" :hide-after="0">
          <button @click="addCell('code')" class="toolbar-btn">
            <i class="fas fa-code"></i>
          </button>
        </el-tooltip>

        <el-tooltip content="添加Markdown单元格" placement="bottom" :hide-after="0">
          <button @click="addCell('markdown')" class="toolbar-btn">
            <i class="fas fa-markdown"></i>
          </button>
        </el-tooltip>

        <el-tooltip content="上传数据文件" placement="bottom" :hide-after="0">
          <button @click="triggerFileUpload" class="toolbar-btn upload-btn">
            <i class="fas fa-upload"></i>
          </button>
        </el-tooltip>

        <el-tooltip content="管理预定义提示词" placement="bottom">
          <div class="tool-item" @click="showPromptManager = true">
            <i class="fas fa-list-alt"></i>
          </div>
        </el-tooltip>
      </div>
    </nav>
    
    <main class="main-container">
      <div class="file-panel" :style="{ width: panelWidth + 'px' }">
        <el-collapse v-model="activePanels" accordion>
          <!-- 笔记本文件列表 -->
          <el-collapse-item name="notebooks">
            <template #title>
              <div class="panel-header">
                <h3><i class="fas fa-book"></i> 笔记文件</h3>
                <button 
                  @click.stop="refreshNotebooks"
                  class="icon-btn refresh-btn"
                  title="刷新笔记本列表">
                  <i class="fas fa-sync-alt"></i>
                </button>
              </div>
            </template>
            <div class="file-list">
              <div v-for="file in notebookFiles" 
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
          </el-collapse-item>

          <!-- 数据文件列表 -->
          <el-collapse-item name="datafiles">
            <template #title>
              <div class="panel-header">
                <h3><i class="fas fa-file-alt"></i> 数据文件</h3>
                <button 
                  @click.stop="refreshDataFiles"
                  class="icon-btn refresh-btn"
                  title="刷新文件列表">
                  <i class="fas fa-sync-alt"></i>
                </button>
              </div>
            </template>
            <div class="file-list">
              <div v-for="file in dataFiles" 
                   :key="file.path" 
                   class="file-item"
                   :class="{ active: currentDataFile === file.path }">
                <div class="file-content">
                  <i :class="['fas', getDataFileIcon(file)]"></i>
                  <span class="file-name">{{ file.name }}</span>
                </div>
                <div class="file-actions">
                  <button 
                    @click="previewDataFile(file)"
                    class="icon-btn preview-btn"
                    title="预览数据">
                    <i class="fas fa-eye"></i>
                  </button>
                  <button 
                    @click="renameDataFile(file)"
                    class="icon-btn"
                    title="重命名">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button 
                    @click="deleteDataFile(file)"
                    class="icon-btn delete-btn"
                    title="删除">
                    <i class="fas fa-trash"></i>
                  </button>
                </div>
              </div>
            </div>
          </el-collapse-item>

          <!-- DataFrame变量列表 -->
          <el-collapse-item name="dataframes">
            <template #title>
              <div class="panel-header">
                <h3><i class="fas fa-database"></i> 数据集合</h3>
                <button 
                  @click.stop="refreshDataFrames"
                  class="icon-btn refresh-btn"
                  title="刷新变量列表">
                  <i class="fas fa-sync-alt"></i>
                </button>
              </div>
            </template>
            <div class="file-list">
              <div v-for="name in dataframes" 
                   :key="name" 
                   class="file-item">
                <div class="file-content">
                  <i class="fas fa-table text-blue-500"></i>
                  <span class="file-name">{{ name }}</span>
                </div>
                <div class="file-actions">
                  <button 
                    @click="previewDataFrame(name)"
                    class="icon-btn preview-btn"
                    title="预览变量">
                    <i class="fas fa-eye"></i>
                  </button>
                </div>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>

      <!-- 添加拖动条 -->
      <div class="resize-handle" 
           @mousedown="startResize"
           title="拖动调整宽度">
        <div class="resize-handle-line"></div>
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
                <option value="code">代码单元格</option>
                <option value="markdown">Markdown单元格</option>
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
                  v-if="cellTypes[cellId] === 'code'"
                  @click="() => {
                    const cell = $refs[`codeCell${cellId}`];
                    if (cell && cell[0]) {
                      cell[0].showAiDialog = true;
                    }
                  }" 
                  class="icon-btn ai-btn" 
                  title="AI代码助手"
                >
                  <i class="fas fa-magic"></i>
                </button>
                <button 
                  v-else
                  @click="() => $refs[`markdownCell${cellId}`]?.[0]?.toggleEdit()" 
                  class="icon-btn" 
                  :title="markdownEditStates[cellId] ? '预览' : '编辑'"
                >
                  <i :class="markdownEditStates[cellId] ? 'fas fa-eye' : 'fas fa-edit'"></i>
                </button>
                <button 
                  @click="copyCell(cellId)"
                  class="icon-btn"
                  title="复制内容"
                >
                  <i class="fas fa-copy"></i>
                </button>
                <button 
                  @click="addCellAbove(cellId)"
                  class="icon-btn"
                  title="在上方添加单元格"
                >
                  <i class="fas fa-file-circle-plus" style="transform: rotate(-90deg);"></i>
                </button>
                <button 
                  @click="addCellBelow(cellId)"
                  class="icon-btn"
                  title="在下方添加单元格"
                >
                  <i class="fas fa-file-circle-plus" style="transform: rotate(90deg);"></i>
                </button>
                <button 
                  @click="moveCellUp(cellId)" 
                  class="icon-btn" 
                  title="向上移动"
                  :disabled="cells.indexOf(cellId) === 0"
                >
                  <i class="fas fa-arrow-up"></i>
                </button>
                <button 
                  @click="moveCellDown(cellId)" 
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
              @refresh-dataframes="fetchDataFrameInfo"
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

    <!-- 修改数据导入组件，添加引用和文件属性 -->
    <FileExplore 
      ref="dataImportRef"
      @data-loaded="handleDataLoaded"
      @insert-code="handleCodeInsert"
    />

    <!-- 隐藏的文件输入框 -->
    <input
      type="file"
      ref="fileInput"
      @change="handleFileSelect"
      accept=".csv,.xlsx,.xls"
      style="display: none; visibility: hidden; position: absolute;"
      class="hidden-input"
    />

    <!-- 添加DataFrame预览组件 -->
    <DataFramePreview
      v-model="showDataFramePreview"
      :title="dataFramePreviewTitle"
      :dataframe-name="currentDataframeName"
      ref="dataFramePreview"
    />

    <!-- 添加保存对话框 -->
    <el-dialog
      v-model="saveDialogVisible"
      title="保存笔记本"
      width="30%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <el-form :model="renameForm" label-width="0px">
        <el-form-item>
          <el-input
            v-model="newFileName"
            placeholder="请输入新的文件名"
            @keyup.enter="confirmSave"
          >
            <template #append>.ipynb</template>
          </el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="cancelSave">取消</el-button>
          <el-button type="primary" @click="confirmSave" :loading="saveDialogLoading">确认</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 添加数据文件重命名对话框 -->
    <el-dialog
      v-model="renameDataFileDialogVisible"
      title="重命名数据文件"
      width="30%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <el-form :model="renameDataFileForm" label-width="0px">
        <el-form-item>
          <el-input
            v-model="renameDataFileForm.newName"
            placeholder="请输入新的文件名"
            @keyup.enter="handleDataFileRename"
          >
            <template #append>{{ renameDataFileForm.extension }}</template>
          </el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="renameDataFileDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleDataFileRename">确认</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 添加系统配置对话框组件 -->
    <SystemPromptConfig ref="systemConfigRef" />

    <!-- 添加预定义提示词管理弹窗 -->
    <el-dialog
      v-model="showPromptManager"
      title="管理预定义提示词"
      width="80%"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <PromptPanel mode="manage" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, provide, onUnmounted } from 'vue'
import CodeCell from './components/CodeCell.vue'
import MarkdownCell from './components/MarkdownCell.vue'
import { v4 as uuidv4 } from 'uuid'
import { themes, applyTheme } from './themes'
import { 
  ElMessage, 
  ElDropdown, 
  ElDropdownMenu, 
  ElDropdownItem,
  ElDialog,
  ElButton,
  ElInput,
  ElForm,
  ElFormItem,
  ElAlert,
  ElTooltip
} from 'element-plus'
import FileExplore from './components/DataExplorer/FileExplore.vue'
import DataFramePreview from './components/DataFramePreview.vue'
import SystemPromptConfig from './components/SystemPromptConfig.vue'
import PromptPanel from './components/prompts/PromptPanel.vue'

const cells = ref([])
const currentFile = ref(null)
const cellContents = ref({})
const cellOutputs = ref({})
const cellTypes = ref({})
const markdownEditStates = ref({})
const currentTheme = ref('light')
const version = ref('加载中...')

// 添加笔记本文件列表和数据文件列表
const notebookFiles = ref([])
const dataFiles = ref([])
const currentDataFile = ref(null)

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

// 添加文件上传和处理逻辑
const fileInput = ref(null)
const dataImportRef = ref(null)

// 添加DataFrame相关的状态
const dataframes = ref([])
const dataframeTimer = ref(null)

// DataFrame预览相关的状态
const showDataFramePreview = ref(false)
const dataFramePreviewTitle = ref('')
const dataFramePreview = ref(null)
const currentDataframeName = ref('')

// 保存对话框相关的响应式变量
const saveDialogVisible = ref(false)
const newFileName = ref('')
const saveDialogLoading = ref(false)

// 添加数据文件重命名相关的响应式变量
const renameDataFileDialogVisible = ref(false)
const renameDataFileForm = ref({
  newName: '',
  file: null,
  extension: ''
})

// 在 script setup 部分添加
const activePanels = ref(['notebooks']) // 默认展开笔记本列表
const panelWidth = ref(250) // 初始宽度
const isDragging = ref(false)
const startX = ref(0)
const startWidth = ref(0)

// 添加系统配置相关的引用
const systemConfigRef = ref(null)

// 预定义提示词管理状态
const showPromptManager = ref(false)

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

// 打开保存对话框
const showSaveDialog = () => {
  if (!currentFile.value) {
    newFileName.value = ''
    saveDialogVisible.value = true
  } else {
    handleSaveNotebook()
  }
}

// 处理保存操作
const handleSaveNotebook = async (fileName = '') => {
  try {
    saveDialogLoading.value = true
    
    // 如果提供了新文件名，更新currentFile
    if (fileName) {
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
    ElMessage.success('笔记本保存成功')
    saveDialogVisible.value = false
  } catch (error) {
    ElMessage.error('保存笔记本失败')
    console.error('保存笔记本失败:', error)
  } finally {
    saveDialogLoading.value = false
  }
}

// 取消保存
const cancelSave = () => {
  saveDialogVisible.value = false
  newFileName.value = ''
}

// 确认保存
const confirmSave = () => {
  if (!newFileName.value.trim()) {
    ElMessage.warning('请输入笔记本名称')
    return
  }
  handleSaveNotebook(newFileName.value.trim())
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
  try {
    // 加载笔记本文件
    const notebookResponse = await fetch('http://localhost:8000/list_notebooks')
    const notebookResult = await notebookResponse.json()
    notebookFiles.value = notebookResult || []

    // 加载数据文件
    const dataResponse = await fetch('http://localhost:8000/api/data-files/list')
    const dataResult = await dataResponse.json()
    dataFiles.value = dataResult.files || []
  } catch (error) {
    console.error('加载文件列表失败:', error)
    ElMessage.error('加载文件列表失败')
  }
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

// 修改主题切换处理方法
const handleThemeChange = (themeKey) => {
  currentTheme.value = themeKey
  applyTheme(themeKey)
  ElMessage.success(`已切换到${themes[themeKey].name}`)
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
  fetchDataFrameInfo()
  // 获取版本信息
  await fetchVersion()
  // 每30秒自动刷新一次
  dataframeTimer.value = setInterval(fetchDataFrameInfo, 30000)
})

// 在组件卸载时清理定时器
onUnmounted(() => {
  if (dataframeTimer.value) {
    clearInterval(dataframeTimer.value)
  }
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
})

// 处理数据加载
const handleDataLoaded = (data) => {
  console.log('数据加载成功:', data)
  ElMessage.success('数据加载成功')
}

// 处理代码插入
const handleCodeInsert = (code) => {
  // 获取最后一个单元格
  const lastCellId = cells.value[cells.value.length - 1]
  
  // 检查最后一个单元格是否为代码单元格且内容为空
  if (lastCellId && 
      cellTypes.value[lastCellId] === 'code' && 
      (!cellContents.value[lastCellId] || cellContents.value[lastCellId].trim() === '')) {
    // 如果是空的代码单元格，直接使用它
    cellContents.value[lastCellId] = code
    ElMessage.success('代码已插入到当前单元格')
  } else {
    // 否则创建新的代码单元格
    const newCellId = uuidv4()
    cells.value.push(newCellId)
    cellContents.value[newCellId] = code
    cellTypes.value[newCellId] = 'code'
    cellOutputs.value[newCellId] = {
      output: '',
      plot: '',
      plotly_html: '',
      status: 'idle'
    }
    ElMessage.success('代码已插入到新的单元格')
  }
}

// 获取数据文件图标
const getDataFileIcon = (file) => {
  const ext = file.name.split('.').pop().toLowerCase()
  switch (ext) {
    case 'csv':
      return 'fa-file-csv'
    case 'xlsx':
    case 'xls':
      return 'fa-file-excel'
    default:
      return 'fa-file'
  }
}

// 预览数据文件
const previewDataFile = async (file) => {
  currentDataFile.value = file.path
  if (dataImportRef.value) {
    try {
      // 加载文件数据
      const fileType = file.name.split('.').pop().toLowerCase()
      const endpoint = fileType === 'csv' 
        ? 'http://localhost:8000/api/data-files/preview/csv'
        : 'http://localhost:8000/api/data-files/preview/excel'
      
      const response = await fetch(`${endpoint}?filename=${file.path}`)
      
      if (!response.ok) {
        throw new Error(`加载失败: ${response.status} ${response.statusText}`)
      }
      
      const result = await response.json()
      if (result.status === 'success') {
        // 显示预览对话框
        dataImportRef.value.previewData = result.data
        dataImportRef.value.previewDataFile(file)  // 调用新的预览方法
      } else {
        throw new Error(result.message || '加载失败')
      }
    } catch (error) {
      console.error('加载数据文件失败:', error)
      ElMessage.error('加载数据文件失败: ' + error.message)
    }
  }
}

// 删除数据文件
const deleteDataFile = async (file) => {
  try {
    const response = await fetch(`http://localhost:8000/api/data-files/delete?filename=${file.path}`, {
      method: 'DELETE'
    })
    
    const result = await response.json()
    if (result.status === 'success') {
      if (currentDataFile.value === file.path) {
        currentDataFile.value = null
      }
      await loadFileList()
      ElMessage.success('数据文件删除成功')
    } else {
      ElMessage.error(result.message || '删除失败')
    }
  } catch (error) {
    console.error('删除数据文件失败:', error)
    ElMessage.error('删除数据文件失败: ' + error.message)
  }
}

// 处理文件选择
const handleFileSelect = async (event) => {
  const files = event.target.files
  if (files.length > 0) {
    const file = files[0]
    
    try {
      // 创建 FormData 对象
      const formData = new FormData()
      formData.append('file', file)
      
      // 根据文件类型选择不同的上传端点
      const fileType = file.name.split('.').pop().toLowerCase()
      let endpoint = ''
      
      if (fileType === 'csv') {
        endpoint = 'http://localhost:8000/api/data-files/upload/csv'
      } else if (['xlsx', 'xls'].includes(fileType)) {
        endpoint = 'http://localhost:8000/api/data-files/upload/excel'
      } else {
        throw new Error('不支持的文件格式')
      }
      
      // 上传文件
      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData
      })
      
      if (!response.ok) {
        throw new Error(`上传失败: ${response.status} ${response.statusText}`)
      }
      
      const result = await response.json()
      
      if (result.status === 'success') {
        // 更新文件列表
        await loadFileList()
        ElMessage.success('文件上传成功')
        
        // 更新当前文件
        currentDataFile.value = result.data.file_path
      } else {
        throw new Error(result.message || '上传失败')
      }
    } catch (error) {
      console.error('文件上传失败:', error)
      ElMessage.error('文件上传失败: ' + error.message)
    }
    
    // 清空文件输入框，允许重复上传同一个文件
    event.target.value = ''
  }
}

// 触发文件上传
const triggerFileUpload = () => {
  fileInput.value.click()
}

// 在当前单元格上方添加新单元格
const addCellAbove = (cellId) => {
  const currentIndex = cells.value.indexOf(cellId)
  const newCellId = uuidv4()
  
  // 在当前单元格前插入新单元格
  cells.value.splice(currentIndex, 0, newCellId)
  cellContents.value[newCellId] = ''
  cellTypes.value[newCellId] = 'code'
  cellOutputs.value[newCellId] = {
    output: '',
    plot: '',
    plotly_html: '',
    status: 'idle'
  }
}

// 在当前单元格下方添加新单元格
const addCellBelow = (cellId) => {
  const currentIndex = cells.value.indexOf(cellId)
  const newCellId = uuidv4()
  
  // 在当前单元格后插入新单元格
  cells.value.splice(currentIndex + 1, 0, newCellId)
  cellContents.value[newCellId] = ''
  cellTypes.value[newCellId] = 'code'
  cellOutputs.value[newCellId] = {
    output: '',
    plot: '',
    plotly_html: '',
    status: 'idle'
  }
}

// 添加复制功能
const copyCell = (cellId) => {
  const content = cellContents.value[cellId]
  if (content) {
    navigator.clipboard.writeText(content).then(() => {
      ElMessage.success('内容已复制到剪贴板')
    }).catch(() => {
      ElMessage.error('复制失败')
    })
  }
}

// 获取DataFrame列表
const fetchDataFrameInfo = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/dataframes/list')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    dataframes.value = data
  } catch (error) {
    console.error('获取DataFrame列表失败:', error)
    ElMessage.error('获取DataFrame列表失败: ' + error.message)
  }
}

// 刷新DataFrame列表
const refreshDataFrames = async () => {
  const btn = document.querySelector('.refresh-btn')
  if (btn) {
    btn.classList.add('loading')
  }
  
  try {
    await fetchDataFrameInfo()
    ElMessage.success('DataFrame列表已刷新')
  } catch (error) {
    console.error('刷新DataFrame列表失败:', error)
    ElMessage.error('刷新DataFrame列表失败: ' + error.message)
  } finally {
    if (btn) {
      btn.classList.remove('loading')
    }
  }
}

// 预览DataFrame的方法
const previewDataFrame = async (name) => {
  currentDataframeName.value = name  // 更新当前DataFrame名称
  dataFramePreviewTitle.value = `DataFrame预览: ${name}`
  showDataFramePreview.value = true
}

// 添加重命名数据文件的方法
const renameDataFile = (file) => {
  const extension = '.' + file.name.split('.').pop()
  renameDataFileForm.value = {
    newName: file.name.replace(extension, ''),
    file: file,
    extension: extension
  }
  renameDataFileDialogVisible.value = true
}

// 处理数据文件重命名
const handleDataFileRename = async () => {
  if (!renameDataFileForm.value.newName.trim()) {
    ElMessage.warning('文件名不能为空')
    return
  }
  
  const newFilename = renameDataFileForm.value.newName + renameDataFileForm.value.extension
  
  try {
    const response = await fetch('http://localhost:8000/api/data-files/rename', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        old_filename: renameDataFileForm.value.file.path,
        new_filename: newFilename
      })
    })
    
    const result = await response.json()
    if (result.status === 'success') {
      // 如果当前打开的文件被重命名，更新currentDataFile
      if (currentDataFile.value === renameDataFileForm.value.file.path) {
        currentDataFile.value = newFilename
      }
      // 重新加载文件列表
      await loadFileList()
      renameDataFileDialogVisible.value = false
      ElMessage.success('重命名成功')
    } else {
      ElMessage.error(result.message || '重命名失败')
    }
  } catch (error) {
    console.error('重命名失败:', error)
    ElMessage.error('重命名失败: ' + error.message)
  }
}

// 添加获取版本信息的方法
const fetchVersion = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/version')
    if (!response.ok) {
      throw new Error('获取版本信息失败')
    }
    const result = await response.json()
    if (result.status === 'success') {
      version.value = result.data.version
    } else {
      throw new Error(result.message || '获取版本信息失败')
    }
  } catch (error) {
    console.error('获取版本信息失败:', error)
    version.value = '获取失败'
  }
}

// 刷新数据文件列表
const refreshDataFiles = async () => {
  const btn = document.querySelector('.panel-section:nth-child(2) .refresh-btn')
  if (btn) {
    btn.classList.add('loading')
  }
  
  try {
    await loadFileList()
    ElMessage.success('数据文件列表已刷新')
  } catch (error) {
    console.error('刷新数据文件列表失败:', error)
    ElMessage.error('刷新数据文件列表失败: ' + error.message)
  } finally {
    if (btn) {
      btn.classList.remove('loading')
    }
  }
}

// 开始拖动
const startResize = (e) => {
  isDragging.value = true
  startX.value = e.clientX
  startWidth.value = panelWidth.value
  
  // 添加事件监听
  document.addEventListener('mousemove', handleResize)
  document.addEventListener('mouseup', stopResize)
  
  // 添加禁止选择类
  document.body.classList.add('resizing')
}

// 处理拖动
const handleResize = (e) => {
  if (!isDragging.value) return
  
  const diff = e.clientX - startX.value
  const newWidth = Math.max(200, Math.min(500, startWidth.value + diff)) // 限制最小/最大宽度
  panelWidth.value = newWidth
}

// 停止拖动
const stopResize = () => {
  isDragging.value = false
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
  document.body.classList.remove('resizing')
}

// 刷新笔记本文件列表
const refreshNotebooks = async () => {
  const btn = document.querySelector('.panel-header:first-child .refresh-btn')
  if (btn) {
    btn.classList.add('loading')
  }
  
  try {
    await loadFileList()
    ElMessage.success('笔记本列表已刷新')
  } catch (error) {
    console.error('刷新笔记本列表失败:', error)
    ElMessage.error('刷新笔记本列表失败: ' + error.message)
  } finally {
    if (btn) {
      btn.classList.remove('loading')
    }
  }
}

// 添加显示系统配置的方法
const showSystemConfig = () => {
  systemConfigRef.value?.show()
}
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
  background: #1e88e5;
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
  align-items: center;
  padding: 8px;
  background: transparent;
  gap: 12px;
}

.toolbar-btn {
  background: transparent !important;
  border: none !important;
  color: white !important;
  width: 40px !important;
  height: 40px !important;
  padding: 0 !important;
  border-radius: 50% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.toolbar-btn:hover {
  background: rgba(255, 255, 255, 0.1) !important;
}

.toolbar-btn i {
  font-size: 18px;
  margin: 0;
}

.el-dropdown-menu {
  padding: 5px 0;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.el-dropdown-menu__item {
  padding: 8px 20px;
  font-size: 14px;
  line-height: 1.5;
  display: flex;
  align-items: center;
  gap: 8px;
}

.el-dropdown-menu__item.is-active {
  color: var(--el-color-primary);
  background-color: var(--el-dropdown-menuItem-hover-fill);
}

.el-dropdown-menu__item .fa-check {
  font-size: 12px;
}

.main-container {
  flex: 1;
  display: flex;
  height: calc(100vh - 72px); /* 减去navbar的高度 */
  overflow: hidden;
  position: relative;
}

.file-panel {
  width: 250px;
  background: var(--filePanel);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s ease;
  flex-shrink: 0;
  position: relative;
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
  position: relative;
  overflow: auto;
  padding: 5px;
  background: var(--background);
  transition: background-color 0.3s ease;
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
    padding: 5px;
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
  gap: 4px;
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
  background: var(--cell-background);
  color: var(--text-color);
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
  background-color: var(--cell-background);
  color: var(--text-color);
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
  font-family: 'Fira Code', 'Consolas', 'Monaco', 'Menlo', monospace;
}

.output-text {
  padding: 12px;
  font-family: 'Fira Code', 'Consolas', 'Monaco', 'Menlo', monospace;
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

.icon-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.icon-btn:active:not(:disabled) {
  background: var(--button-active);
}

.icon-btn i {
  font-size: 14px;
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

.hidden-input {
  width: 0;
  height: 0;
  opacity: 0;
  overflow: hidden;
  position: absolute;
  z-index: -1;
}

.upload-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.upload-btn i {
  font-size: 16px;
}

.panel-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  border-bottom: 1px solid var(--border-color);
}

.panel-section:last-child {
  border-bottom: none;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px;
  width: 100%;
}

.panel-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 14px;
  color: #606266;
}

.panel-header h3 i {
  font-size: 16px;
  color: #909399;
}

.file-list {
  max-height: calc(33vh - 48px);
  overflow-y: auto;
  background: var(--el-fill-color-blank);
}

/* 修改折叠面板样式 */
.file-panel :deep(.el-collapse) {
  border: none;
  --el-collapse-header-height: auto;
}

.file-panel :deep(.el-collapse-item__header) {
  padding: 0;
  border: none;
}

.file-panel :deep(.el-collapse-item__content) {
  padding: 0;
  background-color: var(--el-fill-color-blank);
}

.file-panel :deep(.el-collapse-item__wrap) {
  border: none;
}

.file-panel :deep(.el-collapse-item__arrow) {
  margin: 0 8px;
}

.refresh-btn i {
  font-size: 0.9rem;
}

.refresh-btn.loading i {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 添加拖动相关样式 */
.resize-handle {
  width: 8px;
  height: 100%;
  cursor: ew-resize;
  background-color: transparent;
  position: relative;
  transition: background-color 0.2s;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.resize-handle::after {
  content: "⋮";
  color: var(--el-border-color);
  font-size: 20px;
  line-height: 1;
  opacity: 0;
  transition: opacity 0.2s, color 0.2s;
}

.resize-handle:hover::after,
.resizing .resize-handle::after {
  opacity: 1;
  color: var(--el-color-primary);
}

.resize-handle:hover,
.resizing .resize-handle {
  background-color: var(--el-border-color-lighter);
}

/* 拖动时禁止选择文本 */
body.resizing {
  user-select: none;
  cursor: ew-resize !important;
}

/* 移除原来的分隔线样式 */
.resize-handle-line {
  display: none;
}

/* 修改文件面板样式 */
.file-panel {
  min-width: 200px;
  max-width: 500px;
  transition: none; /* 移除宽度动画以实现流畅拖动 */
}
</style>
