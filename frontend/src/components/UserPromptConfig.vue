<!-- 用户提示词配置对话框 -->
<template>
  <el-dialog
    v-model="dialogVisible"
    title="代码生成要求配置"
    width="60%"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    @open="loadRequirements"
  >
    <div class="prompt-config">
      <div class="requirements-list">
        <div v-for="(requirement, index) in requirements" :key="index" class="requirement-item">
          <el-input
            v-model="requirements[index]"
            type="textarea"
            :rows="requirement.split('\n').length"
            :placeholder="'要求 ' + (index + 1)"
          />
          <div class="requirement-actions">
            <el-button
              type="text"
              @click="moveRequirement(index, -1)"
              :disabled="index === 0"
              title="上移"
            >
              <i class="fas fa-arrow-up"></i>
            </el-button>
            <el-button
              type="text"
              @click="moveRequirement(index, 1)"
              :disabled="index === requirements.length - 1"
              title="下移"
            >
              <i class="fas fa-arrow-down"></i>
            </el-button>
            <el-button
              type="text"
              @click="removeRequirement(index)"
              class="delete-btn"
              title="删除"
            >
              <i class="fas fa-trash"></i>
            </el-button>
          </div>
        </div>
      </div>
      
      <div class="requirement-actions">
        <el-button type="primary" plain @click="addRequirement">
          <i class="fas fa-plus"></i> 添加要求
        </el-button>
      </div>
    </div>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="resetRequirements">恢复默认</el-button>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveRequirements" :loading="saving">
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
const requirements = ref([])
const saving = ref(false)

// 加载代码生成要求
const loadRequirements = async () => {
  try {
    const result = await apiCall(API_ENDPOINTS.AI.USER_PROMPTS)
    requirements.value = result
  } catch (error) {
    console.error('加载代码生成要求失败:', error)
    ElMessage.error('加载代码生成要求失败: ' + error.message)
  }
}

// 保存代码生成要求
const saveRequirements = async () => {
  saving.value = true
  try {
    const result = await apiCall(API_ENDPOINTS.AI.USER_PROMPTS, {
      method: 'PUT',
      body: JSON.stringify({ requirements: requirements.value })
    })
    
    if (result.status === 'success') {
      ElMessage.success('代码生成要求已保存')
      dialogVisible.value = false
    } else {
      throw new Error(result.message || '保存代码生成要求失败')
    }
  } catch (error) {
    console.error('保存代码生成要求失败:', error)
    ElMessage.error('保存代码生成要求失败: ' + error.message)
  } finally {
    saving.value = false
  }
}

// 重置代码生成要求
const resetRequirements = async () => {
  try {
    const result = await apiCall(API_ENDPOINTS.AI.RESET_USER_PROMPTS, {
      method: 'POST'
    })
    
    if (result.status === 'success') {
      ElMessage.success('代码生成要求已重置为默认值')
      await loadRequirements()
    } else {
      throw new Error(result.message || '重置代码生成要求失败')
    }
  } catch (error) {
    console.error('重置代码生成要求失败:', error)
    ElMessage.error('重置代码生成要求失败: ' + error.message)
  }
}

// 添加代码生成要求
const addRequirement = () => {
  requirements.value.push('')
}

// 移除代码生成要求
const removeRequirement = (index) => {
  requirements.value.splice(index, 1)
}

// 移动代码生成要求
const moveRequirement = (index, direction) => {
  const newIndex = index + direction
  if (newIndex >= 0 && newIndex < requirements.value.length) {
    const temp = requirements.value[index]
    requirements.value[index] = requirements.value[newIndex]
    requirements.value[newIndex] = temp
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

.requirements-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 60vh;
  overflow-y: auto;
  padding-right: 8px;
}

.requirement-item {
  display: flex;
  gap: 8px;
  align-items: flex-start;
}

.requirement-item :deep(.el-input__wrapper) {
  flex: 1;
}

.requirement-actions {
  display: flex;
  gap: 4px;
}

.requirement-actions .el-button {
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
.requirements-list::-webkit-scrollbar {
  width: 6px;
}

.requirements-list::-webkit-scrollbar-track {
  background: transparent;
}

.requirements-list::-webkit-scrollbar-thumb {
  background-color: var(--el-border-color-lighter);
  border-radius: 3px;
}

.requirements-list::-webkit-scrollbar-thumb:hover {
  background-color: var(--el-border-color);
}
</style> 