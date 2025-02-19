import { apiCall, API_ENDPOINTS } from '@/api/http'

/**
 * 加载数据文件列表
 * @returns {Promise<Array>} 数据文件列表
 */
export const listDataFiles = async () => {
  try {
    const result = await apiCall(API_ENDPOINTS.DATA_FILES.LIST)
    if (result.status === 'success') {
      return result.files || []
    } else {
      throw new Error(result.message || '获取数据文件列表失败')
    }
  } catch (error) {
    console.error('获取数据文件列表失败:', error)
    throw error
  }
}

/**
 * 上传 CSV 文件
 * @param {File} file 要上传的文件
 * @returns {Promise<Object>} 上传结果
 */
export const uploadCsvFile = async (file) => {
  try {

    console.log(file)
    const formData = new FormData()
    formData.append('file', file)
    console.log(formData)
    const result = await apiCall(API_ENDPOINTS.DATA_FILES.UPLOAD_CSV, {
      method: 'POST',
      body: formData,
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    if (result.status === 'success') {
      return result
    } else {
      throw new Error(result.message || '文件上传失败')
    }
  } catch (error) {
    console.error('文件上传失败:', error)
    throw error
  }
}

/**
 * 上传 Excel 文件
 * @param {File} file 要上传的文件
 * @returns {Promise<Object>} 上传结果
 */
export const uploadExcelFile = async (file) => {
  try {
    const formData = new FormData()
    formData.append('file', file)

    const result = await apiCall(API_ENDPOINTS.DATA_FILES.UPLOAD_EXCEL, {
      method: 'POST',
      body: formData,
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    if (result.status === 'success') {
      return result
    } else {
      throw new Error(result.message || '文件上传失败')
    }
  } catch (error) { 
    console.error('文件上传失败:', error)
    throw error
  }
}


/**
 * 删除数据文件
 * @param {string} filename 文件名
 * @returns {Promise<Object>} 删除结果
 */
export const api_deleteDataFile = async (filename) => {
  try {
    const result = await apiCall(API_ENDPOINTS.DATA_FILES.DELETE(filename), {
      method: 'DELETE'
    })

    if (result.status === 'success') {
      return result
    } else {
      throw new Error(result.message || '文件删除失败')
    }
  } catch (error) {
    console.error('文件删除失败:', error)
    throw error
  }
}

/**
 * 重命名数据文件
 * @param {string} oldFilename 原文件名
 * @param {string} newFilename 新文件名
 * @returns {Promise<Object>} 重命名结果
 */
export const api_renameDataFile = async (oldFilename, newFilename) => {
  try {
    const result = await apiCall(API_ENDPOINTS.DATA_FILES.RENAME, {
      method: 'POST',
      body: JSON.stringify({
        old_filename: oldFilename,
        new_filename: newFilename
      })
    })

    if (result.status === 'success') {
      return result
    } else {
      throw new Error(result.message || '文件重命名失败')
    }
  } catch (error) {
    console.error('文件重命名失败:', error)
    throw error
  }
}

/**
 * 预览 CSV 文件
 * @param {string} filename 文件名
 * @returns {Promise<Object>} 预览结果
 */
export const previewCsvFile = async (filename) => {
  try {
    const result = await apiCall(API_ENDPOINTS.DATA_FILES.PREVIEW_CSV(filename))

    if (result.status === 'success') {
      return result
    } else {
      throw new Error(result.message || '文件预览失败')
    }
  } catch (error) {
    console.error('文件预览失败:', error)
    throw error
  }
}

/**
 * 预览 Excel 文件
 * @param {string} filename 文件名
 * @returns {Promise<Object>} 预览结果
 */
export const previewExcelFile = async (filename) => {
  try {
    const result = await apiCall(API_ENDPOINTS.DATA_FILES.PREVIEW_EXCEL(filename))

    if (result.status === 'success') {
      return result
    } else {
      throw new Error(result.message || '文件预览失败')
    }
  } catch (error) {
    console.error('文件预览失败:', error)
    throw error
  }
} 