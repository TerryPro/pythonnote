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
        <!-- 工具栏 -->
        <div class="list-toolbar">
          <el-button @click="$emit('refresh-notebooks')" class="refresh-btn icon-btn">
            <i class="fas fa-sync-alt"></i>
          </el-button>
        </div>
        
        <!-- 文件列表 -->
        <div class="file-list">
          <div 
            v-for="file in props.notebookFiles" 
            :key="file.path" 
            class="file-item"
            :class="{ active: props.currentFile === file.path }"
          >
            <div class="file-content" @click="$emit('open-notebook', file)">
              <i class="fas fa-file-code file-icon"></i>
              <span class="file-name">{{ file.name }}</span>
            </div>
            <div class="file-actions">
              <button 
                @click="$emit('rename-notebook', file)"
                class="icon-btn"
                title="重命名"
              >
                <i class="fas fa-edit"></i>
              </button>
              <button 
                @click="$emit('delete-notebook', file)"
                class="icon-btn delete-btn"
                title="删除"
              >
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
        </div>
      </template>

      <!-- 添加数据文件列表 -->
      <template v-else-if="currentTab === 'dataFiles'">
        <DataFileList
          :files="props.dataFiles"
          :current-file="props.currentDataFile"
          :get-file-icon="props.getFileIcon"
          @refresh="$emit('refresh-datafiles')"
          @preview="$emit('preview-datafile', $event)"
          @rename="$emit('rename-datafile', $event)"
          @delete="$emit('delete-datafile', $event)"
          @file-uploaded="$emit('file-uploaded', $event)"
        />
      </template>

      <!-- 添加DataFrame列表 -->
      <template v-else-if="currentTab === 'dataFrames'">
        <DataFrameList
          :dataframes="props.dataframes"
          @refresh="$emit('refresh-dataframes')"
          @preview="$emit('preview-dataframe', $event)"
        />
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DataFileList from './DataFileList.vue'
import DataFrameList from './DataFrameList.vue'

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
  dataFiles: {
    type: Array,
    required: true
  },
  currentDataFile: {
    type: String,
    default: ''
  },
  getFileIcon: {
    type: Function,
    required: true
  },
  dataframes: {
    type: Array,
    required: true
  }
})

const emit = defineEmits([
  'update:panel-width',
  'select-tab',
  'refresh-notebooks',
  'refresh-datafiles',
  'open-notebook',
  'rename-notebook',
  'delete-notebook',
  'preview-datafile',
  'rename-datafile',
  'delete-datafile',
  'refresh-dataframes',
  'file-uploaded'
])

const currentTab = ref('notebooks')

const selectTab = (tab) => {
  currentTab.value = tab
  emit('select-tab', tab)
}
</script> 