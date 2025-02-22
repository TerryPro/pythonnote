import { defineStore } from 'pinia'
import { ref } from 'vue'
import { listDataFrames, getDataFrameInfo } from '@/api/dataframe_api'
import { ElMessage } from 'element-plus'

export const useDataFrameStore = defineStore('dataframe', () => {
  const dataframes = ref([])
  const currentDataframe = ref(null)
  const loading = ref(false)
  const error = ref(null)
  let refreshTimer = null

  // 获取DataFrame列表
  const fetchDataFrames = async () => {
    try {
      loading.value = true
      dataframes.value = await listDataFrames()
      error.value = null
    } catch (err) {
      error.value = err.message
      ElMessage.error('获取DataFrame列表失败: ' + err.message)
    } finally {
      loading.value = false
    }
  }

  // 获取单个DataFrame详情
  const fetchDataFrameInfo = async (name) => {
    try {
      return await getDataFrameInfo(name)
    } catch (err) {
      ElMessage.error('获取DataFrame信息失败: ' + err.message)
      return null
    }
  }

  // 启动自动刷新
  const startAutoRefresh = (interval = 30000) => {
    stopAutoRefresh()
    refreshTimer = setInterval(fetchDataFrames, interval)
  }

  // 停止自动刷新
  const stopAutoRefresh = () => {
    if (refreshTimer) {
      clearInterval(refreshTimer)
      refreshTimer = null
    }
  }

  return {
    dataframes,
    currentDataframe,
    loading,
    error,
    fetchDataFrames,
    fetchDataFrameInfo,
    startAutoRefresh,
    stopAutoRefresh
  }
}) 