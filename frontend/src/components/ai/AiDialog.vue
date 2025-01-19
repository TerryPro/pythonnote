<template>
  <el-dialog
    v-model="dialogVisible"
    title="AI 代码助手"
    width="50%"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    destroy-on-close
  >
    <!-- DataFrame选择器 -->
    <div class="dataframe-selector">
      <el-select
        v-model="selectedDataFrame"
        placeholder="选择要操作的DataFrame"
        clearable
        @change="handleDataFrameChange"
        style="width: 100%"
      >
        <el-option
          v-for="df in dataFrames"
          :key="df"
          :label="df"
          :value="df"
        />
      </el-select>
    </div>

    <!-- DataFrame信息展示 -->
    <div v-if="dataFrameInfo" class="dataframe-info">
      <!-- 基本信息卡片 -->
      <div class="info-card">
        <div class="info-item">
          <span class="info-label">行数：</span>
          <span class="info-value">{{ dataFrameInfo.basic_info?.行数 }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">列数：</span>
          <span class="info-value">{{ dataFrameInfo.basic_info?.列数 }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">内存占用：</span>
          <span class="info-value">{{ dataFrameInfo.basic_info?.内存占用 }}</span>
        </div>
      </div>

      <!-- 列信息表格 -->
      <div class="columns-info">
        <div class="section-title">列信息</div>
        <el-table
          :data="dataFrameInfo.columns"
          size="small"
          style="width: 100%"
          :height="200"
        >
          <el-table-column prop="name" label="列名" min-width="120" />
          <el-table-column prop="type" label="数据类型" min-width="120" />
          <el-table-column prop="null_count" label="空值数量" min-width="100" />
        </el-table>
      </div>
    </div>

    <!-- 提示词输入 -->
    <el-input
      v-model="prompt"
      type="textarea"
      :rows="4"
      :placeholder="promptPlaceholder"
      :disabled="loading || !selectedDataFrame"
      @keydown.ctrl.enter="handleGenerate"
    />
    
    <!-- 加载提示 -->
    <div v-if="loading" class="loading-container">
      <el-icon class="loading-icon"><Loading /></el-icon>
      <span>正在生成代码，已等待 {{ waitTime }} 秒...</span>
    </div>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleCancel" :disabled="loading">取消</el-button>
        <el-button
          type="primary"
          @click="handleGenerate"
          :loading="loading"
          :disabled="!prompt.trim() || !selectedDataFrame"
        >
          生成代码
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  notebookContext: {
    type: Object,
    default: () => ({})
  },
  dataframeInfo: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'code-generated'])

// 状态变量
const prompt = ref('')
const loading = ref(false)
const waitTime = ref(0)
let waitTimer = null

// DataFrame相关状态
const dataFrames = ref([])
const selectedDataFrame = ref('')
const dataFrameInfo = ref(null)

// 计算属性
const promptPlaceholder = computed(() => {
  return selectedDataFrame.value
    ? `请描述您要对 ${selectedDataFrame.value} 进行什么操作`
    : '请先选择要操作的DataFrame'
})

// 对话框可见性
const dialogVisible = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  dialogVisible.value = newVal
})

watch(dialogVisible, (newVal) => {
  emit('update:modelValue', newVal)
  if (newVal) {
    fetchDataFrames()
  } else {
    resetState()
  }
})

const resetState = () => {
  prompt.value = ''
  waitTime.value = 0
  stopWaitTimer()
  selectedDataFrame.value = ''
  dataFrameInfo.value = null
}

const startWaitTimer = () => {
  waitTime.value = 0
  waitTimer = setInterval(() => {
    waitTime.value++
  }, 1000)
}

const stopWaitTimer = () => {
  if (waitTimer) {
    clearInterval(waitTimer)
    waitTimer = null
  }
}

// 获取所有DataFrame列表
const fetchDataFrames = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/dataframes/list')
    dataFrames.value = response.data
  } catch (e) {
    ElMessage.error('获取DataFrame列表失败')
  }
}

// 获取选中DataFrame的信息
const fetchDataFrameInfo = async (name) => {
  try {
    const response = await axios.get(`http://localhost:8000/api/dataframes/info/${name}`)
    dataFrameInfo.value = response.data
  } catch (e) {
    ElMessage.error('获取DataFrame信息失败')
    dataFrameInfo.value = null
  }
}

// 处理DataFrame选择变化
const handleDataFrameChange = async (value) => {
  if (value) {
    loading.value = true
    try {
      await fetchDataFrameInfo(value)
    } catch (e) {
      ElMessage.error('获取DataFrame信息失败')
      dataFrameInfo.value = null
    } finally {
      loading.value = false
    }
  } else {
    dataFrameInfo.value = null
  }
}

// 处理代码生成
const handleGenerate = async () => {
  if (!prompt.value.trim() || loading.value || !selectedDataFrame.value) return
  
  loading.value = true
  startWaitTimer()
  
  try {
    const response = await axios.post('http://localhost:8000/api/ai/generate_code', {
      prompt: prompt.value,
      notebook_context: props.notebookContext,
      dataframe_info: dataFrameInfo.value,
      dataframe_name: selectedDataFrame.value
    })
    
    if (response.data.status === 'success') {
      emit('code-generated', response.data.code)
      dialogVisible.value = false
    }
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '请求失败，请重试')
  } finally {
    stopWaitTimer()
    loading.value = false
  }
}

// 处理取消
const handleCancel = () => {
  if (loading.value) return
  dialogVisible.value = false
}
</script>

<style scoped>
.dataframe-selector {
  margin-bottom: 16px;
}

.dataframe-info {
  margin: 16px 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-card {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding: 16px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.info-value {
  font-size: 14px;
  color: var(--el-text-color-primary);
  font-weight: 500;
}

.columns-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.section-title {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  font-weight: 500;
}

.loading-container {
  margin-top: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--el-text-color-secondary);
}

.loading-icon {
  font-size: 18px;
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

:deep(.el-table) {
  --el-table-border-color: var(--el-border-color-lighter);
  --el-table-header-background-color: var(--el-fill-color-light);
  --el-table-row-hover-background-color: var(--el-fill-color);
}

:deep(.el-table th) {
  background-color: var(--el-table-header-background-color);
  font-weight: 500;
  color: var(--el-text-color-regular);
}

:deep(.el-table td) {
  padding: 4px 0;
}
</style> 