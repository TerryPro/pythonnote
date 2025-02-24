<template>
  <nav class="navbar">
    <div class="navbar-left">
      <h1>AI Data Note</h1>
      <VersionDisplay />
    </div>
    <div class="toolbar">
      <el-dropdown @command="handleThemeChange" trigger="click">
        <el-button class="toolbar-btn" type="primary" plain>
          <i class="fas fa-palette"></i>
          <el-tooltip
            class="box-item"
            content="选择主题"
            :hide-after="0"
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

      <el-tooltip content="添加代码单元格" placement="bottom" :hide-after="0">
        <button @click="handleAddCell('code')" class="toolbar-btn">
          <i class="fas fa-code"></i>
        </button>
      </el-tooltip>

      <el-tooltip content="添加Markdown单元格" placement="bottom" :hide-after="0">
        <button @click="handleAddCell('markdown')" class="toolbar-btn">
          <i class="fas fa-markdown"></i>
        </button>
      </el-tooltip>

      
      <el-tooltip content="系统提示词配置" placement="bottom" :hide-after="0">
        <button @click="showSystemConfig" class="toolbar-btn">
          <i class="fas fa-cog"></i>
        </button>
      </el-tooltip>

      <el-tooltip content="数据处理提示词" placement="bottom">
        <div class="tool-item" @click="togglePromptManager">
          <i class="fas fa-list-alt"></i>
        </div>
      </el-tooltip>

      <el-tooltip content="代码示例管理" placement="bottom">
        <button class="toolbar-btn" @click="codeExampleRef?.openExampleManager()">
          <i class="fas fa-file-code"></i>
        </button>
      </el-tooltip>
    </div>
  </nav>

  <!-- 添加系统配置对话框组件 -->
  <SystemPromptConfig ref="systemConfigRef" />
  
  <!-- 添加保存笔记本处理组件 -->
  <SaveNotebookHandler ref="saveNotebookRef" />

  <!-- 添加代码示例管理组件 -->
  <CodeExampleManage ref="codeExampleRef" />

  <!-- 添加预定义提示词管理弹窗 -->
  <el-dialog
    v-model="showPromptManager"
    title="管理预定义提示词"
    width="80%"
    :close-on-click-modal="false"
    destroy-on-close
  >
    <PromptPanel mode="manage" />
  </el-dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
  ElDropdown, 
  ElDropdownMenu, 
  ElDropdownItem,
  ElTooltip
} from 'element-plus'
import { useThemeManager } from '@/composables/useThemeManager'
import SystemPromptConfig from '@/components/config/SystemPromptConfig.vue'
import PromptPanel from '@/components/prompts/PromptPanel.vue'
import { useNotebook } from '@/composables/useNotebook'
import SaveNotebookHandler from '@/components/notebook/SaveNotebookHandler.vue'
import CodeExampleManage from '@/components/examples/CodeExampleManage.vue'
import VersionDisplay from '@/components/layout/VersionDisplay.vue'

const { currentTheme, themes, applyTheme, provideTheme } = useThemeManager()
provideTheme() // 为子组件提供主题上下文
const { createNewNotebook, exportPDF, addCell } = useNotebook()

const codeExampleRef = ref(null)

// 事件处理
const handleThemeChange = (themeKey) => {
  applyTheme(themeKey)
}

const saveNotebookRef = ref(null)

const showSaveDialog = () => {
  saveNotebookRef.value?.showSaveDialog()
}

const systemConfigRef = ref(null)

const showSystemConfig = () => {
  systemConfigRef.value?.show()
}

const handleAddCell = (type) => {
  addCell(type)
}

const showPromptManager = ref(false)

const togglePromptManager = () => {
  showPromptManager.value = true
}

onMounted(() => {
  applyTheme(currentTheme.value)
})
</script>

<style scoped lang="scss">
</style>
