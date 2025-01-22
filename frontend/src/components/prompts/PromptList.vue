<template>
  <div class="prompt-list">
    <div class="prompt-search">
      <input
        v-model="searchText"
        type="text"
        placeholder="搜索提示词..."
        class="search-input"
      >
    </div>
    <div class="prompt-items">
      <div
        v-for="prompt in filteredPrompts"
        :key="prompt.id"
        class="prompt-item"
        :class="{ active: selectedPrompt === prompt.id }"
        @click="selectPrompt(prompt)"
      >
        <div class="prompt-title">{{ prompt.title }}</div>
        <div class="prompt-desc">{{ prompt.description }}</div>
        <div class="prompt-meta">
          <span class="prompt-tags">
            <span v-for="tag in prompt.tags" :key="tag" class="tag">{{ tag }}</span>
          </span>
          <span class="use-count">使用次数: {{ prompt.use_count }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PromptList',
  props: {
    categoryId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      prompts: [],
      selectedPrompt: '',
      searchText: ''
    }
  },
  computed: {
    filteredPrompts() {
      if (!this.searchText) return this.prompts
      const searchLower = this.searchText.toLowerCase()
      return this.prompts.filter(prompt => 
        prompt.title.toLowerCase().includes(searchLower) ||
        prompt.description.toLowerCase().includes(searchLower) ||
        prompt.tags.some(tag => tag.toLowerCase().includes(searchLower))
      )
    }
  },
  methods: {
    async loadPrompts() {
      if (!this.categoryId) return
      try {
        const response = await fetch(`/api/prompts/category/${this.categoryId}`)
        const result = await response.json()
        if (result.code === 200) {
          this.prompts = result.data
        }
      } catch (error) {
        console.error('加载提示词列表失败:', error)
      }
    },
    selectPrompt(prompt) {
      this.selectedPrompt = prompt.id
      this.$emit('prompt-selected', prompt)
    }
  },
  watch: {
    categoryId: {
      immediate: true,
      handler() {
        this.loadPrompts()
      }
    }
  }
}
</script>

<style scoped>
.prompt-list {
  padding: 16px;
}

.prompt-search {
  margin-bottom: 16px;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.prompt-item {
  padding: 12px;
  margin-bottom: 12px;
  border: 1px solid #eee;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.prompt-item:hover {
  background-color: #f5f5f5;
}

.prompt-item.active {
  border-color: #1890ff;
  background-color: #e6f7ff;
}

.prompt-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 4px;
}

.prompt-desc {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.prompt-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}

.prompt-tags {
  display: flex;
  gap: 4px;
}

.tag {
  padding: 2px 6px;
  background-color: #f0f0f0;
  border-radius: 2px;
  color: #666;
}

.use-count {
  color: #999;
}
</style> 