<template>
  <div class="prompt-preview">
    <div v-if="prompt" class="preview-content">
      <div class="preview-header">
        <h3 class="preview-title">{{ prompt.title }}</h3>
        <div class="preview-tags">
          <span v-for="tag in prompt.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
      </div>
      <div class="preview-desc">{{ prompt.description }}</div>
      <div class="preview-template">
        <div class="template-header">
          <span>提示词模板</span>
          <span class="use-count">已使用 {{ prompt.use_count }} 次</span>
        </div>
        <pre class="template-content">{{ prompt.template }}</pre>
      </div>
      <div class="preview-actions">
        <template v-if="isManageMode">
          <el-button type="primary" @click="handleEdit">
            编辑
          </el-button>
          <el-popconfirm
            title="确定要删除这个提示词吗？"
            @confirm="handleDelete"
          >
            <template #reference>
              <el-button type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
        <template v-else>
          <button class="action-btn primary" @click="usePrompt">
            使用此提示词
          </button>
          <button class="action-btn" @click="copyTemplate">
            复制内容
          </button>
        </template>
      </div>
    </div>
    <div v-else class="empty-preview">
      请选择一个提示词查看详情
    </div>
  </div>
</template>

<script>
export default {
  name: 'PromptPreview',
  props: {
    prompt: {
      type: Object,
      default: null
    },
    isManageMode: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    async usePrompt() {
      if (!this.prompt) return
      try {
        await fetch(`/api/prompts/use/${this.prompt.id}`, {
          method: 'POST'
        })
        this.$emit('use-prompt', this.prompt.template)
      } catch (error) {
        console.error('使用提示词失败:', error)
      }
    },
    async copyTemplate() {
      if (!this.prompt) return
      try {
        await navigator.clipboard.writeText(this.prompt.template)
        this.$message.success('复制成功')
      } catch (error) {
        console.error('复制失败:', error)
      }
    },
    handleEdit() {
      this.$emit('edit-prompt', this.prompt)
    },
    handleDelete() {
      this.$emit('delete-prompt', this.prompt.id)
    }
  }
}
</script>

<style scoped>
.prompt-preview {
  padding: 16px;
  height: 100%;
  overflow-y: auto;
}

.preview-header {
  margin-bottom: 16px;
}

.preview-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 8px;
}

.preview-tags {
  display: flex;
  gap: 8px;
}

.tag {
  padding: 2px 8px;
  background-color: #f0f0f0;
  border-radius: 2px;
  font-size: 12px;
  color: #666;
}

.preview-desc {
  color: #666;
  margin-bottom: 16px;
  line-height: 1.5;
}

.preview-template {
  background-color: #f8f8f8;
  border-radius: 4px;
  padding: 16px;
  margin-bottom: 16px;
}

.template-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}

.template-content {
  white-space: pre-wrap;
  font-family: monospace;
  line-height: 1.5;
  margin: 0;
}

.preview-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn:hover {
  background-color: #f5f5f5;
}

.action-btn.primary {
  background-color: #1890ff;
  border-color: #1890ff;
  color: white;
}

.action-btn.primary:hover {
  background-color: #40a9ff;
  border-color: #40a9ff;
}

.empty-preview {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 14px;
}
</style> 