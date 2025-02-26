<template>
  <div>
    <div class="list-toolbar">
      <el-button @click="handleRefresh" class="refresh-btn icon-btn">
        <i class="fas fa-sync-alt" :class="{ 'fa-spin': store.loading }"></i>
      </el-button>
      <el-button @click="showFileUploadDialog" class="upload-btn icon-btn">
        <i class="fas fa-upload"></i>
      </el-button>
    </div>
    
    <div class="file-list">
      <!-- 右键菜单 -->
      <div 
        v-show="contextMenu.visible"
        class="context-menu"
        :style="{ left: contextMenu.x + 'px', top: contextMenu.y + 'px' }"
      >
        <div class="menu-item" @click="handleContextMenuAction('preview')">
          <i class="fas fa-eye mr-2"></i>预览数据
        </div>
        <div class="menu-item" @click="handleContextMenuAction('rename')">
          <i class="fas fa-edit mr-2"></i>重命名
        </div>
        <div class="menu-item delete" @click="handleContextMenuAction('delete')">
          <i class="fas fa-trash mr-2"></i>删除
        </div>
      </div>

      <div 
        v-for="file in store.files" 
        :key="file.path" 
        class="file-item"
        :class="{ active: store.currentFile === file.path }"
        @contextmenu.prevent="showContextMenu($event, file)"
      >
        <div class="file-content" @click="handlePreview(file)">
          <i :class="['fas', getFileIcon(file)]"></i>
          <span class="file-name">{{ file.name }}</span>
        </div>
      </div>
    </div>

    <!-- 隐藏的文件输入框 -->
    <input
      type="file"
      ref="fileInput"
      @change="handleFileUpload"
      accept=".csv,.xlsx,.xls"
      style="display: none"
    />

    <!-- 重命名对话框 -->
    <RenameDialog
      v-model:visible="renameDialogVisible"
      :current-name="renameForm.file?.name || ''"
      :extension="renameForm.extension"
      @confirm="handleRename"
      @cancel="renameDialogVisible = false"
    />

    <!-- 添加数据预览组件 -->
    <FileExplore ref="dataImportRef"/>

    <!-- 删除确认对话框 -->
    <DeleteDialog
      v-model:visible="deleteDialogVisible"
      :file-name="deleteFile?.name || ''"
      @confirm="handleDelete"
      @cancel="deleteDialogVisible = false"
    />
  </div>
</template>
Data
<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useDataFileStore } from '@/stores/dataFileStore'
import FileExplore from '@/components/panel/filepanel/FileExplore.vue'
import RenameDialog from '@/components/common/RenameDialog.vue'
import DeleteDialog from '@/components/common/DeleteDialog.vue'
import { useFileDelete } from './useFileDelete'
import { useFileRename } from './useFileRename'

const store = useDataFileStore()
const fileInput = ref(null)
const dataImportRef = ref(null)

const { renameDialogVisible, renameForm, showRenameDialog, handleRename } = useFileRename(store)
const { deleteDialogVisible, deleteFile, showDeleteDialog, handleDelete } = useFileDelete(store)

// 添加右键菜单状态
const contextMenu = ref({
  visible: false,
  x: 0,
  y: 0,
  selectedFile: null
});

// 初始化加载文件列表
onMounted(async () => {
  await store.loadFiles()
})

// 刷新文件列表
const handleRefresh = async () => {
  try {
    await store.loadFiles()
    ElMessage.success('文件列表已刷新')
  } catch (error) {
    ElMessage.error(error.message)
  }
}

// 触发文件选择对话框
const showFileUploadDialog = () => {
  fileInput.value.click()
}

// 处理文件上传
const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  try {
    await store.uploadFile(file)
    ElMessage.success('文件上传成功')
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    event.target.value = ''
  }
}



// 预览文件
const handlePreview = async (file) => {
  try {
    store.currentFile = file.path
    await store.previewFile(file.path)
    dataImportRef.value.previewDataFile()
  } catch (error) {
    ElMessage.error(error.message)
  }
}

// 文件图标获取
const getFileIcon = (file) => {
  const ext = file.name.split('.').pop().toLowerCase()
  return ext === 'csv' ? 'fa-file-csv' : 'fa-file-excel'
}

// 显示右键菜单
const showContextMenu = (event, file) => {
  contextMenu.value = {
    visible: true,
    x: event.clientX,
    y: event.clientY,
    selectedFile: file
  };
  document.addEventListener('click', closeContextMenu);
};

// 处理右键菜单操作
const handleContextMenuAction = (action) => {
  const file = contextMenu.value.selectedFile;
  if (!file) return;

  switch (action) {
    case 'preview':
      handlePreview(file);
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