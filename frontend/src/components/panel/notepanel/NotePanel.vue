<template>
  <div>
    <!-- 工具栏 -->
    <div class="list-toolbar">
      <el-button @click="refreshNotebooks" class="refresh-btn icon-btn">
        <i class="fas fa-sync-alt"></i>
      </el-button>
    </div>
    
    <!-- 文件列表 -->
    <div class="file-list">
      <!-- 右键菜单 -->
      <div 
        v-show="contextMenu.visible"
        class="context-menu"
        :style="{ left: contextMenu.x + 'px', top: contextMenu.y + 'px' }"
      >
        <div class="menu-item" @click="handleContextMenuAction('open')">
          <i class="fas fa-folder-open mr-2"></i>打开笔记
        </div>
        <div class="menu-item" @click="handleContextMenuAction('rename')">
          <i class="fas fa-edit mr-2"></i>重命名
        </div>
        <div class="menu-item delete" @click="handleContextMenuAction('delete')">
          <i class="fas fa-trash mr-2"></i>删除
        </div>
      </div>

      <div 
        v-for="file in store.notebookFiles" 
        :key="file.path" 
        class="file-item"
        :class="{ active: store.currentFile === file.path }"
        @contextmenu.prevent="showContextMenu($event, file)"
        @click="openNotebook(file)"
      >
        <div class="file-content">
          <i class="fas fa-file-code"></i>
          <span class="file-name">{{ file.name }}</span>
        </div>
      </div>
    </div>

    <!-- 重命名对话框组件 -->
    <RenameDialog
      v-model:visible="renameDialogVisible"
      :current-name="renameForm.file?.name || ''"
      @cancel="renameDialogVisible = false"
      @confirm="handleRename"
    />

    <!-- 删除确认对话框组件 -->
    <DeleteDialog
      v-model:visible="deleteDialogVisible"
      :file-name="deleteFile?.name || ''"
      @cancel="deleteDialogVisible = false"
      @confirm="handleDelete"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useNotebookStore } from '@/stores/notebookStore'
import RenameDialog from '@/components/panel/notepanel/RenameDialog.vue'
import DeleteDialog from '@/components/panel/notepanel/DeleteDialog.vue'
import { api_renameNotebook } from '@/api/notebook_api'
import { deleteNotebook } from '@/api/notebook_api'
import { useNotebook } from '@/composables/useNotebook'

const store = useNotebookStore()
const { openNotebook, createNewNotebook } = useNotebook()

// 重命名相关的响应式变量
const renameDialogVisible = ref(false)
const renameForm = ref({
  newName: '',
  file: null
})

// 删除相关的响应式变量
const deleteDialogVisible = ref(false)
const deleteFile = ref(null)

// 刷新笔记本文件列表
const refreshNotebooks = async () => {
  const btn = document.querySelector('.refresh-btn')
  if (btn) {
    btn.classList.add('loading')
  }
  
  try {
    await store.fetchNotebooks()
    ElMessage.success('笔记本列表已刷新')
  } catch (error) {
    console.error('刷新笔记本列表失败:', error)
    ElMessage.error('刷新笔记本列表失败: ' + error.message)
  } finally {
    if (btn) {
      btn.classList.remove('loading')
    }
  }
}

// 添加右键菜单状态
const contextMenu = ref({
  visible: false,
  x: 0,
  y: 0,
  selectedFile: null
});

// 显示右键菜单
const showContextMenu = (event, file) => {
  event.stopPropagation(); // 防止触发点击事件
  contextMenu.value = {
    visible: true,
    x: event.clientX,
    y: event.clientY,
    selectedFile: file
  };
  document.addEventListener('click', closeContextMenu);
};

// 处理删除
const handleDelete = async () => {
  try {
    const result = await deleteNotebook(deleteFile.value.path)
    
    if (result.status === 'success') {
      // 如果删除的是当前打开的文件，创建新笔记本
      if (store.currentFile === deleteFile.value.path) {
        createNewNotebook()
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

// 处理右键菜单操作
const handleContextMenuAction =  (action) => {
  const file = contextMenu.value.selectedFile;
  if (!file) return;

  switch (action) {
    case 'open':
      openNotebook(file);
      break;
    case 'rename':
      renameNotebook(file);
      break;
    case 'delete':
      deleteFile.value = file;
      deleteDialogVisible.value = true;
      break;
  }
  closeContextMenu();
};

// 关闭右键菜单
const closeContextMenu = () => {
  contextMenu.value.visible = false;
  document.removeEventListener('click', closeContextMenu);
};

// 重命名笔记本
const renameNotebook = (file) => {
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
      // 如果当前打开的文件被重命名，更新currentFile
      if (store.currentFile === renameForm.value.file.path) {
        store.currentFile = newFilename
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
</script>

<style scoped lang="scss">
</style>