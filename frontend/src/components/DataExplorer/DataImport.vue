<template>
  <div class="data-import">
    <!-- 数据预览对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="数据预览"
      width="80%"
      :close-on-click-modal="false"
      :close-on-press-escape="true"
      destroy-on-close
    >
      <div v-if="previewData" class="preview-container">
        <!-- 文件信息 -->
        <div class="file-info">
          <h3>文件信息</h3>
          <div class="info-grid">
            <div v-for="(value, key) in previewData.file_info" :key="key" class="info-item">
              <span class="info-label">{{ key }}:</span>
              <span class="info-value">{{ value }}</span>
            </div>
          </div>
        </div>

        <!-- 数据基本信息 -->
        <div class="data-info">
          <h3>数据信息</h3>
          <div class="info-grid">
            <div v-for="(value, key) in previewData.info" :key="key" class="info-item">
              <span class="info-label">{{ key }}:</span>
              <span class="info-value">
                {{ Array.isArray(value) ? value.join(', ') : value }}
              </span>
            </div>
          </div>
        </div>

        <!-- 数据预览表格 -->
        <div class="data-preview">
          <h3>数据预览</h3>
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th v-for="column in previewData.info.列名" :key="column">
                    {{ column }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in previewData.head" :key="index">
                  <td v-for="column in previewData.info.列名" :key="column">
                    {{ row[column] }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 代码生成区域 -->
        <div class="code-generation">
          <h3>数据操作代码生成</h3>
          <div class="code-actions">
            <div class="code-action-group">
              <h4>基础操作</h4>
              <el-button type="primary" @click="insertDataLoadCode">
                生成数据加载代码
              </el-button>
              <el-button type="primary" @click="insertDataAnalysisCode">
                生成数据分析代码
              </el-button>
              <el-button type="success" @click="insertAllCode">
                生成全部代码
              </el-button>
            </div>
            <div class="code-action-group">
              <h4>数据可视化</h4>
              <el-button type="primary" @click="insertDataVisualizationCode">
                生成可视化代码
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 错误提示 -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeDialog">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ElButton, ElDialog, ElMessage } from 'element-plus'

export default {
  name: 'DataImport',
  components: {
    ElButton,
    ElDialog
  },
  props: {
    currentFile: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      previewData: null,
      loading: false,
      error: null,
      dialogVisible: false,
      currentPreviewFile: null
    }
  },
  methods: {
    showPreview() {
      this.dialogVisible = true
    },
    closeDialog() {
      this.dialogVisible = false
      this.currentPreviewFile = null
    },
    async processFile(file) {
      this.loading = true
      this.error = null
      
      try {
        const formData = new FormData()
        formData.append('file', file)
        
        // 根据文件类型选择不同的上传端点
        const fileType = file.name.split('.').pop().toLowerCase()
        let endpoint = ''
        
        if (fileType === 'csv') {
          endpoint = 'http://localhost:8000/api/data-files/upload/csv'
        } else if (['xlsx', 'xls'].includes(fileType)) {
          endpoint = 'http://localhost:8000/api/data-files/upload/excel'
        } else {
          throw new Error('不支持的文件格式')
        }
        
        const response = await fetch(endpoint, {
          method: 'POST',
          body: formData
        })
        
        if (!response.ok) {
          throw new Error(`上传失败: ${response.status} ${response.statusText}`)
        }
        
        const result = await response.json()
        console.log('Upload response:', result)
        
        if (result.status === 'success') {
          this.previewData = result.data
          this.$emit('data-loaded', result.data)
        } else {
          throw new Error(result.message || '上传失败')
        }
      } catch (error) {
        this.error = error.message
        console.error('上传错误:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    // 生成数据加载代码
    generateDataLoadCode() {
      if (!this.currentPreviewFile) {
        ElMessage.warning('请先选择一个数据文件')
        return ''
      }
      const varName = this.currentPreviewFile.name.split('.')[0].replace(/[^a-zA-Z0-9]/g, '_').toLowerCase() + '_df'
      const filePath = this.currentPreviewFile.path
      const fileType = this.currentPreviewFile.name.split('.').pop().toLowerCase()
      
      let code = '# 导入必要的库\nimport pandas as pd\n\n'
      
      if (fileType === 'csv') {
        code += `# 加载CSV文件\n${varName} = pd.read_csv('data/${filePath}')\n`
      } else {
        code += `# 加载Excel文件\n${varName} = pd.read_excel('data/${filePath}')\n`
      }
      
      code += `\n# 显示数据基本信息\nprint("数据基本信息：")\nprint(${varName}.info())\n\n`
      code += `# 显示前几行数据\nprint("\\n数据预览：")\nprint(${varName}.head())\n`
      
      return code
    },
    // 生成数据分析示例代码
    generateDataAnalysisCode() {
      if (!this.currentPreviewFile) {
        ElMessage.warning('请先选择一个数据文件')
        return ''
      }
      const varName = this.currentPreviewFile.name.split('.')[0].replace(/[^a-zA-Z0-9]/g, '_').toLowerCase() + '_df'
      
      let code = '# 数据基本统计分析\n'
      code += `print("基本统计信息：")\nprint(${varName}.describe())\n\n`
      code += `# 检查缺失值\nprint("\\n缺失值统计：")\nprint(${varName}.isnull().sum())\n\n`
      code += `# 数据类型信息\nprint("\\n数据类型信息：")\nprint(${varName}.dtypes)\n`
      
      return code
    },
    // 生成数据可视化示例代码
    generateVisualizationCode() {
      if (!this.currentPreviewFile) {
        ElMessage.warning('请先选择一个数据文件')
        return ''
      }
      const varName = this.currentPreviewFile.name.split('.')[0].replace(/[^a-zA-Z0-9]/g, '_').toLowerCase() + '_df'
      
      let code = '# 导入可视化库\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\n'
      code += '# 设置中文显示\nplt.rcParams[\'font.sans-serif\'] = [\'SimHei\']\nplt.rcParams[\'axes.unicode_minus\'] = False\n\n'
      
      // 根据数据类型生成不同的可视化代码
      if (this.previewData && this.previewData.info) {
        const numericColumns = this.previewData.info.列名.filter(col => 
          ['int64', 'float64'].includes(this.previewData.info.数据类型[col])
        )
        
        if (numericColumns.length > 0) {
          // 生成箱线图代码
          code += '# 生成数值型数据分布图\n'
          code += `plt.figure(figsize=(10, 6))\n`
          code += `sns.boxplot(data=${varName}[[${numericColumns.map(col => `'${col}'`).join(', ')}]])\n`
          code += `plt.title('数值型数据分布')\nplt.xticks(rotation=45)\nplt.show()\n\n`
          
          // 如果有多个数值列，生成相关性热力图代码
          if (numericColumns.length > 1) {
            code += '# 生成相关性热力图\n'
            code += `plt.figure(figsize=(8, 6))\n`
            code += `sns.heatmap(${varName}[[${numericColumns.map(col => `'${col}'`).join(', ')}]].corr(), annot=True, cmap='coolwarm')\n`
            code += `plt.title('相关性热力图')\nplt.show()\n`
          }
        }
      }
      
      return code
    },
    // 插入代码到笔记本
    insertDataLoadCode() {
      const code = this.generateDataLoadCode()
      if (code) {
        this.$emit('insert-code', code)
        ElMessage.success('数据加载代码已插入到新的代码单元格')
        this.closeDialog()
      }
    },
    insertDataAnalysisCode() {
      const code = this.generateDataAnalysisCode()
      if (code) {
        this.$emit('insert-code', code)
        ElMessage.success('数据分析代码已插入到新的代码单元格')
        this.closeDialog()
      }
    },
    insertDataVisualizationCode() {
      const code = this.generateVisualizationCode()
      if (code) {
        this.$emit('insert-code', code)
        ElMessage.success('数据可视化代码已插入到新的代码单元格')
        this.closeDialog()
      }
    },
    // 插入所有代码
    async insertAllCode() {
      const loadCode = this.generateDataLoadCode()
      const analysisCode = this.generateDataAnalysisCode()
      const visualCode = this.generateVisualizationCode()
      
      if (loadCode && analysisCode && visualCode) {
        // 依次发出事件,让父组件创建三个单元格
        this.$emit('insert-code', loadCode)
        this.$emit('insert-code', analysisCode) 
        this.$emit('insert-code', visualCode)
        
        ElMessage.success('已生成全部代码单元格')
        this.closeDialog()
      }
    },
    // 更新预览文件信息
    async previewDataFile(file) {
      this.currentPreviewFile = file
      this.dialogVisible = true
    }
  }
}
</script>

<style scoped>
.preview-container {
  background: #fff;
  border-radius: 4px;
}

.file-info,
.data-info,
.data-preview,
.code-generation {
  padding: 12px;
  border-bottom: 1px solid #eee;
}

.file-info,
.data-info {
  padding: 8px 12px;
}

.code-generation {
  background-color: #f5f7fa;
}

.info-section {
  display: flex;
  flex-direction: column;
}

h3 {
  margin: 0 0 8px;
  font-size: 14px;
  font-weight: 500;
  color: #409EFF;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 4px;
  align-items: center;
}

.info-item {
  display: flex;
  gap: 4px;
  font-size: 13px;
  min-height: 20px;
  align-items: center;
}

.info-label {
  color: #666;
  font-weight: 500;
  white-space: nowrap;
}

.info-value {
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.data-preview {
  margin-top: 8px;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 8px 12px;
  border: 1px solid #eee;
  text-align: left;
}

th {
  background: #f5f7fa;
  font-weight: 500;
}

.error-message {
  margin-top: 10px;
  padding: 10px;
  background: #fef0f0;
  color: #f56c6c;
  border-radius: 4px;
}

.code-actions {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.code-action-group {
  flex: 1;
  min-width: 200px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.code-action-group h4 {
  margin: 0;
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.code-action-group .el-button {
  width: 100%;
  margin: 0;
}

:deep(.el-dialog__body) {
  padding: 0;
}
</style> 