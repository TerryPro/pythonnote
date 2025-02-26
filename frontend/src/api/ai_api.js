/**
 * ai_api.js
 * 管理所有与AI相关的API调用
 */

import { API_ENDPOINTS, apiCall } from './http'

/**
 * 获取系统提示词列表
 * @returns {Promise<Array>} 系统提示词列表
 */
export const fetchSystemPrompts = async () => {
  try {
    return await apiCall(API_ENDPOINTS.AI.SYSTEM_PROMPTS)
  } catch (error) {
    console.error('获取系统提示词失败:', error)
    throw error
  }
}

/**
 * 保存系统提示词
 * @param {Array<string>} prompts 系统提示词列表
 * @returns {Promise<Object>} 保存结果
 */
export const saveSystemPrompts = async (prompts) => {
  try {
    return await apiCall(API_ENDPOINTS.AI.SYSTEM_PROMPTS, {
      method: 'PUT',
      body: JSON.stringify({ prompts }),
    })
  } catch (error) {
    console.error('保存系统提示词失败:', error)
    throw error
  }
}

/**
 * 重置系统提示词为默认值
 * @returns {Promise<Object>} 重置结果
 */
export const resetSystemPrompts = async () => {
  try {
    return await apiCall(API_ENDPOINTS.AI.SYSTEM_PROMPTS_RESET, {
      method: 'POST'
    })
  } catch (error) {
    console.error('重置系统提示词失败:', error)
    throw error
  }
}

/**
 * 获取用户提示词列表
 * @returns {Promise<Array>} 用户提示词列表
 */
export const fetchUserPrompts = async () => {
  try {
    return await apiCall(API_ENDPOINTS.AI.USER_PROMPTS)
  } catch (error) {
    console.error('获取代码生成要求失败:', error)
    throw error
  }
}

/**
 * 保存用户提示词
 * @param {Array<string>} requirements 用户提示词列表
 * @returns {Promise<Object>} 保存结果
 */
export const saveUserPrompts = async (requirements) => {
  try {
    return await apiCall(API_ENDPOINTS.AI.USER_PROMPTS, {
      method: 'PUT',
      body: JSON.stringify({ requirements })
    })
  } catch (error) {
    console.error('保存代码生成要求失败:', error)
    throw error
  }
}

/**
 * 重置用户提示词为默认值
 * @returns {Promise<Object>} 重置结果
 */
export const resetUserPrompts = async () => {
  try {
    return await apiCall(API_ENDPOINTS.AI.RESET_USER_PROMPTS, {
      method: 'POST'
    })
  } catch (error) {
    console.error('重置代码生成要求失败:', error)
    throw error
  }
}

/**
 * 生成代码
 * @param {Object} params 生成代码所需参数
 * @param {string} params.prompt 用户输入的提示词
 * @param {Object} params.notebook_context 笔记本上下文
 * @param {Object} params.dataframe_info DataFrame信息
 * @param {string} params.dataframe_name DataFrame名称
 * @returns {Promise<Object>} 生成的代码
 */
export const generateCode = async (params) => {
  try {
    return await apiCall(API_ENDPOINTS.AI.GENERATE_CODE, {
      method: 'POST',
      body: params
    })
  } catch (error) {
    console.error('生成代码失败:', error)
    throw error
  }
} 