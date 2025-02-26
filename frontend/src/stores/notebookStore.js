import { defineStore } from 'pinia'
import { listNotebooks, saveNotebook as apiSaveNotebook, loadNotebook as apiLoadNotebook } from '@/api/notebook_api'

export const useNotebookStore = defineStore('notebook', {
  state: () => ({
    notebookFiles: [], // 所有可用的笔记本文件列表
    notebooks: {}, // 存储所有打开的笔记本状态，格式为 { tabId: notebookState }
    activeNotebookId: null, // 当前活动的笔记本ID（对应tabId）
  }),
  getters: {
    // 获取当前活动的笔记本状态
    currentNotebook: (state) => state.notebooks[state.activeNotebookId] || null,
    
    // 获取当前笔记本的cells数组
    cells: (state) => state.currentNotebook?.cells || [],
    
    // 获取当前笔记本的cellContents
    cellContents: (state) => state.currentNotebook?.cellContents || {},
    
    // 获取当前笔记本的cellOutputs
    cellOutputs: (state) => state.currentNotebook?.cellOutputs || {},
    
    // 获取当前笔记本的cellTypes
    cellTypes: (state) => state.currentNotebook?.cellTypes || {},
    
    // 获取当前笔记本的markdownEditStates
    markdownEditStates: (state) => state.currentNotebook?.markdownEditStates || {},
    
    // 获取当前笔记本的session_id
    session_id: (state) => state.currentNotebook?.session_id || null,
    
    // 获取当前笔记本的文件名
    currentFile: (state) => state.currentNotebook?.fileName || null,
  },
  actions: {
    // 获取所有可用的笔记本文件
    async fetchNotebooks() {
      const notebooks = await listNotebooks()
      this.notebookFiles = notebooks || []
    },
    
    // 设置当前活动的笔记本ID
    setActiveNotebook(tabId) {
      this.activeNotebookId = tabId
      
      // 如果该笔记本不存在，则创建一个空的笔记本状态
      if (tabId && !this.notebooks[tabId]) {
        this.notebooks[tabId] = this.createEmptyNotebookState()
      }
    },
    
    // 创建空的笔记本状态
    createEmptyNotebookState() {
      return {
        cells: [],
        cellContents: {},
        cellOutputs: {},
        cellTypes: {},
        markdownEditStates: {},
        session_id: null,
        fileName: null,
      }
    },
    
    // 设置笔记本的session_id
    setSessionId(sessionId) {
      if (!this.activeNotebookId) return
      
      if (!this.notebooks[this.activeNotebookId]) {
        this.notebooks[this.activeNotebookId] = this.createEmptyNotebookState()
      }
      
      this.notebooks[this.activeNotebookId].session_id = sessionId
    },
    
    // 设置笔记本的cells数组
    setCells(cells) {
      if (!this.activeNotebookId) return
      this.notebooks[this.activeNotebookId].cells = cells
    },
    
    // 设置单元格内容
    setCellContent(cellId, content) {
      if (!this.activeNotebookId) return
      this.notebooks[this.activeNotebookId].cellContents[cellId] = content
    },
    
    // 设置单元格输出
    setCellOutput(cellId, output) {
      if (!this.activeNotebookId) return
      this.notebooks[this.activeNotebookId].cellOutputs[cellId] = output
    },
    
    // 设置单元格类型
    setCellType(cellId, type) {
      if (!this.activeNotebookId) return
      this.notebooks[this.activeNotebookId].cellTypes[cellId] = type
    },
    
    // 设置Markdown编辑状态
    setMarkdownEditState(cellId, state) {
      if (!this.activeNotebookId) return
      this.notebooks[this.activeNotebookId].markdownEditStates[cellId] = state
    },
    
    // 清除当前笔记本状态
    clearNotebookState() {
      if (!this.activeNotebookId) return
      
      this.notebooks[this.activeNotebookId] = {
        cells: [],
        cellContents: {},
        cellOutputs: {},
        cellTypes: {},
        markdownEditStates: {},
        session_id: this.notebooks[this.activeNotebookId]?.session_id || null,
        fileName: null,
      }
    },
    
    // 重置笔记本
    async resetNotebook() {
      try {
        // await apiCall(API_ENDPOINTS.EXECUTION.RESET_CONTEXT, { method: 'POST' })
        this.clearNotebookState()
        return true
      } catch (error) {
        console.error('重置笔记本失败:', error)
        return false
      }
    },
    
    // 保存笔记本
    async saveNotebook(fileName = '') {
      if (!this.activeNotebookId) return false
      
      try {
        const notebook = this.notebooks[this.activeNotebookId]
        
        if (fileName) {
          notebook.fileName = fileName + '.ipynb'
        }
        
        const notebookData = {
          session_id: notebook.session_id,
          cells: notebook.cells.map(cellId => ({
            id: cellId,
            type: notebook.cellTypes[cellId],
            content: notebook.cellContents[cellId] || '',
            output: notebook.cellTypes[cellId] === 'code' ? (notebook.cellOutputs[cellId] || {
              output: '',
              plot: '',
              plotly_html: '',
              status: 'idle'
            }) : null
          }))
        }

        await apiSaveNotebook(notebook.fileName, notebookData)
        await this.fetchNotebooks()
        return true
      } catch (error) {
        console.error('保存笔记本失败:', error)
        return false
      }
    },
    
    // 加载笔记本
    async loadNotebook(file, tabId) {
      try {
        const notebookData = await apiLoadNotebook(file.path)
        
        // 如果没有提供tabId，使用当前活动的笔记本ID
        const targetTabId = tabId || this.activeNotebookId
        if (!targetTabId) return false
        
        // 初始化笔记本状态
        if (!this.notebooks[targetTabId]) {
          this.notebooks[targetTabId] = this.createEmptyNotebookState()
        } else {
          this.clearNotebookState()
        }
        
        const notebook = this.notebooks[targetTabId]
        
        // 设置文件名和会话ID
        notebook.fileName = file.path
        notebook.session_id = notebookData.session_id
        
        // 处理笔记本中的单元格
        if (notebookData.cells && Array.isArray(notebookData.cells)) {
          notebookData.cells.forEach(cell => {
            if (cell && cell.id) {
              notebook.cells.push(cell.id)
              notebook.cellTypes[cell.id] = cell.type || 'code'
              notebook.cellContents[cell.id] = cell.content || ''
              
              if (cell.type === 'code') {
                notebook.cellOutputs[cell.id] = {
                  output: cell.output?.output || '',
                  plot: cell.output?.plot || '',
                  plotly_html: cell.output?.plotly_html || '',
                  status: cell.output?.status || 'idle'
                }
              }
            }
          })
        }
        
        // 设置当前活动的笔记本ID
        this.activeNotebookId = targetTabId
        
        return true
      } catch (error) {
        console.error('加载笔记本失败:', error)
        return false
      }
    },
    
    // 关闭笔记本
    closeNotebook(tabId) {
      if (this.notebooks[tabId]) {
        delete this.notebooks[tabId]
      }
      
      // 如果关闭的是当前活动的笔记本，将activeNotebookId设为null
      if (this.activeNotebookId === tabId) {
        this.activeNotebookId = null
      }
    },
    
    // 获取指定笔记本的状态
    getNotebookState(tabId) {
      return this.notebooks[tabId] || null
    },
    
    // 兼容旧API的方法
    SetSessionId(sessionId) {
      this.setSessionId(sessionId)
    }
  }
})