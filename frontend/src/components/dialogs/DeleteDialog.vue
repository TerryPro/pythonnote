<template>
  <el-dialog
    v-model="dialogVisible"
    title="删除笔记本"
    width="30%"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <div class="delete-dialog-content">
      <el-alert
        title="此操作将永久删除该笔记本，是否继续？"
        type="warning"
        :closable="false"
        show-icon
      />
      <div class="file-info">
        <span class="label">文件名：</span>
        <span class="value">{{ fileName }}</span>
      </div>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="danger" @click="handleConfirm">确定删除</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, defineEmits, defineProps, watch } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    required: true
  },
  fileName: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:visible', 'cancel', 'confirm'])

const dialogVisible = ref(props.visible)

// 监听visible属性变化
watch(() => props.visible, (newVal) => {
  dialogVisible.value = newVal
})

// 监听对话框可见性变化
watch(dialogVisible, (newVal) => {
  emit('update:visible', newVal)
})

const handleConfirm = () => {
  emit('confirm')
}

const handleCancel = () => {
  emit('cancel')
  dialogVisible.value = false
}
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.delete-dialog-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.file-info {
  margin-top: 8px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 4px;
  font-size: 14px;
}

.file-info .label {
  color: #606266;
  margin-right: 8px;
}

.file-info .value {
  color: #303133;
  font-weight: 500;
}
</style> 