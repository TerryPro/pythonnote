import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { api_renameNotebook } from '@/api/notebook_api'
import { useNotebookStore } from '@/stores/notebookStore'
import { useTabsStore } from '@/stores/tabsStore'

export function useNoteRename() {
  const store = useNotebookStore()
  const tabsStore = useTabsStore()
  
  // 重命名相关的响应式变量
  const renameDialogVisible = ref(false)
  const renameForm = ref({
    newName: '',
    file: null
  })

  // 显示重命名对话框
  const showRenameDialog = (file) => {
    renameForm.value.newName = file.name.replace('.ipynb', '')
    renameForm.value.file = file
    renameDialogVisible.value = true
  }

  // 处理重命名确认
  const handleRename = async (newName) => {
    if (!newName.trim()) {
      ElMessage.warning('文件名不能为空')
      return
    }
    
    const newFilename = newName.endsWith('.ipynb') 
      ? newName 
      : `${newName}.ipynb`
    
    try {
      const result = await api_renameNotebook(renameForm.value.file.path, newFilename)
      
      if (result.status === 'success') {
        // 更新标签页中的文件名
        const tab = tabsStore.tabs.find(tab => tab.notebookFile === renameForm.value.file.path)
        if (tab) {
          tab.notebookFile = newFilename
          tab.title = newFilename
        }
        
        // 重新加载文件列表
        await store.fetchNotebooks()
        renameDialogVisible.value = false
        ElMessage.success('重命名成功')
      } else {
        ElMessage.error(result.message || '重命名失败')
      }
    } catch (error) {
      console.error('重命名失败:', error)
      ElMessage.error('重命名失败: ' + error.message)
    }
  }

  return {
    renameDialogVisible,
    renameForm,
    showRenameDialog,
    handleRename
  }
}