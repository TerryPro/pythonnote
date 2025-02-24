<template>
  <div id="app">
    <AppNavbar />
    <main class="main-container">
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
.main-container {
  flex: 1;
  display: flex;
  height: calc(100vh - var(--navbar-height));
  overflow: hidden;
  position: relative;
}
</style>
