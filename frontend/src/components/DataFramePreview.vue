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
      <div class="data-info">
        <div class="info-item">
          <span class="label">行数：</span>
          <span class="value">{{ previewData.shape?.[0] || 0 }}</span>
        </div>
        <div class="info-item">
          <span class="label">列数：</span>
          <span class="value">{{ previewData.shape?.[1] || 0 }}</span>
        </div>
        <div class="info-item">
          <span class="label">内存占用：</span>
          <span class="value">{{ formatMemoryUsage(previewData.memory_usage) }}</span>
        </div>
      </div>

      <div class="data-table">
        <el-table
          :data="tableData"
          border
          style="width: 100%"
          height="400"
          :cell-class-name="getCellClass"
        >
          <el-table-column
            v-for="(type, col) in previewData.columns"
            :key="col"
            :prop="col"
            :label="`${col} (${type})`"
            :min-width="120"
          >
            <template #default="scope">
              <span :title="scope.row[col]">{{ formatCellValue(scope.row[col]) }}</span>
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
      previewData: {},
      tableData: []
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
      this.tableData = []
    },
    formatMemoryUsage(bytes) {
      if (!bytes) return '0 B'
      const units = ['B', 'KB', 'MB', 'GB']
      let size = bytes
      let unitIndex = 0
      while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024
        unitIndex++
      }
      return `${size.toFixed(2)} ${units[unitIndex]}`
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
        const response = await fetch(`http://localhost:8000/api/dataframe/preview/${name}`)
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        if (data.status === 'success') {
          this.previewData = data
          this.tableData = Object.keys(data.sample_data).length > 0
            ? Array.from({ length: Object.values(data.sample_data)[0].length }, (_, i) => {
                const row = {}
                Object.keys(data.sample_data).forEach(col => {
                  row[col] = data.sample_data[col][i]
                })
                return row
              })
            : []
        } else {
          throw new Error(data.message || '加载数据失败')
        }
      } catch (err) {
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

.data-table {
  flex: 1;
  overflow: auto;
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