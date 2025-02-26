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
          @execute="$refs[`codeCell${cellId}`]?.[0]?.executeCode(props.sessionId)"
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
import { ref, watch, defineProps, defineEmits } from 'vue'
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

const props = defineProps({
  sessionId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['modified'])

const store = useNotebookStore()

const { cells, cellContents, cellOutputs, cellTypes, markdownEditStates } = storeToRefs(store)
const { handleExecutionComplete, changeCellType, addCellAbove, addCellBelow, moveCellDown, moveCellUp, copyCell } = useNotebook()

// 添加组件引用
const deleteCellHandler = ref(null)
const codeExampleUse = ref(null)
const saveToExampleHandler = ref(null)

// AI对话框状态
const showAiDialog = ref(false)
const currentCellId = ref(null)
const dataframeInfo = ref({})

// 监听session_id变化
watch(() => props.sessionId, (newSessionId) => {
  if (newSessionId) {
    store.SetSessionId(newSessionId)
  }
}, { immediate: true })

// 监听笔记本内容变化，发出modified事件
watch([cellContents, cellTypes], () => {
  emit('modified')
}, { deep: true })

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
@use '@/styles/layout/_notebook.scss'
</style>