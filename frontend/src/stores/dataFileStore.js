import { defineStore } from 'pinia'
import { 
  listDataFiles,
  uploadCsvFile,
  uploadExcelFile,
  api_deleteDataFile,
  api_renameDataFile,
  previewCsvFile,
  previewExcelFile
} from '@/api/datafile_api'

/**
 * 数据文件管理Store
 * 负责集中管理所有数据文件相关状态和业务逻辑
 */
export const useDataFileStore = defineStore('dataFiles', {
  state: () => ({
    // 状态树
    files: [],          // 全部数据文件列表
    currentFile: null,  // 当前选中文件路径
    loading: false,     // 全局加载状态
    error: null,        // 最后发生的错误信息
    previewData: null   // 文件预览数据
  }),

  getters: {
    /**
     * 当前文件元数据
     * @returns {Object|null} 当前文件的完整元数据对象
     */
    currentFileMeta: (state) => state.files.find(f => f.path === state.currentFile)
  },

  actions: {
    /**
     * 初始化加载文件列表
     * 会自动处理加载状态和错误捕获
     */
    async loadFiles() {
      this.loading = true
      try {
        const response = await listDataFiles()
        // 标准化文件对象结构
        this.files = response.map(file => ({
          name: file.name,
          path: file.path,
          size: file.size || 0,
          lastModified: file.lastModified || Date.now(),
          type: file.name.split('.').pop().toLowerCase()
        }))
        this.error = null
      } catch (error) {
        this.handleError(error, '加载文件列表失败')
      } finally {
        this.loading = false
      }
    },

    /**
     * 统一错误处理方法
     * @param {Error} error - 原始错误对象
     * @param {string} defaultMsg - 默认错误提示
     */
    handleError(error, defaultMsg) {
      this.error = error.message || defaultMsg
      console.error('[DataFileStore]', error)
      // 可以在此扩展错误通知逻辑
    },

    /**
     * 通用文件上传方法
     * @param {File} file - 要上传的文件对象
     * @returns {Promise} 上传结果
     */
    async uploadFile(file) {
      const fileType = file.name.split('.').pop().toLowerCase()
      try {
        // 根据类型选择上传器
        const uploader = fileType === 'csv' ? uploadCsvFile : uploadExcelFile
        const result = await uploader(file)
        
        // 刷新文件列表
        await this.loadFiles()
        return result
      } catch (error) {
        this.handleError(error, '文件上传失败')
        throw error // 抛出错误供组件处理
      }
    },

    /**
     * 删除文件
     * @param {string} filePath - 要删除的文件路径
     */
    async deleteFile(filePath) {
      try {
        await api_deleteDataFile(filePath)
        await this.loadFiles()
        
        // 如果删除的是当前文件，清空选中状态
        if (this.currentFile === filePath) {
          this.currentFile = null
        }
      } catch (error) {
        this.handleError(error, '文件删除失败')
        throw error
      }
    },

    /**
     * 重命名文件
     * @param {string} oldPath - 原始文件路径
     * @param {string} newName - 新文件名（不带扩展名）
     */
    async renameFile(oldPath, newName) {
      try {
        const oldFile = this.files.find(f => f.path === oldPath)
        if (!oldFile) throw new Error('文件不存在')
        
        // 保留原扩展名
        const extension = oldFile.name.split('.').pop()
        const newFileName = `${newName}.${extension}`
        
        await api_renameDataFile(oldPath, newFileName)
        await this.loadFiles()
        
        // 更新当前选中文件
        if (this.currentFile === oldPath) {
          this.currentFile = newFileName
        }
      } catch (error) {
        this.handleError(error, '重命名失败')
        throw error
      }
    },

    /**
     * 预览文件数据
     * @param {string} filePath - 要预览的文件路径
     */
    async previewFile(filePath) {
      try {
        const file = this.files.find(f => f.path === filePath)
        if (!file) throw new Error('文件不存在')
        
        // 根据文件类型调用不同预览方法
        const previewer = file.type === 'csv' 
          ? previewCsvFile 
          : previewExcelFile
        
        console.log('previewer:', previewer)
        console.log('filePath:', filePath)
        this.previewData = await previewer(filePath)
        return this.previewData
      } catch (error) {
        this.handleError(error, '预览失败')
        throw error
      }
    }
  }
}) 