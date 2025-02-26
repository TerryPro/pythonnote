<template>
  <el-dialog
    v-model="dialogVisible"
    title="重命名"
    width="30%"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <el-form label-width="0px">
      <el-form-item>
        <el-input
          v-model="newName"
          placeholder="请输入新的文件名"
          @keyup.enter="handleConfirm"
        >
          <template #append>{{ extension }}</template>
        </el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleConfirm">确认</el-button>
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
  currentName: {
    type: String,
    default: ''
  },
  extension: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:visible', 'cancel', 'confirm'])

const newName = ref('')
const dialogVisible = ref(props.visible)

// 监听visible属性变化
watch(() => props.visible, (newVal) => {
  dialogVisible.value = newVal
  if (newVal) {
    newName.value = props.currentName.replace(props.extension, '')
  }
})

// 监听对话框可见性变化
watch(dialogVisible, (newVal) => {
  emit('update:visible', newVal)
  if (!newVal) {
    newName.value = ''
  }
})

const handleConfirm = () => {
  if (!newName.value.trim()) {
    ElMessage.warning('文件名不能为空')
    return
  }
  emit('confirm', newName.value.trim())
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
</style>