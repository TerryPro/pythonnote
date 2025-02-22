<template>
  <div class="prompt-panel">
    <!-- 左侧分类列表 -->
    <el-card class="category-panel" shadow="never">
      <template #header>
        <div class="card-header">
          <span>提示词分类</span>
          <div class="header-actions">
            <button
              class="icon-btn borderless"
              @click="handleReload"
              title="重新加载"
            >
              <el-icon><Refresh /></el-icon>
            </button>
            <button
              v-if="isManageMode"
              class="icon-btn borderless"
              @click="handleAddCategory"
              title="添加分类"
            >
              <el-icon><Plus /></el-icon>
            </button>
          </div>
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
            <i :class="getCategoryIcon(category.id)"></i>
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
                <i :class="getPromptIcon(prompt)"></i>
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
            <h3>{{ selectedPrompt.title }} <el-tag size="small" type="info">已使用 {{ selectedPrompt.use_count }} 次</el-tag></h3>
          </div>
          <p class="preview-desc">{{ selectedPrompt.description }}</p>
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
          <div class="preview-template">
            <el-input
              type="textarea"
              v-model="selectedPrompt.template"
              :rows="6"
              readonly
            />
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
import { API_CONFIG } from '@/api/http'
import {
  Plus,
  Edit,
  Delete,
  Search,
  Refresh
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

// 加载分类列表
const loadCategories = async () => {
  try {
    const response = await fetch(`${API_CONFIG.BASE_URL}/api/prompt/categories`)
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
    const response = await fetch(`${API_CONFIG.BASE_URL}/api/prompt/category/${categoryId}`)
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
    const response = await fetch(`${API_CONFIG.BASE_URL}/api/prompt/${selectedPrompt.value.id}`, {
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
    const response = await fetch(`${API_CONFIG.BASE_URL}/api/prompt/use/${selectedPrompt.value.id}`, {
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
    const response = await fetch(`${API_CONFIG.BASE_URL}/api/prompt/categories`, {
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
    const response = await fetch(`${API_CONFIG.BASE_URL}/api/prompt`, {
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

// 重新加载提示词
const handleReload = async () => {
  try {
    const response = await fetch(`${API_CONFIG.BASE_URL}/api/prompt/reload`, {
      method: 'POST'
    })
    if (!response.ok) {
      throw new Error('重新加载失败')
    }
    await loadCategories() // 重新加载分类列表
    ElMessage.success('重新加载成功')
  } catch (error) {
    console.error('重新加载失败:', error)
    ElMessage.error('重新加载失败')
  }
}

// 获取分类图标
const getCategoryIcon = (categoryId) => {
  const iconMap = {
    'data_exploration': 'fas fa-search',
    'data_preprocessing': 'fas fa-tools',
    'data_visualization': 'fas fa-chart-bar',
    'statistical_analysis': 'fas fa-calculator',
    'data_export': 'fas fa-file-export'
  }
  return iconMap[categoryId] || 'fas fa-folder'
}

// 获取提示词图标
const getPromptIcon = (prompt) => {
  // 根据提示词的id或tags来决定使用什么图标
  if (prompt.id.includes('plot') || prompt.tags.includes('可视化')) {
    return 'fas fa-chart-line'
  }
  if (prompt.id.includes('analysis') || prompt.tags.includes('统计分析')) {
    return 'fas fa-chart-pie'
  }
  if (prompt.id.includes('check') || prompt.tags.includes('数据质量')) {
    return 'fas fa-check-circle'
  }
  if (prompt.id.includes('test') || prompt.tags.includes('统计检验')) {
    return 'fas fa-vial'
  }
  if (prompt.id.includes('distribution') || prompt.tags.includes('数据分布')) {
    return 'fas fa-wave-square'
  }
  if (prompt.id.includes('correlation') || prompt.tags.includes('相关性')) {
    return 'fas fa-project-diagram'
  }
  if (prompt.id.includes('engineering') || prompt.tags.includes('特征工程')) {
    return 'fas fa-cogs'
  }
  if (prompt.id.includes('clean') || prompt.tags.includes('数据清洗')) {
    return 'fas fa-broom'
  }
  return 'fas fa-file-alt' // 默认图标
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
  height: 600px;
  padding: 16px;
  background-color: var(--el-bg-color);
}

.category-panel,
.prompt-list,
.prompt-preview {
  height: 100%;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  background-color: var(--el-bg-color-overlay);
  overflow: hidden;
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
  flex: 1;
  overflow-y: auto;
  border-right: none;
  padding: 8px;
}

.prompt-item {
  width: 100%;
  padding: 8px 12px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.prompt-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.prompt-info i {
  font-size: 14px;
  width: 16px;
  color: var(--el-text-color-regular);
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
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
}

.preview-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.preview-header h3 {
  margin: 0;
  font-size: 18px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.preview-desc {
  margin: 0;
  color: var(--el-text-color-secondary);
  text-align: left;
}

.preview-template {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.preview-template :deep(.el-textarea) {
  height: 100%;
}

.preview-template :deep(.el-textarea__inner) {
  height: 100% !important;
  min-height: unset !important;
  resize: none;
}

.preview-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
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
  overflow: hidden;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.icon-btn {
  padding: 2px;
  border: none;
  background: none;
  cursor: pointer;
  color: var(--el-text-color-regular);
  transition: color 0.2s;

  &:hover {
    color: var(--el-color-primary);
  }
}
</style> 