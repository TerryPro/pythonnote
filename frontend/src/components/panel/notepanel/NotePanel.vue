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
          <i class="fas fa-folder-open mr-2"></i>打开
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
        @click="openNotebookInTab(file)"
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
      extension=".ipynb"
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
import RenameDialog from '@/components/common/RenameDialog.vue'
import DeleteDialog from '@/components/common/DeleteDialog.vue'
import { useNotebook } from '@/composables/useNotebook'
import { useTabsStore } from '@/stores/tabsStore'
import { useLoadingStore } from '@/stores/loadingStore'
import { useNotebookStore } from '@/stores/notebookStore'
import { useNoteDelete } from './useNoteDelete'
import { useNoteRename } from './useNoteRename'

const store = useNotebookStore()
const tabsStore = useTabsStore()
const loadingStore = useLoadingStore()

// 使用重命名笔记本的组合式API
const { renameDialogVisible, renameForm, showRenameDialog, handleRename } = useNoteRename()

// 使用删除笔记本的组合式API
const { deleteDialogVisible, deleteFile, showDeleteDialog, handleDelete } = useNoteDelete()

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

// 打开笔记本到新标签页
const openNotebookInTab = async (file) => {
  try {

    loadingStore.startLoading('正在加载 Notebook...')

    // 在新标签页中打开笔记本
    const tabId = await useNotebook().openNotebook(file)
    
    // 激活新创建的标签页
    if (tabId) {
      tabsStore.activateTab(tabId)
    }

  } catch (error) {
    console.error('打开笔记本失败:', error)
    ElMessage.error('打开笔记本失败: ' + error.message)
  } finally {
    loadingStore.endLoading()
  }
}

// 处理右键菜单操作
const handleContextMenuAction = (action) => {
  const file = contextMenu.value.selectedFile;
  if (!file) return;

  switch (action) {
    case 'open':
      openNotebookInTab(file);
      break;
    case 'rename':
      showRenameDialog(file);
      break;
    case 'delete':
      showDeleteDialog(file);
      break;
  }
  closeContextMenu();
};

// 关闭右键菜单
const closeContextMenu = () => {
  contextMenu.value.visible = false;
  document.removeEventListener('click', closeContextMenu);
};

</script>

<style scoped lang="scss">
</style>