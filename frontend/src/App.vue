<template>
  <div id="app">
    <AppNavbar />
    <main class="main-container">
      <AppSidebar/>
      <ResizeHandle />
      <NoteBook />
      <AppSidebar/>
      <ResizeHandle />
      <NoteBook />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AppNavbar from '@/components/layout/AppNavbar.vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import ResizeHandle from '@/components/layout/ResizeHandle.vue'
import NoteBook from '@/components/notebook/NoteBook.vue'
import { useNotebookStore } from '@/stores/notebookStore'
import { useNotebook } from '@/composables/useNotebook'

const store = useNotebookStore()
const { createNewNotebook } = useNotebook()

onMounted(async () => {
  await store.fetchNotebooks()
  createNewNotebook()
})
</script>

<style lang="scss">
@import '@/styles/layout/_navbar.scss';
@import '@/styles/layout/_sidebar.scss';
@import '@/styles/base/_base.scss';

.main-container {
  flex: 1;
  display: flex;
  height: calc(100vh - 47px); /* 减去navbar的高度 */
  overflow: hidden;
  position: relative;
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

</style>
