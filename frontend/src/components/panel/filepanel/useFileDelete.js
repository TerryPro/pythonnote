import { ref } from 'vue'
import { ElMessage } from 'element-plus'

export function useFileDelete(store) {
  const deleteDialogVisible = ref(false)
  const deleteFile = ref(null)

  // 显示删除确认对话框
  const showDeleteDialog = (file) => {
    deleteFile.value = file
    deleteDialogVisible.value = true
  }

  // 删除文件
  const handleDelete = async () => {
    if (!deleteFile.value) return
    
    try {
      await store.deleteFile(deleteFile.value.path)
      ElMessage.success('文件删除成功')
      deleteDialogVisible.value = false
    } catch (error) {
      ElMessage.error(error.message)
    }
  }

  return {
    deleteDialogVisible,
    deleteFile,
    showDeleteDialog,
    handleDelete
  }
}