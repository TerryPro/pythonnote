<template>
  <SaveDialog
    v-model:visible="saveDialogVisible"
    :loading="saveDialogLoading"
    @cancel="cancelSave"
    @confirm="handleSaveNotebook"
  />
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import SaveDialog from '@/components/notebook/SaveDialog.vue'
import { useTabsStore } from '@/stores/tabsStore'
import { useNotebook } from '@/composables/useNotebook'

const tabsStore = useTabsStore()
const { saveNotebook } = useNotebook()

// 获取当前活动标签页
const activeTab = computed(() => tabsStore.activeTab)

// 保存对话框相关的响应式变量
const saveDialogVisible = ref(false)
const saveDialogLoading = ref(false)

// 显示保存对话框
const showSaveDialog = () => {
  if (activeTab.value && activeTab.value.notebookFile) {
    handleSaveNotebook()
  } else {
    saveDialogVisible.value = true
  }
}

// 处理保存笔记本
const handleSaveNotebook = async (fileName = '') => {
  try {
    saveDialogLoading.value = true
    const success = await saveNotebook(fileName)
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

// 取消保存
const cancelSave = () => {
  saveDialogVisible.value = false
}

// 暴露方法给父组件
defineExpose({
  showSaveDialog
})
</script>