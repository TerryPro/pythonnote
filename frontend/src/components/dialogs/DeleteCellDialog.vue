<template>
  <el-dialog
    v-model="dialogVisible"
    title="删除单元格"
    width="30%"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <div class="delete-dialog-content">
      <el-alert
        title="确定要删除这个单元格吗？此操作不可恢复。"
        type="warning"
        :closable="false"
        show-icon
      />
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
</style>