<template>
  <div class="monaco-editor-container" ref="editorContainer"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as monaco from 'monaco-editor'

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

const emit = defineEmits(['update:value'])
const editorContainer = ref(null)
let editor = null

onMounted(() => {
  if (editorContainer.value) {
    editor = monaco.editor.create(editorContainer.value, {
      value: props.value,
      language: props.language,
      theme: 'vs',
      ...props.options
    })

    // 监听内容变化
    editor.onDidChangeModelContent(() => {
      const value = editor.getValue()
      emit('update:value', value)
    })

    // 设置初始值
    if (props.value) {
      editor.setValue(props.value)
    }
  }
})

// 监听 value prop 的变化
watch(() => props.value, (newValue) => {
  if (editor && newValue !== editor.getValue()) {
    editor.setValue(newValue || '')
  }
}, { immediate: true })

// 监听 options 的变化
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
</script>

<style scoped>
.monaco-editor-container {
  width: 100%;
  height: 200px;
  border: 1px solid #eee;
}
</style> 