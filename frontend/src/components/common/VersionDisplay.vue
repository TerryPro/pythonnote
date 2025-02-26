<template>
  <span class="version">{{ version }}</span>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { API_ENDPOINTS, apiCall } from '@/api/http'

const version = ref('加载中...')

// 获取版本信息
const fetchVersion = async () => {
  try {
    const result = await apiCall(API_ENDPOINTS.SYSTEM.VERSION)
    version.value = result.data.version
  } catch (error) {
    console.error('获取版本信息失败:', error)
    version.value = '未知版本'
  }
}

onMounted(async () => {
  await fetchVersion()
})
</script>

<style scoped lang="scss">
</style>