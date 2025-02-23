<template>
  <div id="app">
    <AppNavbar 
      ref="navbarRef"
      @show-save-dialog="showSaveDialog"
      @open-example-manager="openExampleManager"
      @update-theme="handleThemeChange"
    />

    <main class="main-container">
      <AppSidebar/>
      <ResizeHandle />
      <NoteBook />
    </main>

    <!-- 添加保存对话框组件 -->
    <SaveDialog
      v-model:visible="saveDialogVisible"
      :loading="saveDialogLoading"
      @cancel="cancelSave"
      @confirm="handleSaveNotebook"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useThemeManager } from '@/composables/useThemeManager'
import AppNavbar from '@/components/layout/AppNavbar.vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import ResizeHandle from '@/components/layout/ResizeHandle.vue'
import NoteBook from '@/components/notebook/NoteBook.vue'
import SaveDialog from '@/components/dialogs/SaveDialog.vue'
import { useNotebookStore } from '@/stores/notebookStore'
import { useNotebook } from '@/composables/useNotebook'

const store = useNotebookStore()
const { createNewNotebook } = useNotebook()

// 保存对话框相关的响应式变量
const saveDialogVisible = ref(false)
const saveDialogLoading = ref(false)

// 添加新的主题管理
const { currentTheme, applyTheme, provideTheme } = useThemeManager()
provideTheme() // 为子组件提供主题上下文

// 修改showSaveDialog方法
const showSaveDialog = () => {
  if (!store.currentFile) {
    saveDialogVisible.value = true
  } else {
    handleSaveNotebook()
  }
}

// 修改handleSaveNotebook方法
const handleSaveNotebook = async (fileName = '') => {
  try {
    saveDialogLoading.value = true
    const success = await store.saveNotebook(fileName)
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

// 修改cancelSave方法
const cancelSave = () => {
  saveDialogVisible.value = false
}

// 修改主题切换处理方法
const handleThemeChange = (themeKey) => {
  applyTheme(themeKey)
}

// 打开代码示例管理器
const openExampleManager = () => {
  const notebook = document.querySelector('.notebook')
  if (notebook) {
    notebook.__vueParentComponent?.ctx?.openExampleManager()
  }
}

// 在组件挂载时应用默认主题
const navbarRef = ref(null)

onMounted(async () => {
  await store.fetchNotebooks()
  createNewNotebook()
  applyTheme(currentTheme.value)
  // 通过组件引用获取版本
  if (navbarRef.value) {
    await navbarRef.value.fetchVersion()
  }
})
</script>

<style lang="scss">
@import '@/styles/layout/_navbar.scss';
@import '@/styles/layout/_sidebar.scss';
@import '@/styles/base/_base.scss';

.main-container {
  flex: 1;
  display: flex;
  height: calc(100vh - 72px); /* 减去navbar的高度 */
  overflow: hidden;
  position: relative;
}

.content-area {
  flex-grow: 1; /* 使内容区域占据剩余空间 */
  border: 1px solid #ccc;
  height: calc(100vh - 74px); /* 减去navbar的高度 */
  width: 100%;
}

/* 添加拖动相关样式 */
.resize-handle {
  width: 8px;
  height: 100%;
  cursor: ew-resize;
  background-color: transparent;
  position: relative;
  transition: background-color 0.2s;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.resize-handle::after {
  content: "⋮";
  color: var(--el-border-color);
  font-size: 20px;
  line-height: 1;
  opacity: 0;
  transition: opacity 0.2s, color 0.2s;
}

.resize-handle:hover::after,
.resizing .resize-handle::after {
  opacity: 1;
  color: var(--el-color-primary);
}

.resize-handle:hover,
.resizing .resize-handle {
  background-color: var(--el-border-color-lighter);
}

/* 拖动时禁止选择文本 */
body.resizing {
  user-select: none;
  cursor: ew-resize !important;
}

/* 移除原来的分隔线样式 */
.resize-handle-line {
  display: none;
}

.list-toolbar {
  margin-left: 5px;
  margin-top: 10px;
  margin-bottom: 4px !important; /* 设置底部间距 */
  width: 100%;
}
</style>
