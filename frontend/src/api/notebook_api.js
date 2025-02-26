import { apiCall, API_ENDPOINTS } from '@/api/http'

/**
 * 获取笔记本列表
 * @returns {Promise<Array>} 笔记本列表
 */
export const listNotebooks = async () => {
  try {
    const result = await apiCall(API_ENDPOINTS.NOTEBOOKS.LIST)
    if (result.status === 'success') {
      return result.data
    } else {
      throw new Error(result.message || '获取笔记本列表失败')
    }
  } catch (error) {
    console.error('获取笔记本列表失败:', error)
    throw error
  }
}

/**
 * 保存笔记本
 * @param {string} filename 文件名
 * @param {Object} notebook 笔记本内容
 * @returns {Promise<Object>} 保存结果
 */
export const saveNotebook = async (filename, notebook) => {
  try {
    const result = await apiCall(API_ENDPOINTS.NOTEBOOKS.SAVE, {
      method: 'POST',
      body: JSON.stringify({
        filename,
        notebook
      })
    })
    if (result.status === 'success') {
      return result
    } else {
      throw new Error(result.message || '保存笔记本失败')
    }
  } catch (error) {
    console.error('保存笔记本失败:', error)
    throw error
  }
}

/**
 * 重命名笔记本
 * @param {string} oldFilename 原文件名
 * @param {string} newFilename 新文件名
 * @returns {Promise<Object>} 重命名结果
 */
export const api_renameNotebook = async (oldFilename, newFilename) => {
  try {
    const result = await apiCall(API_ENDPOINTS.NOTEBOOKS.RENAME, {
      method: 'POST',
      body: JSON.stringify({
        old_filename: oldFilename,
        new_filename: newFilename
      })
    })
    if (result.status === 'success') {
      return result
    } else {
      throw new Error(result.message || '重命名笔记本失败')
    }
  } catch (error) {
    console.error('重命名笔记本失败:', error)
    throw error
  }
}

/**
 * 删除笔记本
 * @param {string} filename 文件名
 * @returns {Promise<Object>} 删除结果
 */
export const deleteNotebook = async (filename) => {
  try {
    const result = await apiCall(API_ENDPOINTS.NOTEBOOKS.DELETE(filename), {
      method: 'DELETE'
    })
    if (result.status === 'success') {
      return result
    } else {
      throw new Error(result.message || '删除笔记本失败')
    }
  } catch (error) {
    console.error('删除笔记本失败:', error)
    throw error
  }
}

/**
 * 加载笔记本内容
 * @param {string} filename 文件名
 * @returns {Promise<Object>} 笔记本内容
 */
export const loadNotebook = async (filename) => {
  try {
    const result = await apiCall(API_ENDPOINTS.NOTEBOOKS.LOAD(filename))
    if (result.status === 'success') {
      return result.data
    } else {
      throw new Error(result.message || '加载笔记本失败')
    }
  } catch (error) {
    console.error('加载笔记本失败:', error)
    throw error
  }
}

/**
 * 重置笔记本执行上下文
 * @param {string} session_id 会话ID
 * @returns {Promise<Object>} 重置结果
 */
export const resetNotebook = async (session_id) => {
  try {
    const result = await apiCall(API_ENDPOINTS.EXECUTION.RESET_CONTEXT, {
      method: 'POST',
      body: { session_id: session_id }
    })
    if (result.status === 'success') {
      return result
    } else {
      throw new Error(result.message || '重置笔记本失败')
    }
  } catch (error) {
    console.error('重置笔记本失败:', error)
    throw error
  }
}

