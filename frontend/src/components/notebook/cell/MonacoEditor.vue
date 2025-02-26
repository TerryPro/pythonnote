<template>
  <div ref="editorContainer" class="monaco-editor-container"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as monaco from 'monaco-editor'
import { debounce } from 'lodash'

const props = defineProps({
  value: {
    type: String,
    default: ''
  },
  language: {
    type: String,
    default: 'javascript'
  },
  options: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:value', 'change'])

const editorContainer = ref(null)
let editor = null
let isDisposed = false

// 创建一个防抖的resize处理函数
const handleResize = debounce(() => {
  if (!editor || !editorContainer.value || isDisposed) {
    return
  }
  try {
    const contentHeight = Math.min(1000, editor.getContentHeight())
    editorContainer.value.style.height = `${contentHeight}px`
    editor.layout()
  } catch (error) {
    console.warn('Error during editor resize:', error)
  }
}, 100)

onMounted(() => {
  if (editorContainer.value) {
    editor = monaco.editor.create(editorContainer.value, {
      value: props.value,
      language: props.language,
      theme: 'vs',
      ...props.options,
      automaticLayout: true,
      scrollBeyondLastLine: false,
      fixedOverflowWidgets: true,
      scrollbar: {
        vertical: 'hidden',
        horizontal: 'auto',
        useShadows: false,
        verticalScrollbarSize: 0,
        horizontalScrollbarSize: 10,
        alwaysConsumeMouseWheel: false
      }
    })

    editor.onDidChangeModelContent(() => {
      if (!isDisposed) {
        const value = editor.getValue()
        emit('update:value', value)
        emit('change', value)
      }
    })

    editor.onDidContentSizeChange(() => {
      if (!isDisposed) {
        handleResize()
      }
    })

    // 初始化编辑器大小
    handleResize()

    if (props.value) {
      editor.setValue(props.value)
    }
  }
})

watch(() => props.value, (newValue) => {
  if (editor && !isDisposed && newValue !== editor.getValue()) {
    editor.setValue(newValue)
  }
})

watch(() => props.options, (newOptions) => {
  if (editor && !isDisposed) {
    editor.updateOptions(newOptions)
  }
}, { deep: true })

watch(() => props.language, (newLanguage) => {
  if (editor && !isDisposed) {
    monaco.editor.setModelLanguage(editor.getModel(), newLanguage)
  }
})

onBeforeUnmount(() => {
  isDisposed = true
  if (handleResize) {
    handleResize.cancel()
  }
  if (editor) {
    editor.dispose()
    editor = null
  }
})
</script>

<style>
.monaco-editor-container {
  width: 100%;
  min-height: 20px;
  position: relative;
  overflow: hidden;
}
</style> 