<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    width="60%"
    :before-close="handleClose"
  >
    <template #header>
      <div class="dialog-header">
        <span>{{ title }}</span>
      </div>
    </template>
    <div>
      <div v-if="loading" class="loading-container">
        <el-spinner></el-spinner>
        <p>加载数据中...</p>
      </div>
      
      <div v-else-if="error" class="error-container">
        <i class="fas fa-exclamation-circle"></i>
        <p>{{ error }}</p>
      </div>
      
      <div v-else class="data-preview" style="margin-bottom: 5px">
        <el-descriptions :border="true" column="3">
          <el-descriptions-item label="行数">{{ previewData.basic_info?.行数 || 0 }}</el-descriptions-item>
          <el-descriptions-item label="列数">{{ previewData.basic_info?.列数 || 0 }}</el-descriptions-item>
          <el-descriptions-item label="内存占用">{{ previewData.basic_info?.内存占用 || '0 MB' }}</el-descriptions-item>
        </el-descriptions>
      </div>

      <!-- 列信息表格 -->
      <div class="columns-info">
        <el-table 
          :data="previewData.columns || []" 
          border 
          style="width: 100%; margin-bottom: 5px"
          :max-height="250"
        >
          <el-table-column prop="name" label="列名" width="180" />
          <el-table-column prop="type" label="数据类型" width="180" />
          <el-table-column prop="null_count" label="空值数量" />
        </el-table>
      </div>

      <!-- 数据预览表格 -->
      <div class="preview-data">
        <el-table
          v-if="previewData.preview?.head?.length > 0"
          :data="previewData.preview?.head || []"
          border
          style="width: 100%"
          :max-height="250"
          :key="'table-'+previewData.preview?.head?.length"
          :cell-class-name="getCellClass"
          v-loading="loading"
          element-loading-background="rgba(255, 255, 255, 0.7)"
        >
          <el-table-column
            v-for="col in previewData.columns || []"
            :key="col.name"
            :prop="col.name"
            :label="col.name"
            :min-width="120"
          >
            <template #default="scope">
              <span :title="scope.row[col.name]">{{ formatCellValue(scope.row[col.name]) }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="showSaveDialog">保存数据到文件</el-button>
        <el-button @click="handleClose">关闭</el-button>
      </span>
    </template>

    <el-dialog
      v-model="saveDialogVisible"
      title="保存数据"
      width="30%"
      append-to-body
    >
      <el-form :model="saveForm" label-width="100px">
        <el-form-item label="文件名">
          <el-input v-model="saveForm.fileName" placeholder="请输入文件名"></el-input>
        </el-form-item>
        <el-form-item label="文件类型">
          <el-select v-model="saveForm.fileType" placeholder="请选择文件类型">
            <el-option label="CSV文件" value="csv"></el-option>
            <el-option label="Excel文件" value="excel"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="saveDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSave" :loading="saving">
            保存
          </el-button>
        </span>
      </template>
    </el-dialog>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getDataFrameInfo, saveDataFrame } from '@/api/dataframe_api'
import { debounce } from 'lodash-es'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'DataFrame预览'
  },
  sessionId: {
    type: String,
    required: true
  },
  dataframeName: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'save-success'])

// 响应式状态
const loading = ref(false)
const error = ref(null)
const previewData = ref({})
const saveDialogVisible = ref(false)
const saving = ref(false)
const saveForm = ref({
  fileName: '',
  fileType: 'csv'
})

// 计算属性
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 方法
const handleClose = () => {
  dialogVisible.value = false
  reset()
}

const reset = () => {
  loading.value = false
  error.value = null
  previewData.value = {}
}

const formatCellValue = (value) => {
  if (value === null || value === undefined) return 'null'
  if (typeof value === 'number') return value.toString()
  if (typeof value === 'boolean') return value.toString()
  if (typeof value === 'object') return JSON.stringify(value)
  return value
}

const loadPreview = async (session_id, name) => {
  loading.value = true
  error.value = null
  try {
    previewData.value = await getDataFrameInfo(session_id, name)
  } catch (err) {
    console.error('加载DataFrame预览失败:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const showSaveDialog = () => {
  saveDialogVisible.value = true
  saveForm.value.fileName = props.dataframeName
}

const handleSave = async () => {
  if (!saveForm.value.fileName) {
    ElMessage.error('请输入文件名')
    return
  }
  if (!props.dataframeName) {
    ElMessage.error('DataFrame名称不能为空')
    return
  }

  saving.value = true
  try {
    const fileExtension = saveForm.value.fileType === 'csv' ? '.csv' : '.xlsx'
    const options = {
      file_path: saveForm.value.fileName + fileExtension,
      file_type: saveForm.value.fileType,
      save_options: {}
    }
    
    const result = await saveDataFrame(props.dataframeName, options)
    ElMessage.success('保存成功')
    saveDialogVisible.value = false
    emit('save-success', result)
  } catch (err) {
    console.error('保存失败:', err)
    ElMessage.error(err.message || '保存失败')
  } finally {
    saving.value = false
  }
}

// 监听器
watch(
  [() => props.modelValue, ()=>props.sessionId, () => props.dataframeName],
  debounce(([newModelVal, newsessionId, newDfName]) => {
    if (newModelVal && newsessionId && newDfName) {
      loadPreview(newsessionId, newDfName)
    }
  }, 100),
  { immediate: true }
)

// 生命周期钩子
onMounted(() => {
  if (props.modelValue && props.sessionId && props.dataframeName) {
    loadPreview(props.sessionId, props.dataframeName)
  }

  // 修复ResizeObserver报错
  if (window.ResizeObserver) {
    window.ResizeObserver = class extends ResizeObserver {
      constructor(callback) {
        callback = debounce(callback, 100)
        super(callback)
        this.callback = callback
      }
      observe(target, options) {
        super.observe(target, options)
      }
    }
  }
})
</script>

<style scoped>
/* 保持Element Plus默认样式 */
</style> 