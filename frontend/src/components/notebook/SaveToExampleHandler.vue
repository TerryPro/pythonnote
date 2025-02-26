<template>
  <SaveToExampleDialog
    v-model="showSaveDialog"
    :code="currentCellContent"
    @saved="handleExampleSaved"
  />
</template>

<script setup>
import { ref } from 'vue'
import SaveToExampleDialog from '@/components/notebook/SaveToExampleDialog.vue'
import { ElMessage } from 'element-plus'

// 保存示例相关的状态
const showSaveDialog = ref(false)
const currentCellContent = ref('')

// 处理保存到示例库
const handleSaveToExample = (content) => {
  if (!content?.trim()) {
    ElMessage.warning('请先输入代码')
    return
  }
  currentCellContent.value = content
  showSaveDialog.value = true
}

// 处理示例保存成功
const handleExampleSaved = () => {
  ElMessage.success('示例代码保存成功')
  showSaveDialog.value = false
}

// 暴露方法给父组件
defineExpose({
  handleSaveToExample
})
</script>