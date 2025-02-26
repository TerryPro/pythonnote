<template>
  <div class="tabs-container">
    <!-- 左滚动按钮 -->
    <div class="tabs-scroll-container" ref="tabsScrollContainer">
      <el-tabs 
        v-model="activeTabId" 
        type="card" 
        closable 
        @tab-click="handleTabClick"
        @tab-remove="handleTabRemove"
        class="notebook-tabs"
      >
        <el-tab-pane
          v-for="tab in tabs"
          :key="tab.id"
          :label="tab.title"
          :name="tab.id"
        >
          <template #label>
            <div class="custom-tab-label">
              <div class="title-row">
                <span class="tab-title">{{ tab.title }}</span>
                <span v-if="tab.isModified" class="modified-indicator">*</span>
              </div>
              <div class="tab-tags">
                <el-tag 
                  v-for="tag in tab.tags" 
                  :key="tag" 
                  size="small" 
                  closable 
                  @close.stop="removeTag(tab.id, tag)"
                >
                  {{ tag }}
                </el-tag>
              </div>
            </div>
          </template>
        </el-tab-pane>
      </el-tabs>
    </div>
    
    <div class="tabs-actions">
      <el-button 
        type="primary"
        size="small" 
        @click="createNewTab"
        title="新建标签页"
        :icon="Plus"
        circle
        plain
      />
      <el-button 
        type="success"
        size="small" 
        @click="saveCurrentNotebook"
        title="保存笔记本"
        :icon="Check"
        circle
        plain
        v-if="activeTab"
      />
      <el-button 
        type="warning"
        size="small" 
        @click="exportToPDF"
        title="导出PDF"
        :icon="Document"
        circle
        plain
        v-if="activeTab"
      />
      <el-dropdown 
        trigger="click" 
        @command="handleCommand"
        v-if="activeTab"
      >
        <el-button 
          type="info"
          size="small"
          title="标签操作"
          :icon="More"
          circle
          plain
        />
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="closeOthers">关闭其他标签页</el-dropdown-item>
            <el-dropdown-item command="closeAll">关闭所有标签页</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
  
  <!-- 添加保存笔记本处理组件 -->
  <SaveNotebookHandler ref="saveNotebookRef" />
</template>

<script setup>
import { computed, ref } from 'vue'
import { useTabsStore } from '@/stores/tabsStore'
import { useNotebook } from '@/composables/useNotebook'
import { ElMessageBox } from 'element-plus'
import { Plus, More, Check, Document} from '@element-plus/icons-vue'
import SaveNotebookHandler from '@/components/notebook/SaveNotebookHandler.vue'

const tabsStore = useTabsStore()
const { createNewNotebook, saveNotebook, closeNotebook, exportPDF } = useNotebook()
const saveNotebookRef = ref(null)

// 从store获取标签页数据
const tabs = computed(() => tabsStore.tabs)
const activeTabId = computed({
  get: () => tabsStore.activeTabId,
  set: (value) => tabsStore.activateTab(value)
})
const activeTab = computed(() => tabsStore.activeTab)

// 处理标签点击
const handleTabClick = (tab) => {
  tabsStore.activateTab(tab.props.name)
}

// 处理标签关闭
const handleTabRemove = async (tabId) => {
  await closeTab(tabId)
}

// 关闭标签页
const closeTab = async (tabId) => {
  const tab = tabs.value.find(t => t.id === tabId)
  
  // 如果标签页已修改，询问是否保存
  if (tab && tab.isModified) {
    try {
      const action = await ElMessageBox.confirm(
        '标签页内容已修改，是否保存？',
        '关闭标签页',
        {
          confirmButtonText: '保存',
          cancelButtonText: '不保存',
          type: 'warning',
          distinguishCancelAndClose: true,
          closeOnClickModal: false
        }
      )
      
      if (action === 'confirm') {
        // 激活要保存的标签页
        tabsStore.activateTab(tabId)
        
        // 如果已有文件名，直接保存
        if (tab.notebookFile) {
          await saveNotebook()
        } else {
          // 否则弹出保存对话框
          const { value: fileName } = await ElMessageBox.prompt(
            '请输入笔记本名称',
            '保存笔记本',
            {
              confirmButtonText: '保存',
              cancelButtonText: '取消',
              inputValue: tab.title
            }
          )
          
          if (fileName) {
            await saveNotebook(fileName)
          }
        }
      }
    } catch (e) {
      if (e !== 'cancel') {
        return // 用户取消关闭
      }
    }
  }
  
  // 使用closeNotebook函数关闭笔记本，它会同时关闭标签页和笔记本状态
  closeNotebook(tabId)
}

// 创建新标签页
const createNewTab = () => {
  createNewNotebook()
}

// 保存当前笔记本
const saveCurrentNotebook = () => {
  saveNotebookRef.value?.showSaveDialog()
}

// 导出PDF
const exportToPDF = () => {
  exportPDF()
}

// 移除标签
const removeTag = (tabId, tag) => {
  tabsStore.removeTag(tabId, tag)
}

// 处理下拉菜单命令
const handleCommand = (command) => {
  if (!activeTab.value) return
  
  switch (command) {
    case 'closeOthers':
      closeOtherTabs()
      break
    case 'closeAll':
      closeAllTabs()
      break
  }
}

// 关闭其他标签页
const closeOtherTabs = async () => {
  const otherTabs = tabs.value.filter(tab => tab.id !== activeTab.value.id)
  
  // 检查是否有修改过的标签页
  const modifiedTabs = otherTabs.filter(tab => tab.isModified)
  
  if (modifiedTabs.length > 0) {
    try {
      await ElMessageBox.confirm(
        `有 ${modifiedTabs.length} 个标签页内容已修改但未保存，确定要关闭吗？`,
        '关闭其他标签页',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
    } catch (e) {
      return // 用户取消
    }
  }
  
  // 关闭其他标签页
  for (const tab of otherTabs) {
    closeNotebook(tab.id)
  }
}

// 关闭所有标签页
const closeAllTabs = async () => {
  // 检查是否有修改过的标签页
  const modifiedTabs = tabs.value.filter(tab => tab.isModified)
  
  if (modifiedTabs.length > 0) {
    try {
      await ElMessageBox.confirm(
        `有 ${modifiedTabs.length} 个标签页内容已修改但未保存，确定要关闭吗？`,
        '关闭所有标签页',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
    } catch (e) {
      return // 用户取消
    }
  }
  
  // 关闭所有标签页
  for (const tab of [...tabs.value]) {
    closeNotebook(tab.id)
  }
}
</script>

<style lang="scss" scoped>
.tabs-container {
  display: flex;
  align-items: center;
  background-color: var(--background-secondary);
  border-bottom: 1px solid var(--border-color);
  padding: 0 8px;
  user-select: none;
  position: relative;
}

.tabs-scroll-container {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
  position: relative;
  
  &::-webkit-scrollbar {
    display: none; /* Chrome, Safari, Opera */
  }
}

.notebook-tabs {
  width: 100%;
  
  :deep(.el-tabs__header) {
    margin-bottom: 0;
  }
  
  :deep(.el-tabs__nav) {
    border: none;
  }
  
  :deep(.el-tabs__item) {
    height: 36px;
    line-height: 36px;
    border: none;
    background-color: var(--background-tertiary);
    transition: background-color 0.2s;
    
    &:hover {
      background-color: var(--background-hover);
    }
    
    &.is-active {
      background-color: var(--background);
      border-bottom: 2px solid var(--primary-color);
    }
  }
}

.custom-tab-label {
  display: flex;
  flex-direction: column;
  max-width: 180px;
  overflow: hidden;
}

.title-row {
  display: flex;
  align-items: center;
}

.tab-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.modified-indicator {
  color: var(--warning-color);
  margin-left: 2px;
  font-size: 12px;
}

.tab-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 2px;
  margin-top: 2px;
  
  .el-tag {
    height: 16px;
    line-height: 14px;
    padding: 0 4px;
    font-size: 10px;
  }
}

.tabs-actions {
  display: flex;
  align-items: center;
  margin-left: 8px;
  position: sticky;
  right: 8px;
  
  .el-button {
    margin-left: 4px;
  }
}
</style>