<template>
  <div class="file-panel" :style="{ width: props.panelWidth + 'px' }">
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
        <NoteList/>
      </template>

      <!-- 添加数据文件列表 -->
      <template v-else-if="currentTab === 'dataFiles'">
        <DataFileList
          @insert-code="$emit('insert-code', $event)"
        />
      </template>

      <!-- 添加DataFrame列表 -->
      <template v-else-if="currentTab === 'dataFrames'">
        <DataFrameList/>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'
import NoteList from '@/components/notefile/NoteList.vue'
import DataFileList from '@/components/filepanel/DataFileList.vue'
import DataFrameList from '@/components/datapanel/DataFrameList.vue'

const props = defineProps({
  panelWidth: {
    type: Number,
    required: true
  },
  notebookFiles: {
    type: Array,
    required: true
  },
  currentFile: {
    type: String,
    default: ''
  },
})

const emit = defineEmits([
  'rename-notebook',
  'delete-notebook',
  'preview-datafile',
  'data-loaded',
  'insert-code',
  'select-tab'
])

const currentTab = ref('notebooks')

const selectTab = (tab) => {
  currentTab.value = tab
  emit('select-tab', tab)
}
</script>