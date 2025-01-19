<template>
  <el-dialog
    v-model="dialogVisible"
    title="AI 代码助手"
    width="50%"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    destroy-on-close
  >
    <el-input
      v-model="prompt"
      type="textarea"
      :rows="4"
      :placeholder="'例如：创建一个包含姓名和年龄的数据框，并计算年龄的平均值'"
      :disabled="loading"
      @keydown.ctrl.enter="handleGenerate"
    />
    
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
          :disabled="!prompt.trim()"
        >
          生成代码
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
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
const progress = ref(0)
const waitTime = ref(0)
let progressInterval = null
let waitTimer = null

const startProgress = () => {
  progress.value = 0
  progressInterval = setInterval(() => {
    if (progress.value < 90) {
      progress.value += Math.random() * 10
    }
  }, 1000)
}

const stopProgress = () => {
  if (progressInterval) {
    clearInterval(progressInterval)
    progressInterval = null
  }
  progress.value = 100
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

// 对话框可见性
const dialogVisible = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  dialogVisible.value = newVal
})

watch(dialogVisible, (newVal) => {
  emit('update:modelValue', newVal)
  if (!newVal) {
    // 重置状态
    prompt.value = ''
    progress.value = 0
    stopProgress()
    waitTime.value = 0
    stopWaitTimer()
  }
})

// 处理代码生成
const handleGenerate = async () => {
  if (!prompt.value.trim() || loading.value) return
  
  loading.value = true
  startProgress()
  startWaitTimer()
  
  try {
    const response = await axios.post('http://localhost:8000/api/ai/generate_code', {
      prompt: prompt.value,
      notebook_context: props.notebookContext,
      dataframe_info: props.dataframeInfo
    })
    
    if (response.data.status === 'success') {
      emit('code-generated', response.data.code)
      dialogVisible.value = false
    }
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '请求失败，请重试')
  } finally {
    stopProgress()
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

<style>
.loading-container {
  text-align: center;
  margin-top: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #909399;
}

.loading-icon {
  font-size: 20px;
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
</style> 