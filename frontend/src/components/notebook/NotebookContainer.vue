<template>
  <div class="notebook-container">
    <TabsBar />
    <div class="notebooks-wrapper">
      <!-- 当没有标签页时显示空白状态 -->
      <div v-if="tabs.length === 0" class="empty-state">
        <div class="empty-content">
          <i class="el-icon-notebook"></i>
          <h2>没有打开的笔记本</h2>
          <p>点击标签栏上的"+"按钮创建新的笔记本，或者从左侧文件面板打开已有的笔记本。</p>
          <el-button type="primary" @click="createNewNotebook">创建新笔记本</el-button>
        </div>
      </div>
      
      <!-- 有标签页时显示笔记本 -->
      <div 
        v-else
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
import TabsBar from '@/components/notebook/TabsBar.vue'
import NoteBook from '@/components/notebook/NoteBook.vue'
import { useTabsStore } from '@/stores/tabsStore'
import { useNotebookStore } from '@/stores/notebookStore'
import { useNotebook } from '@/composables/useNotebook'
import { ElButton } from 'element-plus'

const tabsStore = useTabsStore()
const notebookStore = useNotebookStore()
const { createNewNotebook } = useNotebook()

// 从store获取标签页数据
const tabs = computed(() => tabsStore.tabs)
const activeTabId = computed(() => tabsStore.activeTabId)

// 监听活动标签页变化，切换笔记本
watch(activeTabId, (newTabId, oldTabId) => {
  if (newTabId && newTabId !== oldTabId) {
    const tab = tabs.value.find(t => t.id === newTabId)
    if (tab) {
      // 使用新的notebookStore API切换活动笔记本
      notebookStore.setActiveNotebook(newTabId)
      
      // 如果是新标签页，设置session_id
      if (!notebookStore.session_id) {
        notebookStore.setSessionId(tab.sessionId)
      }
    }
  }
}, { immediate: true })

// 处理笔记本内容修改
const handleNotebookModified = (tabId) => {
  // 标记标签页为已修改
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

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  background-color: var(--background);
  
  .empty-content {
    text-align: center;
    max-width: 500px;
    padding: 2rem;
    
    i {
      font-size: 4rem;
      color: var(--text-color-secondary);
      margin-bottom: 1rem;
    }
    
    h2 {
      font-size: 1.5rem;
      color: var(--text-color);
      margin-bottom: 1rem;
    }
    
    p {
      color: var(--text-color-secondary);
      margin-bottom: 2rem;
      line-height: 1.5;
    }
  }
}
</style> 