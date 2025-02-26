import { ref } from 'vue'
import { ElMessage } from 'element-plus'

export function useFileRename(store) {
  const renameDialogVisible = ref(false)
  const renameForm = ref({
    file: null,
    extension: ''
  })

  // 显示重命名对话框
  const showRenameDialog = (file) => {
    const extension = '.' + file.name.split('.').pop()
    renameForm.value = {
      file: file,
      extension: extension
    }
    renameDialogVisible.value = true
  }

  // 执行重命名
  const handleRename = async (newName) => {
    try {
      await store.renameFile(
        renameForm.value.file.path, 
        newName
      )
      ElMessage.success('重命名成功')
      renameDialogVisible.value = false
    } catch (error) {
      ElMessage.error(error.message)
    }
  }

  return {
    renameDialogVisible,
    renameForm,
    showRenameDialog,
    handleRename
  }
}