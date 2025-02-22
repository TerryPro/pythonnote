<template>
  <div class="code-cell" :id="`codeCell${cellId}`">
    <div class="editor-container">
      <MonacoEditor
        v-model:value="localContent"
        :options="{
          language: 'python',
          theme: currentTheme === 'dark' ? 'vs-dark' : 'vs',
          automaticLayout: true,
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          overviewRulerBorder: false,
          lineNumbers: 'on',
          renderLineHighlight: 'all',
          autoHeight: true,
          wordWrap: 'off',
          fontSize: 14,
          tabSize: 4,
          lineHeight: 20,
          fontFamily: 'Fira Code, Source Code Pro, JetBrains Mono, Consolas, monospace',
          fontLigatures: true,
          quickSuggestions: true,
          suggestOnTriggerCharacters: true,
          wordBasedSuggestions: true,
          parameterHints: { enabled: true }
        }"
        @change="handleEditorChange"
        class="monaco-editor-auto-height"
      />
    </div>
    
    <div class="output-container" v-show="outputContent">
      <pre class="output-text" v-if="outputContent.output">{{ outputContent.output }}</pre>
      <div class="plot-container" v-if="outputContent.plot" v-html="outputContent.plot"></div>
      <div class="plotly-container" :id="`plotly-container-${cellId}`" v-if="outputContent.plotly_html" v-html="outputContent.plotly_html"></div>
    </div>
    
    <!-- AI对话框 -->
    <AiDialog
      v-model="showAiDialog"
      :notebook-context="notebookContext"
      :dataframe-info="dataframeInfo"
      @code-generated="handleCodeGenerated"
    />
    
    <!-- 保存到示例库对话框 -->
    <SaveToExampleDialog
      v-model="showSaveDialog"
      :code="localContent"
      @saved="handleExampleSaved"
    />
  </div>
</template>

<script setup>
import { ref, inject, onMounted, watch, nextTick } from 'vue'
import MonacoEditor from '@/components/notebook/MonacoEditor.vue'
import AiDialog from '@/components/ai/AiDialog.vue'
import SaveToExampleDialog from '@/components/examples/SaveToExampleDialog.vue'
import { ElLoading, ElMessage } from 'element-plus'
import { useDataFrameStore } from '@/stores/dataframeStore'

const props = defineProps({
  cellId: {
    type: String,
    required: true
  },
  content: {
    type: String,
    default: ''
  },
  outputContent: {
    type: Object,
    default: () => ({
      output: '',
      plot: '',
      plotly_html: '',
      status: 'idle'
    })
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

// 注入主题
const currentTheme = inject('currentTheme', ref('light'))

// 本地状态
const localContent = ref(props.content)
const showAiDialog = ref(false)
const isExecuting = ref(false)

// 在setup部分添加
const dataframeStore = useDataFrameStore()

// 监听props变化
watch(() => props.content, (newValue) => {
  localContent.value = newValue
})

const emit = defineEmits(['execution-complete', 'update:content', 'update:output', 'refresh-dataframes'])

// 处理编辑器内容变化
const handleEditorChange = (value) => {
  emit('update:content', value || '')
}

// 处理AI生成的代码
const handleCodeGenerated = (code) => {
  localContent.value = code
  emit('update:content', code)
}

const executeCode = async () => {
  if (!props.content.trim()) return
  
  const loading = ElLoading.service({
    target: `#codeCell${props.cellId}`,
    text: '正在执行代码...',
    background: 'rgba(255, 255, 255, 0.7)'
  })
  
  isExecuting.value = true
  try {
    const response = await fetch('http://127.0.0.1:8000/api/execution/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ code: props.content })
    })
    
    if (!response.ok) {
      throw new Error('执行失败')
    }
    
    const result = await response.json()
    
    // 更新输出
    emit('update:output', {
      output: result.output || '',
      plot: result.plot || '',
      plotly_html: result.plotly_html || '',
      status: result.status || 'idle'
    })
    
    // 如果有DataFrame变量，直接通过store刷新
    if (result.has_dataframes) {
      dataframeStore.fetchDataFrames()
    }
    
    // 触发执行完成事件
    emit('execution-complete', props.cellId)
    
  } catch (error) {
    console.error('执行代码失败:', error)
    emit('update:output', {
      output: `执行失败: ${error.message}`,
      plot: '',
      plotly_html: '',
      status: 'error'
    })
  } finally {
    isExecuting.value = false
    loading.close()
  }
}

// 在组件挂载时初始化图表
onMounted(() => {
  // 如果初始化时就有 plotly_html，立即渲染
  if (props.outputContent?.plotly_html) {
    console.log('[Plotly] 初始化时发现 plotly_html 内容，开始渲染');
    renderPlotly(props.outputContent.plotly_html);
  }
});

// 提取渲染 Plotly 图表的函数
const renderPlotly = (htmlContent) => {
  if (!htmlContent) return;
  
  nextTick(() => {
    const container = document.getElementById(`plotly-container-${props.cellId}`);
    if (container) {
      console.log('[Plotly] 找到容器，开始更新内容');
      // 先清空容器
      container.innerHTML = '';

      // 解析HTML字符串为DOM
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = htmlContent;
      
      // 提取脚本内容
      const scriptContent = tempDiv.querySelector('script').textContent;
      
      // 创建并执行新的脚本
      const script = document.createElement('script');
      script.textContent = scriptContent;
      container.appendChild(script);
    } else {
      console.error('[Plotly] 未找到容器元素:', `plotly-container-${props.cellId}`);
    }
  });
};

// 监听 plotly_html 的变化
watch(() => props.outputContent?.plotly_html, (newVal) => {
  console.log('[Plotly] plotly_html 发生变化:', newVal ? '有内容' : '无内容');
  if (newVal && window.Plotly) {
    renderPlotly(newVal);
  }
});

// 保存到示例库相关
const showSaveDialog = ref(false)

const handleSaveToExample = () => {
  if (!localContent.value?.trim()) {
    ElMessage.warning('请先输入代码')
    return
  }
  showSaveDialog.value = true
}

const handleExampleSaved = () => {
  ElMessage.success('示例代码保存成功')
  showSaveDialog.value = false
}

// 暴露属性给父组件
defineExpose({
  executeCode,
  showAiDialog,
  handleSaveToExample
})
</script>

<style>
.code-cell {
  margin: 0;
  background: var(--cell-background);
  position: relative;
  transition: background-color 0.3s ease;
}

.editor-container {
  background: var(--cell-background);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  transition: all 0.3s ease;
  position: relative;
}

.monaco-editor-auto-height {
  width: 100%;
  min-height: 20px;
  position: relative;
}

:deep(.monaco-editor) {
  padding: 8px 0;
}

:deep(.monaco-editor .overflow-guard) {
  position: relative !important;
}

:deep(.monaco-editor .monaco-scrollable-element) {
  position: relative !important;
}

:deep(.monaco-editor-background) {
  background-color: var(--editor-background) !important;
}

:deep(.monaco-editor .editor-scrollable) {
  position: relative !important;
}

:deep(.monaco-editor .lines-content) {
  position: relative !important;
}

:deep(.monaco-editor .view-lines) {
  position: relative !important;
  white-space: pre;
}

:deep(.monaco-editor .view-line) {
  position: relative !important;
  width: 100% !important;
}

.output-container {
  margin-top: 4px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.output-text {
  padding: 12px;
  font-family: 'JetBrains Mono', 'Fira Code', 'Source Code Pro', Consolas, monospace;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  background-color: var(--code-background);
  color: var(--text-color);
  transition: all 0.3s ease;
  letter-spacing: 0.3px;
}

.plot-container {
  padding: 12px;
  background: var(--cell-background);
  text-align: center;
  transition: background-color 0.3s ease;
}

.plot-container :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}

.plotly-container {
  padding: 12px;
  background: var(--cell-background);
  border-radius: 4px;
  overflow: visible;
  transition: all 0.3s ease;
  height: 500px;
  position: relative;
}

.plotly-container :deep(.plotly-graph-div) {
  width: 100% !important;
  height: 100% !important;
  margin: 0 auto;
}

.plotly-container :deep(.modebar) {
  background: var(--cell-background) !important;
  z-index: 1;
}

.plotly-container :deep(.main-svg) {
  background: transparent !important;
}

:deep(.el-loading-spinner) {
  .el-loading-text {
    color: var(--el-color-primary);
    font-size: 14px;
    margin: 8px 0;
  }
  
  .circular {
    width: 32px;
    height: 32px;
    .path {
      stroke: var(--el-color-primary);
      stroke-width: 3;
    }
  }
}

:deep(.el-loading-mask) {
  background-color: var(--el-mask-color);
  backdrop-filter: blur(2px);
  transition: all 0.3s;
  z-index: 10;
}

.editor-toolbar {
  display: flex;
  justify-content: flex-end;
  padding: 8px;
  border-bottom: 1px solid var(--border-color);
}
</style> 