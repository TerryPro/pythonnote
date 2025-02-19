<!-- 系统提示词配置对话框 -->
<template>
  <el-dialog
    v-model="dialogVisible"
    title="系统提示词配置"
    width="60%"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    @open="loadPrompts"
  >
    <div class="prompt-config">
      <div class="prompts-list">
        <div v-for="(prompt, index) in prompts" :key="index" class="prompt-item">
          <el-input
            v-model="prompts[index]"
            type="textarea"
            :rows="prompt.split('\n').length"
            :placeholder="'提示词 ' + (index + 1)"
          />
          <div class="prompt-actions">
            <el-button
              type="text"
              @click="movePrompt(index, -1)"
              :disabled="index === 0"
              title="上移"
            >
              <i class="fas fa-arrow-up"></i>
            </el-button>
            <el-button
              type="text"
              @click="movePrompt(index, 1)"
              :disabled="index === prompts.length - 1"
              title="下移"
            >
              <i class="fas fa-arrow-down"></i>
            </el-button>
            <el-button
              type="text"
              @click="removePrompt(index)"
              class="delete-btn"
              title="删除"
            >
              <i class="fas fa-trash"></i>
            </el-button>
          </div>
        </div>
      </div>
      
      <div class="prompt-actions">
        <el-button type="primary" plain @click="addPrompt">
          <i class="fas fa-plus"></i> 添加提示词
        </el-button>
      </div>
    </div>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="resetPrompts">恢复默认</el-button>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="savePrompts" :loading="saving">
          保存配置
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, defineExpose } from 'vue'
import { ElMessage } from 'element-plus'
import { API_ENDPOINTS, apiCall } from '@/api/http'

const dialogVisible = ref(false)
const prompts = ref([])
const saving = ref(false)

// 加载系统提示词
const loadPrompts = async () => {
  try {
    const result = await apiCall(API_ENDPOINTS.AI.SYSTEM_PROMPTS)
    prompts.value = result
  } catch (error) {
    console.error('加载系统提示词失败:', error)
    ElMessage.error('加载系统提示词失败: ' + error.message)
  }
}

// 保存系统提示词
const savePrompts = async () => {
  saving.value = true
  try {
    const result = await apiCall(API_ENDPOINTS.AI.SYSTEM_PROMPTS, {
      method: 'PUT',
      body: JSON.stringify({ prompts: prompts.value }),
    })
    
    if (result.status === 'success') {
      ElMessage.success('系统提示词已保存')
      dialogVisible.value = false
    } else {
      throw new Error(result.message || '保存系统提示词失败')
    }
  } catch (error) {
    console.error('保存系统提示词失败:', error)
    ElMessage.error('保存系统提示词失败: ' + error.message)
  } finally {
    saving.value = false
  }
}

// 重置系统提示词
const resetPrompts = async () => {
  try {
    const result = await apiCall(API_ENDPOINTS.AI.SYSTEM_PROMPTS_RESET, {
      method: 'POST'
    })
    
    if (result.status === 'success') {
      ElMessage.success('系统提示词已重置为默认值')
      await loadPrompts()
    } else {
      throw new Error(result.message || '重置系统提示词失败')
    }
  } catch (error) {
    console.error('重置系统提示词失败:', error)
    ElMessage.error('重置系统提示词失败: ' + error.message)
  }
}

// 添加系统提示词
const addPrompt = () => {
  prompts.value.push('')
}

// 移除系统提示词
const removePrompt = (index) => {
  prompts.value.splice(index, 1)
}

// 移动系统提示词
const movePrompt = (index, direction) => {
  const newIndex = index + direction
  if (newIndex >= 0 && newIndex < prompts.value.length) {
    const temp = prompts.value[index]
    prompts.value[index] = prompts.value[newIndex]
    prompts.value[newIndex] = temp
  }
}

// 暴露方法给父组件
defineExpose({
  show: () => {
    dialogVisible.value = true
  }
})
</script>

<style scoped>
.prompt-config {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.prompts-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 60vh;
  overflow-y: auto;
  padding-right: 8px;
}

.prompt-item {
  display: flex;
  gap: 8px;
  align-items: flex-start;
}

.prompt-item :deep(.el-input__wrapper) {
  flex: 1;
}

.prompt-actions {
  display: flex;
  gap: 4px;
}

.prompt-actions .el-button {
  padding: 4px 8px;
}

.delete-btn {
  color: var(--el-color-danger);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

/* 自定义滚动条样式 */
.prompts-list::-webkit-scrollbar {
  width: 6px;
}

.prompts-list::-webkit-scrollbar-track {
  background: transparent;
}

.prompts-list::-webkit-scrollbar-thumb {
  background-color: var(--el-border-color-lighter);
  border-radius: 3px;
}

.prompts-list::-webkit-scrollbar-thumb:hover {
  background-color: var(--el-border-color);
}
</style> 