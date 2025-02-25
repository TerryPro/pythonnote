<template>
  <div class="file-panel" :style="{ width: panelWidth + 'px' }">
    <div class="button-group">
      <el-button 
        @click="selectTab('notebooks')" 
        :class="{ active: currentTab === 'notebooks' }"
      >
        <i class="fas fa-book"></i>
      </el-button>
      <el-button 
        @click="selectTab('dataFiles')" 
        :class="{ active: currentTab === 'dataFiles' }"
      >
        <i class="fas fa-file-alt"></i>
      </el-button>
      <el-button 
        @click="selectTab('dataFrames')" 
        :class="{ active: currentTab === 'dataFrames' }"
      >
        <i class="fas fa-database"></i>
      </el-button>
    </div>
    
    <div class="content-area">
      <!-- 各选项卡内容 -->
      <template v-if="currentTab === 'notebooks'">
        <!-- 使用NoteList组件 -->
        <NotePanel/>
      </template>

      <!-- 添加数据文件列表 -->
      <template v-else-if="currentTab === 'dataFiles'">
        <FilePanel/>
      </template>

      <!-- 添加DataFrame列表 -->
      <template v-else-if="currentTab === 'dataFrames'">
        <DataPanel/>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import NotePanel from '@/components/panel/notepanel/NotePanel.vue'
import FilePanel from '@/components/panel/filepanel/FilePanel.vue'
import DataPanel from '@/components/panel/datapanel/DataPanel.vue'

import { useResizePanelStore } from '@/stores/resizePanelStore'
import { computed } from 'vue'

const resizePanelStore = useResizePanelStore()
const panelWidth = computed(() => resizePanelStore.panelWidth)

const currentTab = ref('notebooks')

const selectTab = (tab) => {
  currentTab.value = tab
}
</script>