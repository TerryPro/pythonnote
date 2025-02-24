<template>
  <el-dialog
    v-model="dialogVisible"
    width="50%"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    destroy-on-close
    :resize="false"
    class="ai-dialog-wrapper"
  >
    <template #title>
      <div class="dialog-header">
        <span>AI 代码助手</span>
        <div class="header-actions">
          <el-button-group>
            <el-button text @click="showPromptPanel = true" title="预定义提示词">
              <i class="fas fa-list-alt"></i>
            </el-button>
            <el-button text @click="userPromptConfigRef?.show()" title="设置">
              <i class="fas fa-cog"></i>
            </el-button>
          </el-button-group>
        </div>
      </div>
    </template>

    <div class="dialog-body">
      <!-- DataFrame选择器 -->
      <el-select
        v-model="selectedDataFrame"
        class="df-select"
        placeholder="请选择要操作的DataFrame"
        @change="handleDataFrameChange"
      >
        <el-option
          v-for="df in dataFrames"
          :key="df"
          :label="df"
          :value="df"
        />
      </el-select>

      <!-- DataFrame信息展示 -->
      <div class="df-info">
        <!-- 基本信息卡片 -->
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span>基本信息</span>
            </div>
          </template>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">行数：</span>
              <span class="value">{{ dataFrameInfo?.basic_info?.行数 }}</span>
            </div>
            <div class="info-item">
              <span class="label">列数：</span>
              <span class="value">{{ dataFrameInfo?.basic_info?.列数 }}</span>
            </div>
            <div class="info-item">
              <span class="label">内存占用：</span>
              <span class="value">{{ dataFrameInfo?.basic_info?.内存占用 }}</span>
            </div>
          </div>
        </el-card>

        <!-- 列信息表格 -->
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span>列信息</span>
            </div>
          </template>
          <el-table
            :data="dataFrameInfo?.columns || []"
            style="width: 100%"
            size="small"
            height="200"
          >
            <el-table-column prop="name" label="列名" min-width="180" />
            <el-table-column prop="type" label="数据类型" min-width="180" />
            <el-table-column prop="null_count" label="空值数量" min-width="100" />
          </el-table>
        </el-card>
      </div>

      <!-- 提示词输入 -->
      <el-input
        v-model="prompt"
        type="textarea"
        :rows="4"
        :placeholder="promptPlaceholder"
        :disabled="loading || !selectedDataFrame"
        @keydown.ctrl.enter="handleGenerate"
        class="prompt-input"
      />
      
      <!-- 加载提示 -->
      <div v-if="loading" class="loading-tip">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>正在生成代码，已等待 {{ waitTime }} 秒...</span>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleCancel" :disabled="loading">取消</el-button>
        <el-button
          type="primary"
          @click="handleGenerate"
          :loading="loading"
          :disabled="!prompt.trim() || !selectedDataFrame"
        >
          生成代码
        </el-button>
      </div>
    </template>
  </el-dialog>

  <!-- 用户提示词配置对话框 -->
  <UserPromptConfig ref="userPromptConfigRef" />

  <!-- 提示词面板 -->
  <el-dialog
    v-model="showPromptPanel"
    title="预定义提示词"
    width="80%"
    destroy-on-close
    class="prompt-panel-dialog"
  >
    <PromptPanel @use-prompt="usePrompt" />
  </el-dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { apiCall, API_ENDPOINTS } from '@/api/http'
import { Loading } from '@element-plus/icons-vue'
import UserPromptConfig from '@/components/config/UserPromptConfig.vue'
import PromptPanel from '../prompts/PromptPanel.vue'
import { useDataFrameStore } from '@/stores/dataframeStore'

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

// 添加DataFrame store
const dataframeStore = useDataFrameStore()

// 状态变量
const prompt = ref('')
const loading = ref(false)
const waitTime = ref(0)
let waitTimer = null

// DataFrame相关状态
const dataFrames = computed(() => dataframeStore.dataframes)
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

// 修改后的获取DataFrame列表方法
const fetchDataFrames = async () => {
}

// 修改后的获取DataFrame信息方法
const fetchDataFrameInfo = async (name) => {
  try {
    const data = await dataframeStore.fetchDataFrameInfo(name)
    dataFrameInfo.value = data
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
  if (!selectedDataFrame.value) {
    ElMessage.warning('请先选择要操作的DataFrame')
    return
  }
  
  if (!prompt.value.trim()) {
    ElMessage.warning('请输入提示词')
    return
  }

  loading.value = true
  startWaitTimer()
  
  try {
    const response = await apiCall(API_ENDPOINTS.AI.GENERATE_CODE, {
      body: {
        prompt: prompt.value,
        notebook_context: props.notebookContext,
        dataframe_info: dataFrameInfo.value,
        dataframe_name: selectedDataFrame.value
      },
      method: 'POST'
    })
    
    emit('code-generated', response.code)
    dialogVisible.value = false

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

// 提示词面板相关状态
const showPromptPanel = ref(false)

const usePrompt = (template) => {
  prompt.value = template
  showPromptPanel.value = false
}

// 显示配置对话框
const userPromptConfigRef = ref(null)

// 导出组件属性
defineExpose({
  show() {
    dialogVisible.value = true
  }
})
</script>

<style scoped>

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.dialog-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px 0;
  height: 100%;
  overflow: hidden;
}

.df-select {
  width: 100%;
  flex-shrink: 0;
}

.df-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
  flex: 1;
  overflow: auto;
}

.info-card {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 100px;
}

.info-card :deep(.el-card__body) {
  flex: 1;
  overflow: hidden;
  padding: 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding: 16px;
}

.card-header {
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.prompt-input {
  margin-top: 8px;
  flex-shrink: 0;
}

.loading-tip {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

</style>