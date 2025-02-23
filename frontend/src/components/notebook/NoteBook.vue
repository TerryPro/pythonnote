<template>
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

  <!-- 添加删除单元格确认对话框组件 -->
  <DeleteCellDialog
    v-model:visible="deleteCellDialogVisible"
    @cancel="deleteCellDialogVisible = false"
    @confirm="handleDeleteCell"
  />

  <!-- 添加代码示例库对话框 -->
  <CodeExampleDialog
    v-model="showCodeExamples"
    :mode="exampleDialogMode"
    @use-example="handleUseExample"
  />
</template>

<script setup>
import { ref } from 'vue'
import CodeCell from '@/components/notebook/CodeCell.vue'
import MarkdownCell from '@/components/notebook/MarkdownCell.vue'
import { ElMessage } from 'element-plus'
import { useNotebook } from '@/composables/useNotebook'
import CodeExampleDialog from '../examples/CodeExampleDialog.vue'
import DeleteCellDialog from '@/components/dialogs/DeleteCellDialog.vue'
import { useNotebookStore } from '@/stores/notebookStore'
import { storeToRefs } from 'pinia'
import { v4 as uuidv4 } from 'uuid'

const store = useNotebookStore()
const { cells, cellContents, cellOutputs, cellTypes, markdownEditStates } = storeToRefs(store)
const { addCell, handleExecutionComplete, changeCellType, moveCellDown, moveCellUp } = useNotebook()

// 添加代码示例对话框状态
const showCodeExamples = ref(false)
const exampleDialogMode = ref('use')

// 添加删除单元格相关的响应式变量
const deleteCellDialogVisible = ref(false)
const deleteCellId = ref(null)

// 添加当前单元格引用
const currentCell = ref(null)

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
</script>

<style lang="scss" scoped>
.notebook {
  flex: 1;
  position: relative;
  overflow: auto;
  padding: 2px;
  background: var(--background);
  transition: background-color 0.3s ease;
}

.notebook-cells {
  padding: 0 4px;
  height: 100%;
  overflow-y: auto;
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

.cell-actions {
  display: flex;
  gap: 4px;
}

.delete-btn {
  color: #f56c6c;
}

.delete-btn:hover {
  background: #fef0f0;
  border-color: #f56c6c;
  color: #f56c6c;
}
</style> 