<template>
  <div class="prompt-panel">
    <!-- 左侧分类列表 -->
    <el-card class="category-panel" shadow="never">
      <template #header>
        <div class="card-header">
          <span>提示词分类</span>
          <button
            v-if="isManageMode"
            class="icon-btn"
            @click="handleAddCategory"
            title="添加分类"
          >
            <el-icon><Plus /></el-icon>
          </button>
        </div>
      </template>
      <el-menu
        :default-active="selectedCategory"
        class="category-menu"
        @select="handleCategorySelect"
      >
        <el-menu-item
          v-for="category in categories"
          :key="category.id"
          :index="category.id"
        >
          <template #title>
            <span>{{ category.name }}</span>
          </template>
        </el-menu-item>
      </el-menu>
    </el-card>

    <!-- 中间提示词列表 -->
    <el-card class="prompt-list" shadow="never">
      <template #header>
        <div class="card-header">
          <el-input
            v-model="searchText"
            placeholder="搜索提示词..."
            :prefix-icon="Search"
            clearable
          />
          <button
            v-if="isManageMode"
            class="icon-btn"
            @click="handleAddPrompt"
            title="添加提示词"
          >
            <el-icon><Plus /></el-icon>
          </button>
        </div>
      </template>
      <el-scrollbar>
        <el-empty v-if="filteredPrompts.length === 0" description="暂无提示词" />
        <el-menu
          v-else
          :default-active="selectedPromptId"
          class="prompt-menu"
          @select="handlePromptSelect"
        >
          <el-menu-item
            v-for="prompt in filteredPrompts"
            :key="prompt.id"
            :index="prompt.id"
          >
            <div class="prompt-item">
              <div class="prompt-info">
                <div class="prompt-title">{{ prompt.title }}</div>
              </div>
            </div>
          </el-menu-item>
        </el-menu>
      </el-scrollbar>
    </el-card>

    <!-- 右侧预览区域 -->
    <el-card class="prompt-preview" shadow="never">
      <template #header>
        <div class="card-header">
          <span>提示词预览</span>
        </div>
      </template>
      <el-empty
        v-if="!selectedPrompt"
        description="请选择一个提示词查看详情"
      />
      <template v-else>
        <div class="preview-content">
          <div class="preview-header">
            <h3>{{ selectedPrompt.title }}</h3>
          </div>
          <p class="preview-desc">{{ selectedPrompt.description }}</p>
          <div class="preview-template">
            <div class="template-header">
              <span>提示词模板</span>
              <el-tag size="small" type="info">
                已使用 {{ selectedPrompt.use_count }} 次
              </el-tag>
            </div>
            <el-input
              type="textarea"
              v-model="selectedPrompt.template"
              :rows="6"
              readonly
            />
          </div>
          <div class="preview-actions">
            <template v-if="isManageMode">
              <el-button type="primary" @click="handleEdit">
                <el-icon><Edit /></el-icon>编辑
              </el-button>
              <el-popconfirm
                title="确定要删除这个提示词吗？"
                @confirm="handleDelete"
              >
                <template #reference>
                  <el-button type="danger">
                    <el-icon><Delete /></el-icon>删除
                  </el-button>
                </template>
              </el-popconfirm>
            </template>
            <template v-else>
              <el-button type="primary" @click="usePrompt">
                使用此提示词
              </el-button>
              <el-button @click="copyTemplate">
                复制内容
              </el-button>
            </template>
          </div>
        </div>
      </template>
    </el-card>

    <!-- 添加/编辑分类对话框 -->
    <el-dialog
      v-model="showCategoryDialog"
      :title="editingCategory ? '编辑分类' : '添加分类'"
      width="500px"
    >
      <el-form
        ref="categoryFormRef"
        :model="categoryForm"
        :rules="categoryRules"
        label-width="80px"
      >
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="categoryForm.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="categoryForm.description"
            type="textarea"
            placeholder="请输入分类描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCategoryDialog = false">取消</el-button>
        <el-button type="primary" @click="saveCategoryForm">确定</el-button>
      </template>
    </el-dialog>

    <!-- 添加/编辑提示词对话框 -->
    <el-dialog
      v-model="showPromptDialog"
      :title="editingPrompt ? '编辑提示词' : '添加提示词'"
      width="650px"
    >
      <el-form
        ref="promptFormRef"
        :model="promptForm"
        :rules="promptRules"
        label-width="80px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="promptForm.title" placeholder="请输入提示词标题" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="promptForm.description"
            type="textarea"
            placeholder="请输入提示词描述"
          />
        </el-form-item>
        <el-form-item label="模板" prop="template">
          <el-input
            v-model="promptForm.template"
            type="textarea"
            :rows="6"
            placeholder="请输入提示词模板内容"
          />
        </el-form-item>
        <el-form-item label="标签" prop="tags">
          <el-select
            v-model="promptForm.tags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="请选择或输入标签"
          >
            <el-option
              v-for="tag in availableTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPromptDialog = false">取消</el-button>
        <el-button type="primary" @click="savePromptForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Plus,
  Edit,
  Delete,
  Search
} from '@element-plus/icons-vue'

const props = defineProps({
  mode: {
    type: String,
    default: 'use' // 'use' or 'manage'
  }
})

const emit = defineEmits(['use-prompt'])

// 状态变量
const selectedCategory = ref('')
const selectedPromptId = ref('')
const selectedPrompt = ref(null)
const searchText = ref('')
const showCategoryDialog = ref(false)
const showPromptDialog = ref(false)
const editingCategory = ref(null)
const editingPrompt = ref(null)

// 表单数据
const categoryForm = ref({
  name: '',
  description: ''
})

const promptForm = ref({
  title: '',
  description: '',
  template: '',
  tags: []
})

// 表单验证规则
const categoryRules = {
  name: [
    { required: true, message: '请输入分类名称', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入分类描述', trigger: 'blur' },
    { max: 200, message: '最多 200 个字符', trigger: 'blur' }
  ]
}

const promptRules = {
  title: [
    { required: true, message: '请输入提示词标题', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入提示词描述', trigger: 'blur' },
    { max: 200, message: '最多 200 个字符', trigger: 'blur' }
  ],
  template: [
    { required: true, message: '请输入提示词模板', trigger: 'blur' }
  ],
  tags: [
    { required: true, message: '请至少选择一个标签', trigger: 'change' }
  ]
}

// 可用标签列表
const availableTags = ref([
  '数据探索',
  '数据清洗',
  '数据分析',
  '数据可视化',
  '统计分析'
])

// 计算属性
const isManageMode = computed(() => props.mode === 'manage')

// 修改模拟数据为实际API调用
const categories = ref([])
const prompts = ref([])

// 基础 URL 常量
const BASE_URL = 'http://localhost:8000'

// 加载分类列表
const loadCategories = async () => {
  try {
    const response = await fetch(`${BASE_URL}/api/prompt/categories`)
    if (response.ok) {
      const result = await response.json()
      if (result.code === 200) {
        categories.value = result.data
      }
    }
  } catch (error) {
    ElMessage.error('加载分类失败')
  }
}

// 加载分类下的提示词
const loadCategoryPrompts = async (categoryId) => {
  if (!categoryId) return
  try {
    const response = await fetch(`${BASE_URL}/api/prompt/category/${categoryId}`)
    if (response.ok) {
      const result = await response.json()
      if (result.code === 200) {
        prompts.value = result.data
      }
    }
  } catch (error) {
    ElMessage.error('加载提示词失败')
  }
}

// 过滤后的提示词列表
const filteredPrompts = computed(() => {
  if (!searchText.value) return prompts.value
  const searchLower = searchText.value.toLowerCase()
  return prompts.value.filter(prompt => 
    prompt.title.toLowerCase().includes(searchLower) ||
    prompt.description.toLowerCase().includes(searchLower) ||
    prompt.tags.some(tag => tag.toLowerCase().includes(searchLower))
  )
})

// 方法
const handleCategorySelect = async (categoryId) => {
  selectedCategory.value = categoryId
  selectedPrompt.value = null
  selectedPromptId.value = ''
  await loadCategoryPrompts(categoryId)
}

const handlePromptSelect = (promptId) => {
  selectedPromptId.value = promptId
  selectedPrompt.value = prompts.value.find(p => p.id === promptId)
}

const handleAddCategory = () => {
  editingCategory.value = null
  categoryForm.value = {
    name: '',
    description: ''
  }
  showCategoryDialog.value = true
}

const handleAddPrompt = () => {
  editingPrompt.value = null
  promptForm.value = {
    title: '',
    description: '',
    template: '',
    tags: []
  }
  showPromptDialog.value = true
}

const handleEdit = () => {
  if (!selectedPrompt.value) return
  editingPrompt.value = selectedPrompt.value
  promptForm.value = {
    title: selectedPrompt.value.title,
    description: selectedPrompt.value.description,
    template: selectedPrompt.value.template,
    tags: [...selectedPrompt.value.tags]
  }
  showPromptDialog.value = true
}

const handleDelete = async () => {
  if (!selectedPrompt.value) return
  try {
    const response = await fetch(`${BASE_URL}/api/prompt/${selectedPrompt.value.id}`, {
      method: 'DELETE'
    })
    if (response.ok) {
      ElMessage.success('删除成功')
      selectedPrompt.value = null
      selectedPromptId.value = ''
      await loadCategoryPrompts(selectedCategory.value)
    }
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const usePrompt = async () => {
  if (!selectedPrompt.value) return
  try {
    const response = await fetch(`${BASE_URL}/api/prompt/use/${selectedPrompt.value.id}`, {
      method: 'POST'
    })
    if (response.ok) {
      emit('use-prompt', selectedPrompt.value.template)
    }
  } catch (error) {
    ElMessage.error('使用提示词失败')
  }
}

const copyTemplate = async () => {
  if (!selectedPrompt.value) return
  try {
    await navigator.clipboard.writeText(selectedPrompt.value.template)
    ElMessage.success('复制成功')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const saveCategoryForm = async () => {
  try {
    const response = await fetch(`${BASE_URL}/api/prompt/categories`, {
      method: editingCategory.value ? 'PUT' : 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        id: editingCategory.value?.id || undefined,
        ...categoryForm.value
      })
    })
    if (response.ok) {
      const result = await response.json()
      if (result.code === 200) {
        ElMessage.success(editingCategory.value ? '更新成功' : '添加成功')
        showCategoryDialog.value = false
        await loadCategories()
      }
    }
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const savePromptForm = async () => {
  if (!selectedCategory.value) {
    ElMessage.warning('请先选择一个分类')
    return
  }
  
  try {
    const response = await fetch(`${BASE_URL}/api/prompt`, {
      method: editingPrompt.value ? 'PUT' : 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        id: editingPrompt.value?.id || undefined,
        category_id: selectedCategory.value,
        ...promptForm.value
      })
    })
    if (response.ok) {
      const result = await response.json()
      if (result.code === 200) {
        ElMessage.success(editingPrompt.value ? '更新成功' : '添加成功')
        showPromptDialog.value = false
        await loadCategoryPrompts(selectedCategory.value)
      }
    }
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 在组件挂载时加载分类列表
onMounted(async () => {
  await loadCategories()
})
</script>

<style scoped>
.prompt-panel {
  display: grid;
  grid-template-columns: 220px 300px 1fr;
  gap: 16px;
  height: 100%;
  padding: 16px;
  background-color: var(--el-bg-color);
  min-height: 600px;
}

.category-panel,
.prompt-list,
.prompt-preview {
  height: 100%;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  background-color: var(--el-bg-color-overlay);
}

:deep(.el-card) {
  border: 1px solid var(--el-border-color-lighter);
  box-shadow: var(--el-box-shadow-lighter) !important;
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 48px;
  padding: 0 16px;
  border-bottom: 1px solid var(--el-border-color-light);
  background-color: var(--el-bg-color);
  margin: 0 !important;
}

.card-header .icon-btn {
  padding: 6px;
  border: none;
  background: none;
  color: var(--el-text-color-regular);
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s;
}

.card-header .icon-btn:hover {
  color: var(--el-color-primary);
  background-color: var(--el-color-primary-light-9);
}

.card-header :deep(.el-input) {
  width: 180px;
}

.card-header span {
  font-size: 16px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.category-menu,
.prompt-menu {
  border-right: none;
  flex: 1;
  padding: 8px;
}

.prompt-item {
  width: 100%;
  padding: 8px 12px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.prompt-info {
  width: 100%;
}

.prompt-title {
  font-weight: 500;
  font-size: 14px;
  line-height: 1.4;
  color: var(--el-text-color-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.prompt-desc,
.prompt-tags,
.prompt-meta {
  display: none;
}

.preview-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  height: 100%;
  overflow-y: auto;
}

.preview-header {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.preview-header h3 {
  margin: 0;
  font-size: 20px;
  line-height: 1.4;
  color: var(--el-text-color-primary);
}

.preview-desc {
  color: var(--el-text-color-regular);
  margin: 0;
  line-height: 1.6;
  font-size: 14px;
}

.preview-template {
  display: flex;
  flex-direction: column;
  gap: 16px;
  flex: 1;
  background-color: var(--el-fill-color-blank);
  border-radius: 8px;
  padding: 20px;
}

.template-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  color: var(--el-text-color-regular);
  font-size: 14px;
}

.preview-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 20px;
  border-top: 1px solid var(--el-border-color-light);
}

:deep(.el-empty) {
  padding: 40px 0;
}

:deep(.el-tag) {
  border-radius: 4px;
  padding: 0 8px;
  height: 24px;
  line-height: 22px;
}

:deep(.el-input__wrapper) {
  box-shadow: none;
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
}

:deep(.el-input__wrapper:hover) {
  border-color: var(--el-border-color-hover);
}

:deep(.el-input__wrapper.is-focus) {
  border-color: var(--el-color-primary);
  box-shadow: 0 0 0 1px var(--el-color-primary-light-5);
}

:deep(.el-textarea__inner) {
  min-height: 200px !important;
  font-family: var(--el-font-family-monospace);
  line-height: 1.6;
  padding: 16px;
  border-radius: 4px;
  background-color: var(--el-fill-color-blank);
  resize: vertical;
}

:deep(.el-dialog) {
  border-radius: 8px;
  --el-dialog-padding-primary: 24px;
}

:deep(.el-dialog__header) {
  margin-right: 0;
  padding: var(--el-dialog-padding-primary);
  border-bottom: 1px solid var(--el-border-color-light);
}

:deep(.el-dialog__body) {
  padding: var(--el-dialog-padding-primary);
}

:deep(.el-dialog__footer) {
  padding: var(--el-dialog-padding-primary);
  border-top: 1px solid var(--el-border-color-light);
  margin-top: 0;
}

:deep(.el-form-item:last-child) {
  margin-bottom: 0;
}

:deep(.el-select) {
  width: 100%;
}

:deep(.el-scrollbar) {
  height: 100%;
  flex: 1;
}

:deep(.el-menu) {
  border-right: none;
}

:deep(.el-menu-item) {
  height: auto;
  padding: 2px 8px;
  margin: 2px 0;
  border-radius: 4px;
}

:deep(.el-menu-item.is-active) {
  background-color: var(--el-color-primary-light-9);
}

:deep(.el-menu-item:not(.is-active):hover) {
  background-color: var(--el-fill-color-light);
}

:deep(.el-card__header) {
  padding: 0;
  border-bottom: none;
}

:deep(.el-card__body) {
  height: calc(100% - 57px);
  padding: 0;
  display: flex;
  flex-direction: column;
}
</style> 