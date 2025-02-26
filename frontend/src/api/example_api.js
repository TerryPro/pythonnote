/**
 * example_api.js
 * 管理所有与代码示例相关的API调用
 */

import { API_ENDPOINTS, apiCall } from '@/api/http'

/**
 * 获取所有代码示例分类
 * @returns {Promise<Array>} 分类列表
 */
export const fetchCategories = async () => {
  try {
    return await apiCall(API_ENDPOINTS.CODE_EXAMPLES.CATEGORIES)
  } catch (error) {
    console.error('获取分类失败:', error)
    throw error
  }
}

/**
 * 获取指定分类下的所有代码示例
 * @param {string} categoryId 分类ID
 * @returns {Promise<Array>} 代码示例列表
 */
export const fetchExamplesByCategory = async (categoryId) => {
  try {
    return await apiCall(API_ENDPOINTS.CODE_EXAMPLES.CATEGORIES_ID(categoryId))
  } catch (error) {
    console.error('获取示例失败:', error)
    throw error
  }
}

/**
 * 创建新的代码示例分类
 * @param {Object} categoryData 分类数据
 * @param {string} categoryData.name 分类名称
 * @param {string} categoryData.description 分类描述
 * @returns {Promise<Object>} 创建的分类
 */
export const createCategory = async (categoryData) => {
  try {
    return await apiCall(API_ENDPOINTS.CODE_EXAMPLES.CATEGORIES, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(categoryData)
    })
  } catch (error) {
    console.error('创建分类失败:', error)
    throw error
  }
}

/**
 * 更新代码示例分类
 * @param {string} categoryId 分类ID
 * @param {Object} categoryData 分类数据
 * @returns {Promise<Object>} 更新后的分类
 */
export const updateCategory = async (categoryId, categoryData) => {
  try {
    return await apiCall(API_ENDPOINTS.CODE_EXAMPLES.CATEGORIES_ID(categoryId), {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(categoryData)
    })
  } catch (error) {
    console.error('更新分类失败:', error)
    throw error
  }
}

/**
 * 创建新的代码示例
 * @param {Object} exampleData 示例数据
 * @param {string} exampleData.title 标题
 * @param {string} exampleData.description 描述
 * @param {string} exampleData.code 代码内容
 * @param {Array<string>} exampleData.tags 标签列表
 * @param {string} exampleData.category_id 分类ID
 * @returns {Promise<Object>} 创建的示例
 */
export const createExample = async (exampleData) => {
  try {
    return await apiCall(API_ENDPOINTS.CODE_EXAMPLES.CODE_EXAMPLES, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(exampleData)
    })
  } catch (error) {
    console.error('创建示例失败:', error)
    throw error
  }
}

/**
 * 更新代码示例
 * @param {string} exampleId 示例ID
 * @param {Object} exampleData 示例数据
 * @returns {Promise<Object>} 更新后的示例
 */
export const updateExample = async (exampleId, exampleData) => {
  try {
    return await apiCall(API_ENDPOINTS.CODE_EXAMPLES.CODE_EXAMPLES_ID(exampleId), {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(exampleData)
    })
  } catch (error) {
    console.error('更新示例失败:', error)
    throw error
  }
}

/**
 * 删除代码示例
 * @param {string} exampleId 示例ID
 * @returns {Promise<void>}
 */
export const deleteExample = async (exampleId) => {
  try {
    return await apiCall(API_ENDPOINTS.CODE_EXAMPLES.CODE_EXAMPLES_ID(exampleId), {
      method: 'DELETE'
    })
  } catch (error) {
    console.error('删除示例失败:', error)
    throw error
  }
}

/**
 * 从单元格保存代码示例
 * @param {Object} data 保存数据
 * @param {string} data.title 标题
 * @param {string} data.description 描述
 * @param {string} data.code 代码内容
 * @param {Array<string>} data.tags 标签列表
 * @param {string} data.category_id 分类ID
 * @returns {Promise<Object>} 保存的示例
 */
export const saveFromCell = async (data) => {
  try {
    return await apiCall(API_ENDPOINTS.CODE_EXAMPLES.SAVE_FROM_CELL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
  } catch (error) {
    console.error('保存示例失败:', error)
    throw error
  }
} 