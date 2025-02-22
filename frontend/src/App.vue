<template>
  <div id="app">
    <AppNavbar 
      ref="navbarRef"
      @show-save-dialog="showSaveDialog"
      @open-example-manager="openExampleManager"
      @update-theme="handleThemeChange"
    />
    <main class="main-container">
      <AppSidebar 
        :panel-width="panelWidth" 
        @insert-code="handleInsertCode"
      >
      </AppSidebar>
      
      <ResizeHandle 
        @resize-start="startResize"
        @resize-move="handleResize"
        @resize-end="stopResize"
      />

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
                  title="运行代码"
                >
                  <i class="fas fa-play"></i>
                </button>
                <button 
                  v-if="cellTypes[cellId] === 'code'"
                  @click="openExampleSelector(cellId)"
                  class="icon-btn"
                  title="代码示例"
                >
                  <i class="fas fa-file-code"></i>
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
                <button 
                  v-if="cellTypes[cellId] === 'code'"
                  @click="() => $refs[`codeCell${cellId}`]?.[0]?.handleSaveToExample()"
                  class="icon-btn"
                  title="保存到示例库"
                >
                  <i class="fas fa-save"></i>
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

    <!-- 添加删除单元格确认对话框组件 -->
    <DeleteCellDialog
      v-model:visible="deleteCellDialogVisible"
      @cancel="deleteCellDialogVisible = false"
      @confirm="handleDeleteCell"
    />

    <!-- 添加保存对话框组件 -->
    <SaveDialog
      v-model:visible="saveDialogVisible"
      :loading="saveDialogLoading"
      @cancel="cancelSave"
      @confirm="handleSaveNotebook"
    />

    <!-- 添加代码示例库对话框 -->
    <CodeExampleDialog
      v-model="showCodeExamples"
      :mode="exampleDialogMode"
      @use-example="handleUseExample"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CodeCell from '@/components/notebook/CodeCell.vue'
import MarkdownCell from '@/components/notebook/MarkdownCell.vue'
import { ElMessage } from 'element-plus'
import { useThemeManager } from '@/composables/useThemeManager'
import { useNotebook } from '@/composables/useNotebook'
import AppNavbar from '@/components/layout/AppNavbar.vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import ResizeHandle from '@/components/layout/ResizeHandle.vue'
import CodeExampleDialog from './components/examples/CodeExampleDialog.vue'
import SaveDialog from '@/components/dialogs/SaveDialog.vue'
import DeleteCellDialog from '@/components/dialogs/DeleteCellDialog.vue'
import { useNotebookStore } from '@/stores/notebookStore'
import { storeToRefs } from 'pinia'
import { v4 as uuidv4 } from 'uuid'

const store = useNotebookStore()
const { cells, cellContents, cellOutputs, cellTypes, markdownEditStates } = storeToRefs(store)
const { addCell, handleExecutionComplete, changeCellType, addCellAbove, addCellBelow, moveCellUp, moveCellDown, deleteCell } = useNotebook()

// 添加代码示例对话框状态
const showCodeExamples = ref(false)
const exampleDialogMode = ref('use')

// 添加删除单元格相关的响应式变量
const deleteCellDialogVisible = ref(false)
const deleteCellId = ref(null)

// 保存对话框相关的响应式变量
const saveDialogVisible = ref(false)
const saveDialogLoading = ref(false)

// 在 script setup 部分添加
const panelWidth = ref(300) // 初始宽度
const isDragging = ref(false)
const startX = ref(0)
const startWidth = ref(300)

// 添加当前单元格引用
const currentCell = ref(null)

// 添加新的主题管理
const { currentTheme, applyTheme, provideTheme } = useThemeManager()
provideTheme() // 为子组件提供主题上下文

// 修改showSaveDialog方法
const showSaveDialog = () => {
  if (!store.currentFile) {
    saveDialogVisible.value = true
  } else {
    handleSaveNotebook()
  }
}

// 修改handleSaveNotebook方法
const handleSaveNotebook = async (fileName = '') => {
  try {
    saveDialogLoading.value = true
    const success = await store.saveNotebook(fileName)
    if (success) {
      saveDialogVisible.value = false
      ElMessage.success('笔记本保存成功')
    } else {
      ElMessage.error('笔记本保存失败')
    }
  } finally {
    saveDialogLoading.value = false
  }
}

// 修改cancelSave方法
const cancelSave = () => {
  saveDialogVisible.value = false
}

// 修改主题切换处理方法
const handleThemeChange = (themeKey) => {
  applyTheme(themeKey)
}

// 确认删除单元格
const confirmDeleteCell = (cellId) => {
  deleteCellId.value = cellId
  deleteCellDialogVisible.value = true
}

// 处理删除单元格
const handleDeleteCell = () => {
  deleteCell(deleteCellId.value)
  deleteCellDialogVisible.value = false
  ElMessage.success('单元格已删除')
}

// 在组件挂载时应用默认主题
const navbarRef = ref(null)

onMounted(async () => {
  await store.fetchNotebooks()
  addCell('code')
  applyTheme(currentTheme.value)
  // 通过组件引用获取版本
  if (navbarRef.value) {
    await navbarRef.value.fetchVersion()
  }
})
// 处理代码插入
const handleInsertCode = (code) => {
  const newCellId = uuidv4()
  if (cells.value.length === 0 || cellContents.value[cells.value[cells.value.length - 1]] !== '') {
    cells.value.push(newCellId)
  } else {
    cellContents.value[cells.value[cells.value.length - 1]] = code
  }
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

// 拖拽开始
const startResize = (e) => {
  isDragging.value = true
  startX.value = e.clientX
  startWidth.value = panelWidth.value
  document.body.classList.add('resizing')
}

// 处理拖拽
const handleResize = (e) => {
  if (!isDragging.value) return
  const newWidth = Math.max(200, Math.min(500, startWidth.value + (e.clientX - startX.value)))
  panelWidth.value = newWidth
}

// 结束拖拽
const stopResize = () => {
  isDragging.value = false
  document.body.classList.remove('resizing')
}

// 处理使用代码示例
const handleUseExample = (code) => {
  const cellId = currentCell.value?.id?.replace('codeCell', '')
  if (cellId && cellTypes.value[cellId] === 'code') {
    // 更新单元格内容
    cellContents.value[cellId] = code
    
    // 获取代码单元格组件实例
    const codeCell = document.querySelector(`#codeCell${cellId}`)
    if (codeCell) {
      // 获取Monaco编辑器实例并更新内容
      const editor = codeCell.__vueParentComponent?.ctx?.editor
      if (editor) {
        editor.setValue(code)
      }
    }
    
    ElMessage.success('代码示例已插入')
    showCodeExamples.value = false
  } else {
    ElMessage.warning('请先选择代码单元格')
  }
}

// 打开代码示例选择器
const openExampleSelector = (cellId) => {
  if (cellTypes.value[cellId] === 'code') {
    const cell = document.querySelector(`#codeCell${cellId}`)
    if (cell) {
      currentCell.value = cell
      exampleDialogMode.value = 'use'
      showCodeExamples.value = true
    }
  }
}

// 打开代码示例管理器
const openExampleManager = () => {
  exampleDialogMode.value = 'manage'
  showCodeExamples.value = true
}
</script>

<style lang="scss">

.main-container {
  flex: 1;
  display: flex;
  height: calc(100vh - 72px); /* 减去navbar的高度 */
  overflow: hidden;
  position: relative;
}

.content-area {
  flex-grow: 1; /* 使内容区域占据剩余空间 */
  border: 1px solid #ccc;
  height: calc(100vh - 74px); /* 减去navbar的高度 */
  width: 100%;
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

.hidden-input {
  width: 0;
  height: 0;
  opacity: 0;
  overflow: hidden;
  position: absolute;
  z-index: -1;
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

</style>
