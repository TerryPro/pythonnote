<template>
  <el-dialog
    v-model="dialogVisible"
    title="保存笔记本"
    width="30%"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <el-form label-width="0px">
      <el-form-item>
        <el-input
          v-model="fileName"
          placeholder="请输入新的文件名"
          @keyup.enter="handleConfirm"
        >
          <template #append>.ipynb</template>
        </el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleConfirm" :loading="loading">确认</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, defineEmits, defineProps, watch } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  visible: {
    type: Boolean,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'cancel', 'confirm'])

const fileName = ref('')
const dialogVisible = ref(props.visible)

// 监听visible属性变化
watch(() => props.visible, (newVal) => {
  dialogVisible.value = newVal
})

// 监听对话框可见性变化
watch(dialogVisible, (newVal) => {
  emit('update:visible', newVal)
  if (!newVal) {
    fileName.value = ''
  }
})

const handleConfirm = () => {
  if (!fileName.value.trim()) {
    ElMessage.warning('请输入笔记本名称')
    return
  }
  emit('confirm', fileName.value.trim())
}

const handleCancel = () => {
  emit('cancel')
  fileName.value = ''
}
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style> 