<template>
  <CodeExampleDialog
    v-model="showCodeExamples"
    :mode="exampleDialogMode"
    @use-example="handleUseExample"
  />
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import CodeExampleDialog from './CodeExampleDialog.vue'
import { useNotebookStore } from '@/stores/notebookStore'
import { storeToRefs } from 'pinia'

const store = useNotebookStore()
const { cellTypes, cellContents } = storeToRefs(store)

// 代码示例对话框状态
const showCodeExamples = ref(false)
const exampleDialogMode = ref('use')

// 当前单元格引用
const currentCell = ref(null)

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

defineExpose({
  openExampleSelector
})
</script>