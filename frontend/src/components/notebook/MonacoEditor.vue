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

    // 监听内容变化
    editor.onDidChangeModelContent(() => {
      const value = editor.getValue()
      emit('update:value', value)
      emit('change', value)
    })

    // 使用防抖处理 resize
    const handleResize = debounce(() => {
      const contentHeight = Math.min(1000, editor.getContentHeight())
      editorContainer.value.style.height = `${contentHeight}px`
      editor.layout()
    }, 100)

    editor.onDidContentSizeChange(handleResize)

    // 设置初始值
    if (props.value) {
      editor.setValue(props.value)
    }
  }
})

// 监听 value 属性变化
watch(() => props.value, (newValue) => {
  if (editor && newValue !== editor.getValue()) {
    editor.setValue(newValue)
  }
})

// 监听 options 变化
watch(() => props.options, (newOptions) => {
  if (editor) {
    editor.updateOptions(newOptions)
  }
}, { deep: true })

// 监听 language 的变化
watch(() => props.language, (newLanguage) => {
  if (editor) {
    monaco.editor.setModelLanguage(editor.getModel(), newLanguage)
  }
})

onBeforeUnmount(() => {
  if (editor) {
    editor.dispose()
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