import { ElMessage } from 'element-plus'
import { API_ENDPOINTS, downloadFile } from '@/api/http'
import { useNotebookStore } from '@/stores/notebookStore'
import { v4 as uuidv4 } from 'uuid'
import { useDataFrameStore } from '@/stores/dataframeStore'

export function useNotebook() {
  const store = useNotebookStore()
  const dataframeStore = useDataFrameStore()

  // 创建新笔记本
  const createNewNotebook = async () => {
    try {
      // await apiCall(API_ENDPOINTS.EXECUTION.RESET_CONTEXT, { method: 'POST' })
      store.clearNotebookState()
      store.session_id = uuidv4()
      store.currentFile = null
      addCell('code')
    } catch (error) {
      console.error('创建新笔记本失败:', error)
      ElMessage.error('创建新笔记本失败')
    }
  }

  const _refreshDataFrame = async (session_id) => {
    try {
      await dataframeStore.fetchDataFrames(session_id)
      ElMessage.success('变量已刷新')
    } catch (error) {
      console.error(error.message)
    }
  }

  // 打开笔记本
  const openNotebook = async (file) => {
    try {
      const notebook = await store.loadNotebook(file)
      
      if (!notebook) {
        throw new Error('加载笔记本失败')
      }

      // 如果笔记本为空，添加一个代码单元格
      if (store.cells.length === 0) {
        addCell('code')
      }

      _refreshDataFrame(store.session_id)

    } catch (error) {
      console.error('打开笔记本失败:', error)
      ElMessage.error('打开笔记本失败')
      // 如果打开失败，创建一个新的笔记本
      createNewNotebook()
    }
  }

  // 添加单元格
  const addCell = (type = 'code') => {
    const newCellId = uuidv4()
    store.cells.push(newCellId)
    store.cellContents[newCellId] = ''
    store.cellTypes[newCellId] = type
    if (type === 'code') {
      store.cellOutputs[newCellId] = {
        output: '',
        plot: '',
        plotly_html: '',
        status: 'idle'
      }
    } else if (type === 'markdown') {
      store.markdownEditStates[newCellId] = true
    }
  }

  // 处理执行完成
  const handleExecutionComplete = (cellId) => {
    const index = store.cells.indexOf(cellId)
    if (index === store.cells.length - 1) {
      addCell('code')
    }
  }

  // 更改单元格类型
  const changeCellType = (cellId, newType) => {
    if (!cellId || store.cellTypes[cellId] === newType) return
    
    const currentContent = store.cellContents[cellId] || ''
    
    // 更新单元格类型
    store.cellTypes[cellId] = newType
    
    // 根据新类型设置相应的状态
    if (newType === 'code') {
      store.cellOutputs[cellId] = {
        output: '',
        plot: '',
        plotly_html: '',
        status: 'idle'
      }
      delete store.markdownEditStates[cellId]
    } else if (newType === 'markdown') {
      delete store.cellOutputs[cellId]
      store.markdownEditStates[cellId] = true
    }

    // 重置单元格内容
    store.cellContents[cellId] = currentContent
  }

  // 向上移动单元格
  const moveCellUp = (cellId) => {
    const currentIndex = store.cells.indexOf(cellId)
    if (currentIndex > 0) {
      const temp = store.cells[currentIndex]
      store.cells[currentIndex] = store.cells[currentIndex - 1]
      store.cells[currentIndex - 1] = temp
    }
  }

  // 向下移动单元格
  const moveCellDown = (cellId) => {
    const currentIndex = store.cells.indexOf(cellId)
    if (currentIndex < store.cells.length - 1) {
      const temp = store.cells[currentIndex]
      store.cells[currentIndex] = store.cells[currentIndex + 1]
      store.cells[currentIndex + 1] = temp
    }
  }

  // 导出PDF
  const exportPDF = async () => {
    try {
      if (!store.currentFile) {
        const fileName = prompt('请输入PDF文件名：')
        if (!fileName) return
        store.currentFile = fileName
      }

      const notebook = {
        cells: store.cells.map(cellId => ({
          id: cellId,
          type: store.cellTypes[cellId],
          content: store.cellContents[cellId] || '',
          output: store.cellTypes[cellId] === 'code' ? (store.cellOutputs[cellId] || {
            output: '',
            plot: '',
            status: 'idle'
          }) : null
        }))
      }

      const data = {
        filename: store.currentFile,
        notebook: notebook,
      };
      await downloadFile(API_ENDPOINTS.EXPORT_PDF.EXPORT, `${store.currentFile}.pdf`, data);
    } catch (error) {
      console.error('导出PDF失败:', error)
      ElMessage.error('导出PDF失败: ' + error.message)
    }
  }

  // 删除单元格
  const deleteCell = (cellId) => {
    const index = store.cells.indexOf(cellId)
    if (index > -1) {
      // 从数组中移除单元格ID
      store.cells.splice(index, 1)
      // 删除相关的内容和状态
      delete store.cellContents[cellId]
      delete store.cellOutputs[cellId]
      delete store.cellTypes[cellId]
      delete store.markdownEditStates[cellId]
      
      // 如果删除后没有单元格了，添加一个新的代码单元格
      if (store.cells.length === 0) {
        addCell('code')
      }
      
      return true
    }
    return false
  }

  // 在当前单元格上方添加新单元格
  const addCellAbove = (cellId) => {
    const currentIndex = store.cells.indexOf(cellId)
    const newCellId = uuidv4()
    
    // 在当前单元格前插入新单元格
    store.cells.splice(currentIndex, 0, newCellId)
    store.cellContents[newCellId] = ''
    store.cellTypes[newCellId] = 'code'
    store.cellOutputs[newCellId] = {
      output: '',
      plot: '',
      plotly_html: '',
      status: 'idle'
    }
  }

  // 在当前单元格下方添加新单元格
  const addCellBelow = (cellId) => {
    const currentIndex = store.cells.indexOf(cellId)
    const newCellId = uuidv4()
    
    // 在当前单元格后插入新单元格
    store.cells.splice(currentIndex + 1, 0, newCellId)
    store.cellContents[newCellId] = ''
    store.cellTypes[newCellId] = 'code'
    store.cellOutputs[newCellId] = {
      output: '',
      plot: '',
      plotly_html: '',
      status: 'idle'
    }
  }

  // 新增插入代码函数
  const insertCode = (code) => {
    const newCellId = uuidv4()

    if (store.cells.length === 0 || store.cellContents[store.cells[store.cells.length - 1]] !== '') {
      store.cells.push(newCellId)
    } else {
      store.cellContents[store.cells[store.cells.length - 1]] = code
    }

    store.cellContents[newCellId] = code
    store.cellTypes[newCellId] = 'code'
    store.cellOutputs[newCellId] = {
      output: '',
      plot: '',
      plotly_html: '',
      status: 'idle'
    }
  }

  // 添加复制功能
  const copyCell = (cellId) => {
    const content = store.cellContents[cellId]
    if (content) {
      navigator.clipboard.writeText(content).then(() => {
        ElMessage.success('内容已复制到剪贴板')
      }).catch(() => {
        ElMessage.error('复制失败')
      })
    }
  }

  return {
    createNewNotebook,
    openNotebook,
    addCell,
    handleExecutionComplete,
    changeCellType,
    exportPDF,
    moveCellUp,
    moveCellDown,
    deleteCell,
    addCellAbove,
    addCellBelow,
    insertCode,
    copyCell
  }
}