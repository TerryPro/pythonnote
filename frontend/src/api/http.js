import axios from 'axios';

// API基础配置
export const API_CONFIG = {
  BASE_URL: process.env.VUE_APP_API_BASE_URL,
  WS_BASE_URL: process.env.VUE_APP_WS_BASE_URL,
}

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

  // 数据框相关
  DATAFRAMES: {
    LIST: '/api/dataframes/list',
    PREVIEW: (name) => `/api/dataframes/preview/${name}`, // 获取DataFrame预览
    SAVE: (name) => `/api/dataframes/save/${name}`, // 保存DataFrame
    INFO: (name) => `/api/dataframes/info/${name}` // 获取DataFrame信息
  }, 

  // 导出相关
  EXPORT_PDF: {
    EXPORT: '/api/export/pdf',
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

// 配置axios默认值
axios.defaults.baseURL = API_CONFIG.BASE_URL;
axios.defaults.headers.common['Content-Type'] = 'application/json';
axios.defaults.timeout = REQUEST_CONFIG.timeout;

// 创建通用的API调用方法
export const apiCall = async (endpoint, options = {}) => {
  try {
    const response = await axios({
      url: endpoint, // 直接使用 endpoint，axios 会自动拼接 baseURL
      method: options.method || 'GET',
      headers: {
        ...options.headers,
      },
      data: options.body,
      params: options.params,
    });

    return response.data;
  } catch (error) {
    console.error('API调用失败:', error);
    if (error.response) {
      // 服务器返回了错误响应
      throw new Error(error.response.data.message || `HTTP error! status: ${error.response.status}`);
    } else if (error.request) {
      // 请求已发出，但没有收到响应
      throw new Error('网络错误，请检查您的网络连接');
    } else {
      // 其他错误
      throw new Error('请求失败，请重试');
    }
  }
};

// 新增的 downloadFile 函数
export const downloadFile = async (endpoint, filename, data) => {
  try {
    const response = await axios({
      url: endpoint, // 直接使用 endpoint，axios 会自动拼接 baseURL
      method: 'POST',
      data: data,
      responseType: 'blob', // 指定响应类型为 blob
    });

    // 获取文件并下载
    const blob = new Blob([response.data], { type: response.headers['content-type'] });
    const downloadUrl = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(downloadUrl);
    document.body.removeChild(a);
  } catch (error) {
    console.error('下载文件失败:', error);
    alert('下载文件失败: ' + error.message);
  }
}; 