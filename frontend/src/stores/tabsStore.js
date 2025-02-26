import { defineStore } from 'pinia'
import { v4 as uuidv4 } from 'uuid'

export const useTabsStore = defineStore('tabs', {
  state: () => ({
    tabs: [], // 存储所有打开的标签页
    activeTabId: null, // 当前激活的标签页ID
  }),
  getters: {
    activeTab: (state) => state.tabs.find(tab => tab.id === state.activeTabId),
    tabCount: (state) => state.tabs.length,
  },
  actions: {
    // 添加新标签页
    addTab(notebook = null, title = '未命名') {
      const tabId = uuidv4()
      const newTab = {
        id: tabId,
        title: title,
        notebookFile: notebook?.path || null,
        sessionId: notebook?.session_id || uuidv4(),
        tags: [], // 标签列表
        isModified: false
      }
      
      this.tabs.push(newTab)
      this.activeTabId = tabId
      return tabId
    },
    
    // 关闭标签页
    closeTab(tabId) {
      const index = this.tabs.findIndex(tab => tab.id === tabId)
      if (index === -1) return
      
      // 如果关闭的是当前激活的标签页，需要激活其他标签页
      if (this.activeTabId === tabId) {
        if (this.tabs.length > 1) {
          // 如果有其他标签页，激活下一个或上一个
          const newActiveIndex = index === this.tabs.length - 1 ? index - 1 : index + 1
          this.activeTabId = this.tabs[newActiveIndex].id
        } else {
          this.activeTabId = null
        }
      }
      
      // 移除标签页
      this.tabs.splice(index, 1)
    },
    
    // 激活标签页
    activateTab(tabId) {
      if (this.tabs.some(tab => tab.id === tabId)) {
        this.activeTabId = tabId
      }
    },
    
    // 更新标签页标题
    updateTabTitle(tabId, title) {
      const tab = this.tabs.find(tab => tab.id === tabId)
      if (tab) {
        tab.title = title
      }
    },
    
    // 标记标签页为已修改
    markTabAsModified(tabId, isModified = true) {
      const tab = this.tabs.find(tab => tab.id === tabId)
      if (tab) {
        tab.isModified = isModified
      }
    },
    
    // 添加标签
    addTag(tabId, tag) {
      const tab = this.tabs.find(tab => tab.id === tabId)
      if (tab && !tab.tags.includes(tag)) {
        tab.tags.push(tag)
      }
    },
    
    // 移除标签
    removeTag(tabId, tag) {
      const tab = this.tabs.find(tab => tab.id === tabId)
      if (tab) {
        const index = tab.tags.indexOf(tag)
        if (index !== -1) {
          tab.tags.splice(index, 1)
        }
      }
    },
    
    // 更新标签页的笔记本文件信息
    updateTabNotebook(tabId, notebookFile) {
      const tab = this.tabs.find(tab => tab.id === tabId)
      if (tab) {
        tab.notebookFile = notebookFile
        tab.isModified = false
      }
    }
  }
}) 