<template>
  <div class="prompt-category">
    <h3 class="title">提示词分类</h3>
    <div
      v-for="category in categories"
      :key="category.id"
      class="category-item"
      :class="{ active: selectedCategory === category.id }"
      @click="selectCategory(category.id)"
    >
      <div class="category-name">{{ category.name }}</div>
      <div class="category-desc">{{ category.description }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PromptCategory',
  data() {
    return {
      categories: [],
      selectedCategory: ''
    }
  },
  methods: {
    async loadCategories() {
      try {
        const response = await fetch('/api/prompts/categories')
        const result = await response.json()
        if (result.code === 200) {
          this.categories = result.data
          if (this.categories.length > 0) {
            this.selectCategory(this.categories[0].id)
          }
        }
      } catch (error) {
        console.error('加载提示词分类失败:', error)
      }
    },
    selectCategory(categoryId) {
      this.selectedCategory = categoryId
      this.$emit('category-selected', categoryId)
    }
  },
  mounted() {
    this.loadCategories()
  }
}
</script>

<style scoped>
.prompt-category {
  padding: 16px;
  border-right: 1px solid #eee;
}

.title {
  margin-bottom: 16px;
  font-size: 18px;
  font-weight: bold;
}

.category-item {
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.category-item:hover {
  background-color: #f5f5f5;
}

.category-item.active {
  background-color: #e6f7ff;
  border-right: 3px solid #1890ff;
}

.category-name {
  font-size: 16px;
  margin-bottom: 4px;
}

.category-desc {
  font-size: 12px;
  color: #666;
}
</style> 