<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    width="80%"
    class="data-preview-dialog"
    :before-close="handleClose"
  >
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
        <el-table :data="previewData.columns || []" border style="width: 100%; margin-bottom: 20px">
          <el-table-column prop="name" label="列名" />
          <el-table-column prop="type" label="数据类型" />
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
  </el-dialog>
</template>

<script>
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
    }
  },
  emits: ['update:modelValue'],
  data() {
    return {
      loading: false,
      error: null,
      previewData: {}
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
        const response = await fetch(`http://localhost:8000/api/dataframes/info/${name}`)
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        this.previewData = data
      } catch (err) {
        console.error('加载DataFrame预览失败:', err)
        this.error = err.message
      } finally {
        this.loading = false
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

:deep(.el-table) {
  --el-table-border-color: #dcdfe6;
  --el-table-header-background-color: #f5f7fa;
}

:deep(.el-table th) {
  background-color: var(--el-table-header-background-color);
  font-weight: bold;
}

:deep(.el-table td) {
  padding: 8px 0;
}
</style> 