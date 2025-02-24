<template>

  <!-- 数据预览对话框 -->
  <el-dialog v-model="dialogVisible" title="文件预览" width="80%" :close-on-click-modal="false" destroy-on-close>
    <!-- 文件信息 -->
    <el-descriptions title="文件信息" :column="3" border class="info-section">
      <el-descriptions-item v-for="(value, key) in store.previewData.file_info" :key="key" :label="key"
        label-class-name="info-label">
        {{ value }}
      </el-descriptions-item>
    </el-descriptions>

    <!-- 数据基本信息 -->
    <el-descriptions title="数据信息" :column="3" border class="info-section">
      <el-descriptions-item v-for="(value, key) in store.previewData.info" :key="key" :label="key"
        label-class-name="info-label">
        <template v-if="Array.isArray(value)">
          {{ value.join(', ') }}
        </template>
        <template v-else>
          {{ value }}
        </template>
      </el-descriptions-item>
    </el-descriptions>

    <!-- 数据预览表格 -->
    <div class="data-preview mt-4">
      <el-table :data="store.previewData?.head || []" height="250px" stripe border style="width: 100%">
        <el-table-column v-for="column in store.previewData?.info?.列名 || []" :key="column" :prop="column"
          :label="column" min-width="120" />
      </el-table>
    </div>

    <!-- 代码生成区域 -->
    <div class="code-generation mt-4">
      <el-row :gutter="20">
        <el-col :span="24">
          <div class="code-action-group">
            <el-space direction="horizontal" class="w-full">
              <el-button type="primary" @click="handleGenerateCode('load')" class="w-full">
                生成数据加载代码
              </el-button>
              <el-button type="primary" @click="handleGenerateCode('analysis')" class="w-full">
                生成数据分析代码
              </el-button>
              <el-button type="success" @click="handleGenerateCode('all')" class="w-full">
                生成全部代码
              </el-button>
              <el-button type="primary" @click="handleGenerateCode('visualization')" class="w-full">
                生成可视化代码
              </el-button>
            </el-space>
          </div>
        </el-col>
      </el-row>
    </div>

    <el-alert v-if="error" :title="error" type="error" show-icon class="mt-4" />

    <template #footer>
      <el-button @click="closeDialog">关闭</el-button>
    </template>
  </el-dialog>

</template>

<script setup>
import { ref, computed } from 'vue'
import { ElButton, ElDialog, ElMessage } from 'element-plus'
import { useDataFileStore } from '@/stores/dataFileStore'
import { useNotebook } from '@/composables/useNotebook'

const store = useDataFileStore()
const dialogVisible = ref(false)
const error = ref(null)
const { insertCode } = useNotebook()

const currentPreviewFile = computed(() => {
  return store.currentFileMeta
})

const previewDataFile = () => {
  dialogVisible.value = true
}

const closeDialog = () => {
  dialogVisible.value = false
}

// 统一处理代码生成
const handleGenerateCode = (type) => {
  let code = ''
  switch (type) {
    case 'load':
      code = generateDataLoadCode()
      break
    case 'analysis':
      code = generateDataAnalysisCode()
      break
    case 'visualization':
      code = generateVisualizationCode()
      break
    case 'all':
      code = [
        generateDataLoadCode(),
        generateDataAnalysisCode(),
        generateVisualizationCode()
      ]
      break
  }

  if (Array.isArray(code)) {
    code.forEach(item => insertCode(item))
  } else if (code) {
    insertCode(code)
  }
  closeDialog()
}

// 修改原有方法返回代码而不是直接处理
const generateDataLoadCode = () => {
  if (!currentPreviewFile.value) {
    ElMessage.warning('请先选择一个数据文件')
    return ''
  }

  const varName = getVarName(currentPreviewFile.value.name)
  const filePath = currentPreviewFile.value.path
  const fileType = currentPreviewFile.value.type

  let code = '# 导入必要的库\nimport pandas as pd\n\n'

  code += fileType === 'csv'
    ? `# 加载CSV文件\n${varName} = pd.read_csv('data/${filePath}')\n`
    : `# 加载Excel文件\n${varName} = pd.read_excel('data/${filePath}')\n`

  code += `\n# 显示数据基本信息\nprint("数据基本信息：")\nprint(${varName}.info())\n\n`
  code += `# 显示前几行数据\nprint("\\n数据预览：")\nprint(${varName}.head())\n`

  return code
}

const generateDataAnalysisCode = () => {
  if (!currentPreviewFile.value) {
    ElMessage.warning('请先选择一个数据文件')
    return ''
  }

  const varName = getVarName(currentPreviewFile.value.name)

  let code = '# 数据基本统计分析\n'
  code += `print("基本统计信息：")\nprint(${varName}.describe())\n\n`
  code += `# 检查缺失值\nprint("\\n缺失值统计：")\nprint(${varName}.isnull().sum())\n\n`
  code += `# 数据类型信息\nprint("\\n数据类型信息：")\nprint(${varName}.dtypes)\n`

  return code
}

const generateVisualizationCode = () => {
  if (!currentPreviewFile.value) {
    ElMessage.warning('请先选择一个数据文件')
    return ''
  }

  const varName = getVarName(currentPreviewFile.value.name)
  let code = '# 导入可视化库\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\n'
  code += '# 设置中文显示\nplt.rcParams[\'font.sans-serif\'] = [\'SimHei\']\nplt.rcParams[\'axes.unicode_minus\'] = False\n\n'

  if (store.previewData?.value?.info) {
    const numericColumns = store.previewData.info.列名.filter(col =>
      ['int64', 'float64'].includes(store.previewData.info.数据类型[col])
    )

    if (numericColumns.length > 0) {
      code += '# 生成数值型数据分布图\n'
      code += `plt.figure(figsize=(10, 6))\n`
      code += `sns.boxplot(data=${varName}[[${numericColumns.map(col => `'${col}'`).join(', ')}]])\n`
      code += `plt.title('数值型数据分布')\nplt.xticks(rotation=45)\nplt.show()\n\n`

      if (numericColumns.length > 1) {
        code += '# 生成相关性热力图\n'
        code += `plt.figure(figsize=(8, 6))\n`
        code += `sns.heatmap(${varName}[[${numericColumns.map(col => `'${col}'`).join(', ')}]].corr(), annot=True, cmap='coolwarm')\n`
        code += `plt.title('相关性热力图')\nplt.show()\n`
      }
    }
  }

  return code
}

// 工具函数
const getVarName = (fileName) => {
  return fileName.split('.')[0]
    .replace(/[^a-zA-Z0-9]/g, '_')
    .toLowerCase() + '_df'
}

// 暴露方法给父组件
defineExpose({
  previewDataFile
})
</script>

<style scoped>
.preview-container {
  padding: 16px;
}

.info-section {
  margin-bottom: 20px;
}

.mt-4 {
  margin-top: 16px;
}

.code-action-group h4 {
  margin: 0 0 8px;
  color: var(--el-color-info);
  font-size: 14px;
}

:deep(.info-label) {
  width: 120px;
  background-color: var(--el-fill-color-light) !important;
}
</style>