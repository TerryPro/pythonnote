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
  <!-- 添加删除单元格处理组件 -->
  <DeleteCellHandler ref="deleteCellHandler"/>
  <!-- 添加代码示例使用组件 -->
  <CodeExampleUse ref="codeExampleUse"/>
</template>

<script setup>
import { ref } from 'vue'
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
</script>

<style lang="scss" scoped>
</style>