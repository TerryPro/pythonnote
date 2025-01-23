<template>
  <el-dialog
    v-model="dialogVisible"
    title="Python代码示例库"
    width="80%"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    destroy-on-close
    class="example-dialog"
  >
    <ExamplePanel
      :mode="mode"
      @use-example="handleUseExample"
    />
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import ExamplePanel from './ExamplePanel.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  mode: {
    type: String,
    default: 'use' // 'use' or 'manage'
  }
})

const emit = defineEmits(['update:modelValue', 'use-example'])

// 对话框可见性
const dialogVisible = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  dialogVisible.value = newVal
})

watch(dialogVisible, (newVal) => {
  emit('update:modelValue', newVal)
})

// 处理使用示例
const handleUseExample = (code) => {
  emit('use-example', code)
  dialogVisible.value = false
}

// 导出组件属性
defineExpose({
  show() {
    dialogVisible.value = true
  }
})
</script>

<style scoped>
.example-dialog :deep(.el-dialog__body) {
  padding: 16px;
  height: 70vh;
  overflow: hidden;
}

.example-dialog :deep(.el-dialog__header) {
  margin-right: 0;
  padding: 16px;
}

.example-dialog :deep(.el-dialog__headerbtn) {
  top: 16px;
}
</style> 