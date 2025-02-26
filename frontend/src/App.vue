<template>
  <div id="app">
    <LoadingMask />
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
import LoadingMask from '@/components/common/LoadingMask.vue'

const notebookStore = useNotebookStore()

onMounted(async () => {
  await notebookStore.fetchNotebooks()
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
