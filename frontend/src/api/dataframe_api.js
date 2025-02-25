import { apiCall, API_ENDPOINTS } from '@/api/http'

/**
 * 获取所有DataFrame列表
 * @param {string} session_id 会话ID 
 * @returns {Promise<Array<string>>} DataFrame名称列表
 */
export const listDataFrames = async (session_id) => {
  try {
    const result = await apiCall(API_ENDPOINTS.DATAFRAMES.LIST(session_id));
    if (result.status === "success") {
      return result.data;
    } else {
      throw new Error(result.message || '获取DataFrame列表失败');
    }
  } catch (error) {
    console.error('获取DataFrame列表失败:', error);
    throw error;
  }
};

/**
 * 获取指定DataFrame的详细信息
 * @param {string} session_id 会话ID
 * @param {string} name DataFrame名称
 * @returns {Promise<Object>} DataFrame的详细信息
 */
export const getDataFrameInfo = async (session_id, name) => {
  try {
    const result = await apiCall(API_ENDPOINTS.DATAFRAMES.INFO(session_id, name));
    if (result.status === "success") {
      return result.data;
    } else {
      throw new Error(result.message || '获取DataFrame信息失败');
    }
  } catch (error) {
    console.error('获取DataFrame信息失败:', error);
    throw error;
  }
};

/**
 * 获取指定DataFrame的预览信息
 * @param {string} name DataFrame名称
 * @returns {Promise<Object>} DataFrame的预览信息
 */
export const previewDataFrame = async (name) => {
  try {
    const result = await apiCall(API_ENDPOINTS.DATAFRAMES.PREVIEW(name));
    if (result.status === "success") {
      return result.data;
    } else {
      throw new Error(result.message || '获取DataFrame预览失败');
    }
  } catch (error) {
    console.error('获取DataFrame预览失败:', error);
    throw error;
  }
};

/**
 * 保存DataFrame到文件
 * @param {string} name DataFrame名称
 * @param {Object} options 保存选项
 * @param {string} options.filePath 文件路径
 * @param {string} options.fileType 文件类型（csv/excel）
 * @param {Object} options.saveOptions 保存选项
 * @returns {Promise<Object>} 保存结果
 */
export const saveDataFrame = async (name, options) => {
  try {
    const result = await apiCall(API_ENDPOINTS.DATAFRAMES.SAVE(name), {
      method: 'POST',
      body: JSON.stringify(options),
    });
    if (result.status === "success") {
      return result.data;
    } else {
      throw new Error(result.message || '保存DataFrame失败');
    }
  } catch (error) {
    console.error('保存DataFrame失败:', error);
    throw error;
  }
}; 