import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { deleteNotebook } from '@/api/notebook_api'
import { useNotebookStore } from '@/stores/notebookStore'
import { useNotebook } from '@/composables/useNotebook'
import { useTabsStore } from '@/stores/tabsStore'

export function useNoteDelete() {
  const store = useNotebookStore()
  const tabsStore = useTabsStore()
  const { closeNotebook } = useNotebook()

  // 删除相关的响应式变量
  const deleteDialogVisible = ref(false)
  const deleteFile = ref(null)

  // 显示删除确认对话框
  const showDeleteDialog = (file) => {
    deleteFile.value = file
    deleteDialogVisible.value = true
  }

  // 处理删除
  const handleDelete = async () => {
    try {
      const result = await deleteNotebook(deleteFile.value.path)
      
      if (result.status === 'success') {
        const tab = tabsStore.tabs.find(tab => tab.notebookFile === deleteFile.value.path)
        if (tab) {
          closeNotebook(tab.id)
        }

        // 重新加载文件列表
        await store.fetchNotebooks()
        deleteDialogVisible.value = false
        ElMessage.success(result.message)
      } else {
        ElMessage.error(result.message || '删除失败')
      }
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败: ' + error.message)
    }
  }

  // 取消删除
  const cancelDelete = () => {
    deleteDialogVisible.value = false
  }

  return {
    deleteDialogVisible,
    deleteFile,
    showDeleteDialog,
    handleDelete,
    cancelDelete
  }
}