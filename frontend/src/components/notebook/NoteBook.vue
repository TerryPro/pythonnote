<template>
  <div class="notebook" v-if="cells.length">
    <div class="notebook-cells">
      <div v-for="cellId in cells" :key="cellId" class="cell-wrapper">
        <CellHeader
          :type="cellTypes[cellId]"
          :is-editing="markdownEditStates[cellId]"
          :is-first="cells.indexOf(cellId) === 0"
          :is-last="cells.indexOf(cellId) === cells.length - 1"
          @update:type="(v) => changeCellType(cellId, v)"
          @execute="$refs[`codeCell${cellId}`]?.[0]?.executeCode()"
          @open-example="openExampleSelector(cellId)"
          @open-ai-dialog="openAiDialog($refs[`codeCell${cellId}`])"
          @toggle-edit="$refs[`markdownCell${cellId}`]?.[0]?.toggleEdit()"
          @copy="copyCell(cellId)"
          @add-above="addCellAbove(cellId)"
          @add-below="addCellBelow(cellId)"
          @move-up="moveCellUp(cellId)"
          @move-down="moveCellDown(cellId)"
          @delete="confirmDeleteCell(cellId)"
          @save-to-example="$refs[`codeCell${cellId}`]?.[0]?.handleSaveToExample()"
        />
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
  <!-- 添加删除单元格处理组件 -->
  <DeleteCellHandler ref="deleteCellHandler"/>
  <!-- 添加代码示例使用组件 -->
  <CodeExampleUse ref="codeExampleUse"/>
</template>

<script setup>
import { ref } from 'vue'
import CellHeader from '@/components/notebook/CellHeader.vue'
import CodeCell from '@/components/notebook/CodeCell.vue'
import MarkdownCell from '@/components/notebook/MarkdownCell.vue'
import { useNotebook } from '@/composables/useNotebook'
import CodeExampleUse from '../examples/CodeExampleUse.vue'
import DeleteCellHandler from '@/components/notebook/DeleteCellHandler.vue'
import { useNotebookStore } from '@/stores/notebookStore'
import { storeToRefs } from 'pinia'

const store = useNotebookStore()
const { cells, cellContents, cellOutputs, cellTypes, markdownEditStates } = storeToRefs(store)
const { handleExecutionComplete, changeCellType, addCellAbove, addCellBelow, moveCellDown, moveCellUp, copyCell } = useNotebook()

// 添加删除单元格处理组件引用
const deleteCellHandler = ref(null)
const codeExampleUse = ref(null)
// 确认删除单元格
const confirmDeleteCell = (cellId) => {
  deleteCellHandler.value?.confirmDeleteCell(cellId)
}

// 打开代码示例选择器
const openExampleSelector = (cellId) => {
  codeExampleUse.value?.openExampleSelector(cellId)
}

// 打开AI对话框
const openAiDialog = (cell) => {
  console.log(cell)
  if (cell && cell[0]) {
    cell[0].showAiDialog = true
  }
}
</script>

<style lang="scss" scoped>
</style>