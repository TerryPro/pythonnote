import { ElMessage } from 'element-plus'
import { API_ENDPOINTS, downloadFile } from '@/api/http'
import { useNotebookStore } from '@/stores/notebookStore'
import { useTabsStore } from '@/stores/tabsStore'
import { v4 as uuidv4 } from 'uuid'
import { useDataFrameStore } from '@/stores/dataframeStore'

export function useNotebook() {
  const store = useNotebookStore()
  const tabsStore = useTabsStore()
  const dataframeStore = useDataFrameStore()

  // 创建新笔记本
  const createNewNotebook = async () => {
    try {
      // 创建新的标签页（不再在这里创建标签页，而是由TabsManager.vue中的createNewTab函数调用tabsStore.addTab）
      const tabId = tabsStore.addTab(null, '未命名')
      const sessionId = uuidv4()
      
      // 设置当前活动的笔记本
      store.setActiveNotebook(tabId)
      store.clearNotebookState()
      store.setSessionId(sessionId)
      
      // 添加一个代码单元格
      addCell('code')
      
      // 更新标签页的会话ID
      const tab = tabsStore.tabs.find(t => t.id === tabId)
      if (tab) {
        tab.sessionId = sessionId
      }
      
      return sessionId
    } catch (error) {
      console.error('创建新笔记本失败:', error)
      ElMessage.error('创建新笔记本失败')
    }
  }

  const _refreshDataFrame = async (session_id) => {
    try {
      await dataframeStore.fetchDataFrames(session_id)
    } catch (error) {
      console.error(error.message)
    }
  }

  // 打开笔记本
  const openNotebook = async (file) => {
    try {
      // 检查笔记本是否已经打开
      const existingTab = tabsStore.tabs.find(tab => tab.notebookFile === file.path)
      if (existingTab) {
        // 如果已经打开，直接激活该标签页
        tabsStore.activateTab(existingTab.id)
        return existingTab.id
      }
      
      // 创建新标签页
      const tabId = tabsStore.addTab(file, file.name.replace('.ipynb', ''))
      
      // 加载笔记本到新标签页
      const success = await store.loadNotebook(file, tabId)
      
      if (!success) {
        throw new Error('加载笔记本失败')
      }

      // 如果笔记本为空，添加一个代码单元格
      if (store.cells.length === 0) {
        addCell('code')
      }

      // 更新标签页的会话ID
      const tab = tabsStore.tabs.find(t => t.id === tabId)
      if (tab) {
        tab.sessionId = store.session_id
        tab.notebookFile = file.path
      }
      
      _refreshDataFrame(store.session_id)
      
      return tabId
    } catch (error) {
      console.error('打开笔记本失败:', error)
      ElMessage.error('打开笔记本失败')
      // 如果打开失败，创建一个新的笔记本
      return createNewNotebook()
    }
  }
 
  // 添加单元格
  const addCell = (type = 'code') => {
    const newCellId = uuidv4()
    
    // 获取当前cells数组的副本
    const cells = [...store.cells]
    cells.push(newCellId)
    store.setCells(cells)
    
    // 设置单元格内容和类型
    store.setCellContent(newCellId, '')
    store.setCellType(newCellId, type)
    
    // 根据类型设置相应的状态
    if (type === 'code') {
      store.setCellOutput(newCellId, {
        output: '',
        plot: '',
        plotly_html: '',
        status: 'idle'
      })
    } else if (type === 'markdown') {
      store.setMarkdownEditState(newCellId, true)
    }
    
    return newCellId
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
    store.setCellType(cellId, newType)
    
    // 根据新类型设置相应的状态
    if (newType === 'code') {
      store.setCellOutput(cellId, {
        output: '',
        plot: '',
        plotly_html: '',
        status: 'idle'
      })
    } else if (newType === 'markdown') {
      store.setMarkdownEditState(cellId, true)
    }

    // 重置单元格内容
    store.setCellContent(cellId, currentContent)
  }

  // 向上移动单元格
  const moveCellUp = (cellId) => {
    const cells = [...store.cells]
    const currentIndex = cells.indexOf(cellId)
    if (currentIndex > 0) {
      const temp = cells[currentIndex]
      cells[currentIndex] = cells[currentIndex - 1]
      cells[currentIndex - 1] = temp
      store.setCells(cells)
    }
  }

  // 向下移动单元格
  const moveCellDown = (cellId) => {
    const cells = [...store.cells]
    const currentIndex = cells.indexOf(cellId)
    if (currentIndex < cells.length - 1) {
      const temp = cells[currentIndex]
      cells[currentIndex] = cells[currentIndex + 1]
      cells[currentIndex + 1] = temp
      store.setCells(cells)
    }
  }

  // 导出PDF
  const exportPDF = async () => {
    try {
      if (!store.currentFile) {
        const fileName = prompt('请输入PDF文件名：')
        if (!fileName) return
        
        // 保存笔记本文件名
        await store.saveNotebook(fileName)
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
    const cells = [...store.cells]
    const index = cells.indexOf(cellId)
    if (index > -1) {
      // 从数组中移除单元格ID
      cells.splice(index, 1)
      store.setCells(cells)
      
      // 如果删除后没有单元格了，添加一个新的代码单元格
      if (cells.length === 0) {
        addCell('code')
      }
      
      return true
    }
    return false
  }

  // 在当前单元格上方添加新单元格
  const addCellAbove = (cellId) => {
    const cells = [...store.cells]
    const currentIndex = cells.indexOf(cellId)
    const newCellId = uuidv4()
    
    // 在当前单元格前插入新单元格
    cells.splice(currentIndex, 0, newCellId)
    store.setCells(cells)
    
    // 设置单元格内容和类型
    store.setCellContent(newCellId, '')
    store.setCellType(newCellId, 'code')
    store.setCellOutput(newCellId, {
      output: '',
      plot: '',
      plotly_html: '',
      status: 'idle'
    })
    
    return newCellId
  }

  // 在当前单元格下方添加新单元格
  const addCellBelow = (cellId) => {
    const cells = [...store.cells]
    const currentIndex = cells.indexOf(cellId)
    const newCellId = uuidv4()
    
    // 在当前单元格后插入新单元格
    cells.splice(currentIndex + 1, 0, newCellId)
    store.setCells(cells)
    
    // 设置单元格内容和类型
    store.setCellContent(newCellId, '')
    store.setCellType(newCellId, 'code')
    store.setCellOutput(newCellId, {
      output: '',
      plot: '',
      plotly_html: '',
      status: 'idle'
    })
    
    return newCellId
  }

  // 新增插入代码函数
  const insertCode = (code) => {
    const cells = [...store.cells]
    
    if (cells.length === 0 || store.cellContents[cells[cells.length - 1]] !== '') {
      // 添加新单元格
      const newCellId = addCell('code')
      store.setCellContent(newCellId, code)
    } else {
      // 使用最后一个空单元格
      store.setCellContent(cells[cells.length - 1], code)
    }
  }

  // 复制单元格
  const copyCell = (cellId) => {
    const newCellId = uuidv4()
    const cells = [...store.cells]
    const currentIndex = cells.indexOf(cellId)
    
    // 在当前单元格后插入新单元格
    cells.splice(currentIndex + 1, 0, newCellId)
    store.setCells(cells)
    
    // 复制单元格内容和类型
    const cellType = store.cellTypes[cellId]
    store.setCellType(newCellId, cellType)
    store.setCellContent(newCellId, store.cellContents[cellId] || '')
    
    // 根据类型设置相应的状态
    if (cellType === 'code') {
      store.setCellOutput(newCellId, {
        output: '',
        plot: '',
        plotly_html: '',
        status: 'idle'
      })
    } else if (cellType === 'markdown') {
      store.setMarkdownEditState(newCellId, true)
    }
    
    return newCellId
  }

  // 保存笔记本
  const saveNotebook = async (fileName = '') => {
    try {
      const success = await store.saveNotebook(fileName)
      
      if (success) {
        // 更新当前标签页的标题和修改状态
        if (tabsStore.activeTabId) {
          const displayName = fileName || store.currentFile?.replace('.ipynb', '') || '未命名'
          tabsStore.updateTabTitle(tabsStore.activeTabId, displayName)
          tabsStore.markTabAsModified(tabsStore.activeTabId, false)
          
          // 更新标签页的笔记本文件信息
          tabsStore.updateTabNotebook(tabsStore.activeTabId, store.currentFile)
        }
        
        ElMessage.success('笔记本保存成功')
        return true
      } else {
        throw new Error('保存笔记本失败')
      }
    } catch (error) {
      console.error('保存笔记本失败:', error)
      ElMessage.error('保存笔记本失败: ' + error.message)
      return false
    }
  }

  // 关闭笔记本
  const closeNotebook = (tabId) => {
    // 关闭标签页
    tabsStore.closeTab(tabId)
    
    // 关闭笔记本状态
    store.closeNotebook(tabId)
  }

  return {
    createNewNotebook,
    openNotebook,
    addCell,
    handleExecutionComplete,
    changeCellType,
    moveCellUp,
    moveCellDown,
    exportPDF,
    deleteCell,
    addCellAbove,
    addCellBelow,
    insertCode,
    copyCell,
    saveNotebook,
    closeNotebook
  }
}