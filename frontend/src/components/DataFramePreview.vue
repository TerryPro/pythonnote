<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    width="80%"
    class="data-preview-dialog"
    :before-close="handleClose"
  >
    <template #header>
      <div class="dialog-header">
        <span>{{ title }}</span>
      </div>
    </template>
    <div v-if="loading" class="loading-container">
      <el-spinner></el-spinner>
      <p>加载数据中...</p>
    </div>
    <div v-else-if="error" class="error-container">
      <i class="fas fa-exclamation-circle"></i>
      <p>{{ error }}</p>
    </div>
    <div v-else class="data-preview">
      <!-- 基本信息 -->
      <div class="data-info">
        <div class="info-item">
          <span class="label">行数：</span>
          <span class="value">{{ previewData.basic_info?.行数 || 0 }}</span>
        </div>
        <div class="info-item">
          <span class="label">列数：</span>
          <span class="value">{{ previewData.basic_info?.列数 || 0 }}</span>
        </div>
        <div class="info-item">
          <span class="label">内存占用：</span>
          <span class="value">{{ previewData.basic_info?.内存占用 || '0 MB' }}</span>
        </div>
      </div>

      <!-- 列信息表格 -->
      <div class="columns-info">
        <h4>列信息</h4>
        <el-table 
          :data="previewData.columns || []" 
          border 
          style="width: 100%; margin-bottom: 20px"
          height="200"
          :max-height="200"
        >
          <el-table-column prop="name" label="列名" width="180" />
          <el-table-column prop="type" label="数据类型" width="180" />
          <el-table-column prop="null_count" label="空值数量" />
        </el-table>
      </div>

      <!-- 数据预览表格 -->
      <div class="preview-data">
        <h4>数据预览（前5行）</h4>
        <el-table
          :data="previewData.preview?.head || []"
          border
          style="width: 100%"
          height="300"
          :cell-class-name="getCellClass"
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

<script>
import { ElMessage } from 'element-plus'
import { getDataFrameInfo, saveDataFrame } from '@/api/dataframe_api'

export default {
  name: 'DataFramePreview',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'DataFrame预览'
    },
    dataframeName: {
      type: String,
      required: true
    }
  },
  emits: ['update:modelValue', 'save-success'],
  data() {
    return {
      loading: false,
      error: null,
      previewData: {},
      saveDialogVisible: false,
      saving: false,
      saveForm: {
        fileName: '',
        fileType: 'csv'
      }
    }
  },
  computed: {
    dialogVisible: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      }
    }
  },
  watch: {
    modelValue(newVal) {
      if (newVal && this.dataframeName) {
        this.loadPreview(this.dataframeName)
      }
    },
    dataframeName: {
      immediate: true,
      handler(newVal) {
        if (newVal && this.modelValue) {
          this.loadPreview(newVal)
        }
      }
    }
  },
  mounted() {
    if (this.modelValue && this.dataframeName) {
      this.loadPreview(this.dataframeName)
    }
  },
  methods: {
    handleClose() {
      this.dialogVisible = false
      this.reset()
    },
    reset() {
      this.loading = false
      this.error = null
      this.previewData = {}
    },
    formatCellValue(value) {
      if (value === null || value === undefined) return 'null'
      if (typeof value === 'number') {
        return value.toString()
      }
      if (typeof value === 'boolean') {
        return value.toString()
      }
      if (typeof value === 'object') {
        return JSON.stringify(value)
      }
      return value
    },
    getCellClass({ row, column }) {
      const value = row[column.property]
      if (value === null || value === undefined) {
        return 'null-cell'
      }
      return ''
    },
    async loadPreview(name) {
      this.loading = true
      this.error = null
      try {
        const data = await getDataFrameInfo(name)
        this.previewData = data
      } catch (err) {
        console.error('加载DataFrame预览失败:', err)
        this.error = err.message
      } finally {
        this.loading = false
      }
    },
    showSaveDialog() {
      this.saveDialogVisible = true
      this.saveForm.fileName = this.dataframeName
    },
    async handleSave() {
      if (!this.saveForm.fileName) {
        ElMessage.error('请输入文件名')
        return
      }
      
      if (!this.dataframeName) {
        ElMessage.error('DataFrame名称不能为空')
        return
      }
      
      this.saving = true
      try {
        const fileExtension = this.saveForm.fileType === 'csv' ? '.csv' : '.xlsx'
        const options = {
          file_path: this.saveForm.fileName + fileExtension,
          file_type: this.saveForm.fileType,
          save_options: {}
        }
        
        const result = await saveDataFrame(this.dataframeName, options)
        ElMessage.success('保存成功')
        this.saveDialogVisible = false
        
        this.$emit('save-success', result)
      } catch (error) {
        console.error('保存失败:', error)
        ElMessage.error(error.message || '保存失败')
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

<style scoped>
.data-preview-dialog {
  display: flex;
  flex-direction: column;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
}

.error-container {
  color: #f56c6c;
}

.error-container i {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.data-info {
  display: flex;
  gap: 2rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.info-item .label {
  font-weight: bold;
  color: #606266;
}

.columns-info,
.preview-data {
  margin-top: 1rem;
}

.columns-info h4,
.preview-data h4 {
  margin: 0 0 10px 0;
  color: #606266;
  font-size: 14px;
}

:deep(.null-cell) {
  color: #909399;
  font-style: italic;
}

.columns-info {
  margin-top: 1rem;
}

.columns-info h4 {
  margin: 0 0 10px 0;
  color: #606266;
  font-size: 14px;
}

:deep(.el-table) {
  --el-table-border-color: #dcdfe6;
  --el-table-header-background-color: #f5f7fa;
  border-radius: 4px;
  overflow: hidden;
}

:deep(.el-table__header-wrapper) {
  background-color: var(--el-table-header-background-color);
}

:deep(.el-table__header th) {
  background-color: var(--el-table-header-background-color);
  font-weight: bold;
  color: #606266;
  padding: 8px 0;
}

:deep(.el-table__body td) {
  padding: 8px;
}

:deep(.el-table__body-wrapper) {
  overflow-y: auto;
  scrollbar-width: thin;
}

:deep(.el-table__body-wrapper::-webkit-scrollbar) {
  width: 6px;
  height: 6px;
}

:deep(.el-table__body-wrapper::-webkit-scrollbar-thumb) {
  border-radius: 3px;
  background: #c0c4cc;
}

:deep(.el-table__body-wrapper::-webkit-scrollbar-track) {
  border-radius: 3px;
  background: #f5f7fa;
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 