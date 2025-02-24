<template>
  <div class="delete-cell-handler">
    <!-- 删除单元格确认对话框组件 -->
    <DeleteCellDialog
      v-model:visible="deleteCellDialogVisible"
      @cancel="deleteCellDialogVisible = false"
      @confirm="handleDeleteCell"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DeleteCellDialog from '@/components/dialogs/DeleteCellDialog.vue'
import { ElMessage } from 'element-plus'
import { useNotebook } from '@/composables/useNotebook'

const { deleteCell} = useNotebook()

// 删除单元格相关的响应式变量
const deleteCellDialogVisible = ref(false)
const deleteCellId = ref(null)

// 确认删除单元格
const confirmDeleteCell = (cellId) => {
  deleteCellId.value = cellId
  deleteCellDialogVisible.value = true
}

// 处理删除单元格
const handleDeleteCell = () => {
  if (deleteCell(deleteCellId.value)) {
    ElMessage.success('单元格已删除')
  }
  deleteCellDialogVisible.value = false
}

// 对外暴露方法
defineExpose({
  confirmDeleteCell
})
</script>
