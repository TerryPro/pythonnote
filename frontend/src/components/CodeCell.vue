<template>
  <div class="code-cell" :id="`codeCell${cellId}`">
    <div class="editor-container">
      <MonacoEditor
        :value="content"
        @update:value="updateContent"
        language="python"
        :options="editorOptions"
        :theme="editorTheme"
      />
    </div>
    <div class="output-container" v-show="outputContent">
      <pre class="output-text" v-if="outputContent.output">{{ outputContent.output }}</pre>
      <div class="plot-container" v-if="outputContent.plot" v-html="outputContent.plot"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, computed } from 'vue'
import MonacoEditor from './MonacoEditor.vue'

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
      status: 'idle'
    })
  }
})

// 注入主题
const currentTheme = inject('currentTheme', ref('light'))
const editorTheme = computed(() => {
  switch (currentTheme.value) {
    case 'dark':
      return 'vs-dark'
    case 'sepia':
    case 'ocean':
    default:
      return 'vs'
  }
})

const emit = defineEmits(['execution-complete', 'update:content', 'update:output'])

const isExecuting = ref(false)

const editorOptions = {
  minimap: { enabled: false },
  scrollBeyondLastLine: false,
  lineNumbers: 'on',
  lineHeight: 18,
  fontSize: 13,
  automaticLayout: true,
  wordWrap: 'on',
  renderLineHighlight: 'all',
  scrollbar: {
    vertical: 'hidden',
    horizontal: 'hidden'
  },
  fontFamily: "'Fira Code', 'Source Code Pro', 'JetBrains Mono', Consolas, monospace",
  fontLigatures: true,
  tabSize: 4,
  insertSpaces: true,
  quickSuggestions: true,
  suggestOnTriggerCharacters: true,
  wordBasedSuggestions: true,
  parameterHints: {
    enabled: true
  }
}

const updateContent = (newValue) => {
  emit('update:content', newValue || '')
}

const executeCode = async () => {
  isExecuting.value = true
  try {
    const response = await fetch('http://localhost:8000/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        code: props.content
      })
    })
    
    const result = await response.json()
    console.log('Execution result:', result)
    
    emit('update:output', {
      output: result.error ? 
        `错误: ${result.error.type}\n${result.error.message}` : 
        result.output || '',
      plot: result.plot || '',
      status: result.status || 'idle'
    })
      
    if (result.status === 'success') {
      emit('execution-complete', props.cellId)
    }
  } catch (error) {
    console.error('Execution error:', error)
    emit('update:output', {
      output: `请求错误: ${error.message}`,
      plot: '',
      status: 'error'
    })
  } finally {
    isExecuting.value = false
  }
}

defineExpose({
  executeCode
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
}

.editor-container :deep(.monaco-editor) {
  padding: 3px 0;
  background-color: var(--code-background);
}

.editor-container :deep(.monaco-editor .overflow-guard) {
  border-radius: 0 !important;
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
  font-family: 'Fira Code', monospace;
  font-size: 13px;
  line-height: 1.5;
  white-space: pre-wrap;
  background-color: var(--code-background);
  color: var(--text-color);
  transition: all 0.3s ease;
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
</style> 