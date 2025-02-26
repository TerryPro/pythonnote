<template>
  <div class="notebook" v-if="cells.length">
    <div class="notebook-cells">
      <div v-for="cellId in cells" :key="cellId" class="cell-wrapper">
        <CellToolsBar
          :type="cellTypes[cellId]"
          :is-editing="markdownEditStates[cellId]"
          :is-first="cells.indexOf(cellId) === 0"
          :is-last="cells.indexOf(cellId) === cells.length - 1"
          @update:type="(v) => changeCellType(cellId, v)"
          @execute="$refs[`codeCell${cellId}`]?.[0]?.executeCode(session_id)"
          @open-example="openExampleSelector(cellId)"
          @open-ai-dialog="openAiDialog(cellId)"
          @toggle-edit="$refs[`markdownCell${cellId}`]?.[0]?.toggleEdit()"
          @copy="copyCell(cellId)"
          @add-above="addCellAbove(cellId)"
          @add-below="addCellBelow(cellId)"
          @move-up="moveCellUp(cellId)"
          @move-down="moveCellDown(cellId)"
          @delete="confirmDeleteCell(cellId)"
          @save-to-example="handleSaveToExample(cellId)"
        />
        <CodeCell
          v-if="cellTypes[cellId] === 'code'"
          :ref="`codeCell${cellId}`"
          :cell-id="cellId"
          :content="cellContents[cellId]"
          :output-content="cellOutputs[cellId]"
          :dataframe-info="dataframeInfo"
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
  <!-- 添加删除单元格处理组件 -->
  <DeleteCellHandler ref="deleteCellHandler"/>
  <!-- 添加代码示例使用组件 -->
  <CodeExampleUse ref="codeExampleUse"/>
  <!-- 添加保存示例处理组件 -->
  <SaveToExampleHandler ref="saveToExampleHandler"/>
  <!-- AI对话框组件 -->
  <AiDialog
    v-model="showAiDialog"
    :dataframe-info="dataframeInfo"
    @code-generated="handleCodeGenerated"
  />
</template>

<script setup>
import { ref } from 'vue'
import CellToolsBar from '@/components/notebook/CellToolsBar.vue'
import CodeCell from '@/components/notebook/CodeCell.vue'
import MarkdownCell from '@/components/notebook/MarkdownCell.vue'
import { useNotebook } from '@/composables/useNotebook'
import CodeExampleUse from '../examples/CodeExampleUse.vue'
import DeleteCellHandler from '@/components/notebook/DeleteCellHandler.vue'
import SaveToExampleHandler from '@/components/notebook/SaveToExampleHandler.vue'
import AiDialog from '@/components/ai/AiDialog.vue'
import { useNotebookStore } from '@/stores/notebookStore'

import { storeToRefs } from 'pinia'

const store = useNotebookStore()

const { session_id, cells, cellContents, cellOutputs, cellTypes, markdownEditStates } = storeToRefs(store)
const { handleExecutionComplete, changeCellType, addCellAbove, addCellBelow, moveCellDown, moveCellUp, copyCell } = useNotebook()

// 添加组件引用
const deleteCellHandler = ref(null)
const codeExampleUse = ref(null)
const saveToExampleHandler = ref(null)

// AI对话框状态
const showAiDialog = ref(false)
const currentCellId = ref(null)
const dataframeInfo = ref({})

// 确认删除单元格
const confirmDeleteCell = (cellId) => {
  deleteCellHandler.value?.confirmDeleteCell(cellId)
}

// 打开代码示例选择器
const openExampleSelector = (cellId) => {
  codeExampleUse.value?.openExampleSelector(cellId)
}

// 打开AI对话框
const openAiDialog = (cellId) => {
  currentCellId.value = cellId
  showAiDialog.value = true
}

// 处理AI生成的代码
const handleCodeGenerated = (code) => {
  if (currentCellId.value) {
    cellContents.value[currentCellId.value] = code
  }
}

// 处理保存到示例库
const handleSaveToExample = (cellId) => {
  const content = cellContents.value[cellId]
  saveToExampleHandler.value?.handleSaveToExample(content)
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
</style>