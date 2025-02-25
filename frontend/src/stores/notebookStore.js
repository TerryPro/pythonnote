import { defineStore } from 'pinia'
import { listNotebooks, saveNotebook as apiSaveNotebook, loadNotebook as apiLoadNotebook } from '@/api/notebook_api'

export const useNotebookStore = defineStore('notebook', {
  state: () => ({
    notebookFiles: [],
    currentFile: null,
    session_id: null,
    cells: [],
    cellContents: {},
    cellOutputs: {},
    cellTypes: {},
    markdownEditStates: {}
  }),
  actions: {
    async fetchNotebooks() {
      const notebooks = await listNotebooks()
      this.notebookFiles = notebooks || []
    },
    SetSessionId(sessionId) {
      this.session_id = sessionId
    },
    setCells(cells) {
      this.cells = cells
    },
    setCellContent(cellId, content) {
      this.cellContents[cellId] = content
    },
    setCellOutput(cellId, output) {
      this.cellOutputs[cellId] = output
    },
    setCellType(cellId, type) {
      this.cellTypes[cellId] = type
    },
    setMarkdownEditState(cellId, state) {
      this.markdownEditStates[cellId] = state
    },
    clearNotebookState() {
      this.session_id = null
      this.cells = []
      this.cellContents = {}
      this.cellOutputs = {}
      this.cellTypes = {}
      this.markdownEditStates = {}
    },
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
    async saveNotebook(fileName = '') {
      try {
        if (fileName) {
          this.currentFile = fileName + '.ipynb'
        }
        
        const notebook = {
          session_id: this.session_id,
          cells: this.cells.map(cellId => ({
            id: cellId,
            type: this.cellTypes[cellId],
            content: this.cellContents[cellId] || '',
            output: this.cellTypes[cellId] === 'code' ? (this.cellOutputs[cellId] || {
              output: '',
              plot: '',
              plotly_html: '',
              status: 'idle'
            }) : null
          }))
        }

        await apiSaveNotebook(this.currentFile, notebook)
        await this.fetchNotebooks()
        return true
      } catch (error) {
        console.error('保存笔记本失败:', error)
        return false
      }
    },

    async loadNotebook(file) {
      try {
        // await apiCall(API_ENDPOINTS.EXECUTION.RESET_CONTEXT, { method: 'POST' })
        const notebook = await apiLoadNotebook(file.path)
        this.currentFile = file.path
        
        // 初始化状态
        this.clearNotebookState()
        
        // 保存session_id
        this.session_id = notebook.session_id
        // 处理笔记本中的单元格
        if (notebook.cells && Array.isArray(notebook.cells)) {
          notebook.cells.forEach(cell => {
            if (cell && cell.id) {
              this.cells.push(cell.id)
              this.cellTypes[cell.id] = cell.type || 'code'
              this.cellContents[cell.id] = cell.content || ''
              
              if (cell.type === 'code') {
                this.cellOutputs[cell.id] = {
                  output: cell.output?.output || '',
                  plot: cell.output?.plot || '',
                  plotly_html: cell.output?.plotly_html || '',
                  status: cell.output?.status || 'idle'
                }
              }
            }
          })
        }

        return true
      } catch (error) {
        console.error('加载笔记本失败:', error)
        return false
      }
    }
  }
})