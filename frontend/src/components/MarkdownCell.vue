<template>
  <div class="markdown-cell">
    <div v-if="isEditing" class="editor-container">
      <MonacoEditor
        :value="content"
        @update:value="updateContent"
        language="markdown"
        :options="editorOptions"
      />
    </div>
    <div v-else class="output-container" @dblclick="toggleEdit">
      <div class="markdown-preview markdown-body" v-html="renderedContent"></div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import MonacoEditor from './MonacoEditor.vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const props = defineProps({
  cellId: {
    type: String,
    required: true
  },
  content: {
    type: String,
    default: ''
  },
  isEditing: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:content', 'update:isEditing'])

// 监听编辑状态变化
watch(() => props.isEditing, (newValue) => {
  emit('update:isEditing', newValue)
})

const editorOptions = {
  minimap: { enabled: false },
  scrollBeyondLastLine: false,
  lineNumbers: 'off',
  lineHeight: 18,
  fontSize: 13,
  automaticLayout: true,
  wordWrap: 'on',
  renderLineHighlight: 'none',
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
  glyphMargin: false,
  folding: false,
  lineDecorationsWidth: 0,
  lineNumbersMinChars: 0
}

const renderedContent = computed(() => {
  return DOMPurify.sanitize(marked(props.content || ''))
})

const toggleEdit = () => {
  emit('update:isEditing', !props.isEditing)
}

const updateContent = (newValue) => {
  emit('update:content', newValue || '')
}

defineExpose({
  toggleEdit,
  isEditing: props.isEditing
})
</script>

<style>
@import 'github-markdown-css/github-markdown.css';
@import '@fortawesome/fontawesome-free/css/all.css';

.markdown-cell {
  margin: 0;
  background: #ffffff;
  position: relative;
}

.cell-actions {
  display: flex;
  gap: 8px;
  padding: 4px 8px;
}

.icon-btn {
  width: 32px;
  height: 32px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.icon-btn:hover {
  background: #f5f5f5;
  border-color: #ccc;
  color: #333;
}

.icon-btn:active {
  background: #e8e8e8;
}

.icon-btn i {
  font-size: 14px;
}

.editor-container {
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.editor-container :deep(.monaco-editor) {
  padding: 3px 0;
}

.editor-container :deep(.monaco-editor .overflow-guard) {
  border-radius: 0 !important;
}

.output-container {
  margin-top: 4px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
  background-color: #f8f9fa;
  margin-left: 0;
  margin-right: 0;
}

.markdown-preview {
  padding: 12px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  font-size: 13px;
  line-height: 1.5;
  margin: 0;
}

.markdown-body :deep(h1:first-child) {
  margin-top: 0;
}

.markdown-body :deep(p:last-child) {
  margin-bottom: 0;
}

.markdown-body :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}
</style> 