<template>
  <!-- 代码示例库对话框 -->
  <CodeExampleDialog
    v-model="showCodeExamples"
    :mode="exampleDialogMode"
  />
</template>

<script setup>
import { ref } from 'vue'
import CodeExampleDialog from './CodeExampleDialog.vue'

const showCodeExamples = ref(false)
const exampleDialogMode = ref('manage')

const openExampleManager = () => {
  exampleDialogMode.value = 'manage'
  showCodeExamples.value = true
}

// 暴露方法给父组件
defineExpose({
  openExampleManager
})
</script>