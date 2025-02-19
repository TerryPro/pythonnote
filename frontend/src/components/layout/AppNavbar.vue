<template>
  <nav class="navbar">
    <div class="navbar-left">
      <h1>AI Data Note</h1>
      <span class="version">{{ version }}</span>
    </div>
    <div class="toolbar">
      <el-dropdown @command="handleThemeChange" trigger="click">
        <el-button class="toolbar-btn" type="primary" plain>
          <i class="fas fa-palette"></i>
          <el-tooltip
            class="box-item"
            effect="light"
            content="选择主题"
            placement="bottom"
          >
            <span class="el-dropdown-link"></span>
          </el-tooltip>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item 
              v-for="(theme, key) in themes" 
              :key="key"
              :command="key"
              :class="{ 'is-active': currentTheme === key }"
            >
              <i class="fas fa-check" v-if="currentTheme === key"></i>
              {{ theme.name }}
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
      
      <el-tooltip content="新建笔记本" placement="bottom" :hide-after="0">
        <button @click="createNewNotebook" class="toolbar-btn">
          <i class="fas fa-plus"></i>
        </button>
      </el-tooltip>

      <el-tooltip content="保存笔记本" placement="bottom" :hide-after="0">
        <button @click="showSaveDialog" class="toolbar-btn">
          <i class="fas fa-save"></i>
        </button>
      </el-tooltip>

      <el-tooltip content="导出PDF" placement="bottom" :hide-after="0">
        <button @click="exportPDF" class="toolbar-btn">
          <i class="fas fa-file-pdf"></i>
        </button>
      </el-tooltip>

      <el-tooltip content="系统配置" placement="bottom" :hide-after="0">
        <button @click="showSystemConfig" class="toolbar-btn">
          <i class="fas fa-cog"></i>
        </button>
      </el-tooltip>

      <el-tooltip content="添加代码单元格" placement="bottom" :hide-after="0">
        <button @click="addCell('code')" class="toolbar-btn">
          <i class="fas fa-code"></i>
        </button>
      </el-tooltip>

      <el-tooltip content="添加Markdown单元格" placement="bottom" :hide-after="0">
        <button @click="addCell('markdown')" class="toolbar-btn">
          <i class="fas fa-markdown"></i>
        </button>
      </el-tooltip>

      <el-tooltip content="管理预定义提示词" placement="bottom">
        <div class="tool-item" @click="togglePromptManager">
          <i class="fas fa-list-alt"></i>
        </div>
      </el-tooltip>

      <el-tooltip content="管理代码示例" placement="bottom">
        <button class="toolbar-btn" @click="openExampleManager">
          <i class="fas fa-file-code"></i>
        </button>
      </el-tooltip>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { 
  ElDropdown, 
  ElDropdownMenu, 
  ElDropdownItem,
  ElTooltip
} from 'element-plus'
import { useTheme } from '@/composables/useThemeManager'
import { API_ENDPOINTS, apiCall } from '@/api/http'

const { currentTheme, themes } = useTheme()

// 定义事件
const emit = defineEmits([
  'create-notebook',
  'show-save-dialog',
  'export-pdf',
  'show-config',
  'add-cell',
  'open-example-manager',
  'update-theme',
  'toggle-prompt-manager'
])

// 版本信息
const version = ref('加载中...')

// 暴露版本获取方法
const fetchVersion = async () => {
  try {
    const result = await apiCall(API_ENDPOINTS.SYSTEM.VERSION)
    version.value = result.data.version
  } catch (error) {
    console.error('获取版本信息失败:', error)
    version.value = '未知版本'
  }
}

// 事件处理
const handleThemeChange = (themeKey) => {
  emit('update-theme', themeKey)
}

const createNewNotebook = () => {
  emit('create-notebook')
}

const showSaveDialog = () => {
  emit('show-save-dialog')
}

const exportPDF = () => {
  emit('export-pdf')
}

const showSystemConfig = () => {
  emit('show-config')
}

const addCell = (type) => {
  emit('add-cell', type)
}

const openExampleManager = () => {
  emit('open-example-manager')
}

const togglePromptManager = () => {
  emit('toggle-prompt-manager')
}

// 暴露方法给父组件
defineExpose({
  fetchVersion
})
</script> 