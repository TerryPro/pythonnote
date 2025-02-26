<template>
  <div class="notebook-container">
    <TabsManager />
    <div class="notebooks-wrapper">
      <div 
        v-for="tab in tabs" 
        :key="tab.id" 
        class="notebook-wrapper"
        :class="{ 'active': tab.id === activeTabId }"
      >
        <NoteBook 
          v-if="tab.id === activeTabId"
          :key="tab.id"
          :session-id="tab.sessionId"
          @modified="handleNotebookModified(tab.id)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import TabsManager from '@/components/notebook/TabsManager.vue'
import NoteBook from '@/components/notebook/NoteBook.vue'
import { useTabsStore } from '@/stores/tabsStore'
import { useNotebookStore } from '@/stores/notebookStore'

const tabsStore = useTabsStore()
const notebookStore = useNotebookStore()

// 从store获取标签页数据
const tabs = computed(() => tabsStore.tabs)
const activeTabId = computed(() => tabsStore.activeTabId)

// 监听活动标签页变化，切换笔记本
watch(activeTabId, (newTabId, oldTabId) => {
  if (newTabId && newTabId !== oldTabId) {
    const tab = tabs.value.find(t => t.id === newTabId)
    if (tab) {
      // 保存当前笔记本状态
      if (oldTabId) {
        saveNotebookState(oldTabId)
      }
      
      // 加载新标签页的笔记本状态
      loadNotebookState(newTabId)
    }
  }
}, { immediate: true })

// 保存笔记本状态
const saveNotebookState = (tabId) => {
  const tab = tabs.value.find(t => t.id === tabId)
  if (!tab) return
  
  // 保存笔记本状态到标签页对象
  tab.notebookState = {
    cells: [...notebookStore.cells],
    cellContents: { ...notebookStore.cellContents },
    cellOutputs: { ...notebookStore.cellOutputs },
    cellTypes: { ...notebookStore.cellTypes },
    markdownEditStates: { ...notebookStore.markdownEditStates }
  }
}

// 加载笔记本状态
const loadNotebookState = (tabId) => {
  const tab = tabs.value.find(t => t.id === tabId)
  if (!tab) return
  
  // 如果标签页有保存的笔记本状态，恢复它
  if (tab.notebookState) {
    notebookStore.SetSessionId(tab.sessionId)
    notebookStore.setCells(tab.notebookState.cells)
    
    // 恢复单元格内容和状态
    Object.entries(tab.notebookState.cellContents).forEach(([cellId, content]) => {
      notebookStore.setCellContent(cellId, content)
    })
    
    Object.entries(tab.notebookState.cellOutputs).forEach(([cellId, output]) => {
      notebookStore.setCellOutput(cellId, output)
    })
    
    Object.entries(tab.notebookState.cellTypes).forEach(([cellId, type]) => {
      notebookStore.setCellType(cellId, type)
    })
    
    Object.entries(tab.notebookState.markdownEditStates).forEach(([cellId, state]) => {
      notebookStore.setMarkdownEditState(cellId, state)
    })
  } else {
    // 如果是新标签页，设置session_id
    notebookStore.SetSessionId(tab.sessionId)
  }
}

// 处理笔记本内容修改
const handleNotebookModified = (tabId) => {
  tabsStore.markTabAsModified(tabId, true)
}
</script>

<style lang="scss" scoped>
.notebook-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.notebooks-wrapper {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.notebook-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: none;
  
  &.active {
    display: block;
  }
}
</style> 