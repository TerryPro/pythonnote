<template>
  <div id="app">
    <AppNavbar />
    <main class="main-container">
      <AppSidebar/>
      <ResizeHandle />
      <NotebookContainer />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AppNavbar from '@/components/layout/AppNavbar.vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import ResizeHandle from '@/components/layout/ResizeHandle.vue'
import NotebookContainer from '@/components/notebook/NotebookContainer.vue'
import { useNotebookStore } from '@/stores/notebookStore'
import { useTabsStore } from '@/stores/tabsStore'

const notebookStore = useNotebookStore()
const tabsStore = useTabsStore()

onMounted(async () => {
  await notebookStore.fetchNotebooks()
  // 创建初始标签页
  if (tabsStore.tabCount === 0) {
    tabsStore.addTab()
  }
})
</script>

<style lang="scss">
.main-container {
  flex: 1;
  display: flex;
  height: calc(100vh - var(--navbar-height));
  overflow: hidden;
  position: relative;
}
</style>
