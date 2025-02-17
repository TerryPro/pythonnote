// API基础配置
export const API_CONFIG = {
  BASE_URL: process.env.VUE_APP_API_BASE_URL,
  WS_BASE_URL: process.env.VUE_APP_WS_BASE_URL,
}

console.log('Loaded VUE_APP_API_BASE_URL:', process.env.VUE_APP_API_BASE_URL)

// API端点配置
export const API_ENDPOINTS = {
  // 数据文件相关
  DATA_FILES: {
    LIST: '/api/data-files/list',
    PREVIEW_CSV: (filename) => `/api/data-files/preview/csv?filename=${filename}`,
    PREVIEW_EXCEL: (filename) => `/api/data-files/preview/excel?filename=${filename}`,
    UPLOAD_CSV: '/api/data-files/upload/csv',
    UPLOAD_EXCEL: '/api/data-files/upload/excel',
    DELETE: (filename) => `/api/data-files/delete?filename=${filename}`,
    RENAME: '/api/data-files/rename'
  },
  
  // 笔记本相关
  NOTEBOOKS: {
    LIST: '/api/notebooks/list_notebooks',
    SAVE: '/api/notebooks/save_notebook',
    RENAME: '/api/notebooks/rename_notebook',
    DELETE: (filename) => `/api/notebooks/delete_notebook?filename=${filename}`,
    LOAD: (filename) => `/api/notebooks/load_notebook?filename=${filename}`
  },
  
  // AI相关
  AI: {
    SYSTEM_PROMPTS: '/api/ai/system-prompts',
    SYSTEM_PROMPTS_RESET: '/api/ai/system-prompts/reset',
    USER_PROMPTS: '/api/ai/user-prompts',
    RESET_USER_PROMPTS: '/api/ai/user-prompts/reset',
  },
  
  // 代码示例相关
  CODE_EXAMPLES: {
    CATEGORIES: '/api/code-examples/categories',
    CATEGORIES_ID: (categoryId) => `/api/code-examples/category/${categoryId}`,
    CODE_EXAMPLES: '/api/code-examples',
    CODE_EXAMPLES_ID: (exampleId) => `/api/code-examples/${exampleId}`,
    SAVE_FROM_CELL: '/api/code-examples/save-from-cell',
  },
  
  // 提示词相关
  PROMPTS: {
    CATEGORIES: '/api/prompt/categories',
    LIST: (categoryId) => `/api/prompt/category/${categoryId}`,
    CREATE: '/api/prompt',
    UPDATE: '/api/prompt',
  },

  EXECUTION: {
    RESET_CONTEXT: '/api/execution/reset_context'
  },

  DATAFRAMES: {
    LIST: '/api/dataframes/list'
  },

  SYSTEM: {
    VERSION: '/api/system/version'
  }
}

// 构建完整的API URL
export const getApiUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${endpoint}`
}

// 构建WebSocket URL
export const getWsUrl = (endpoint) => {
  return `${API_CONFIG.WS_BASE_URL}${endpoint}`
}

// HTTP请求配置
export const REQUEST_CONFIG = {
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30秒超时
}

// 创建通用的API调用方法
export const apiCall = async (endpoint, options = {}) => {
  try {
    const response = await fetch(getApiUrl(endpoint), {
      ...REQUEST_CONFIG,
      ...options,
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('API调用失败:', error)
    throw error
  }
} 