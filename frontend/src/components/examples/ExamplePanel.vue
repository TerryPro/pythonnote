<template>
  <div class="example-panel">
    <!-- 左侧分类列表 -->
    <el-card class="category-panel">
      <template #header>
        <div class="card-header">
          <span class="header-title">代码分类</span>
          <div class="header-actions">
            <button class="icon-btn" @click="handleReload" title="重新加载">
              <el-icon><Refresh /></el-icon>
            </button>
            <button
              v-if="isManageMode"
              class="icon-btn"
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
            <el-icon><component :is="getCategoryIcon(category.id)" /></el-icon>
            <span>{{ category.name }}</span>
          </template>
        </el-menu-item>
      </el-menu>
    </el-card>

    <!-- 中间示例列表 -->
    <el-card class="example-list">
      <template #header>
        <div class="card-header">
          <div class="search-wrapper">
            <el-input
              v-model="searchText"
              placeholder="搜索代码示例..."
              :prefix-icon="Search"
              clearable
              size="small"
            />
          </div>
          <div class="header-actions">
            <button
              v-if="isManageMode"
              class="icon-btn"
              @click="handleAddExample"
              title="添加示例"
            >
              <el-icon><Plus /></el-icon>
            </button>
          </div>
        </div>
      </template>
      <el-scrollbar>
        <el-empty v-if="filteredExamples.length === 0" description="暂无示例" />
        <el-menu
          v-else
          :default-active="selectedExampleId"
          class="example-menu"
          @select="handleExampleSelect"
        >
          <el-menu-item
            v-for="example in filteredExamples"
            :key="example.id"
            :index="example.id"
          >
            <div class="example-item">
              <div class="example-info">
                <el-icon><Document /></el-icon>
                <div class="example-title">{{ example.title }}</div>
              </div>
            </div>
          </el-menu-item>
        </el-menu>
      </el-scrollbar>
    </el-card>

    <!-- 右侧预览区域 -->
    <el-card class="example-preview">
      <template #header>
        <div class="card-header">
          <span class="header-title">示例预览</span>
        </div>
      </template>
      <el-empty
        v-if="!selectedExample"
        description="请选择一个示例查看详情"
      />
      <template v-else>
        <div class="preview-content">
          <div class="preview-header">
            <h3>{{ selectedExample.title }}</h3>
            <el-tag size="small" type="info">
              已使用 {{ selectedExample.use_count }} 次
            </el-tag>
          </div>
          <p class="preview-desc">{{ selectedExample.description }}</p>
          <div class="preview-tags">
            <el-tag
              v-for="tag in selectedExample.tags"
              :key="tag"
              size="small"
              class="tag-item"
            >
              {{ tag }}
            </el-tag>
          </div>
          <div class="preview-code">
            <div class="code-header">
              <div class="code-actions">
                <template v-if="isManageMode">
                  <el-button type="primary" @click="handleEdit" size="small">
                    <el-icon><Edit /></el-icon>编辑
                  </el-button>
                  <el-popconfirm
                    title="确定要删除这个示例吗？"
                    @confirm="handleDelete"
                  >
                    <template #reference>
                      <el-button type="danger" size="small">
                        <el-icon><Delete /></el-icon>删除
                      </el-button>
                    </template>
                  </el-popconfirm>
                </template>
                <template v-else>
                  <el-button type="primary" @click="useExample" size="small">
                    使用此示例
                  </el-button>
                  <el-button @click="copyCode" size="small">
                    复制代码
                  </el-button>
                </template>
              </div>
            </div>
            <el-input
              type="textarea"
              v-model="selectedExample.code"
              :rows="15"
              readonly
              class="code-input"
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

    <!-- 添加/编辑示例对话框 -->
    <el-dialog
      v-model="showExampleDialog"
      :title="editingExample ? '编辑示例' : '添加示例'"
      width="650px"
    >
      <el-form
        ref="exampleFormRef"
        :model="exampleForm"
        :rules="exampleRules"
        label-width="80px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="exampleForm.title" placeholder="请输入示例标题" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="exampleForm.description"
            type="textarea"
            placeholder="请输入示例描述"
          />
        </el-form-item>
        <el-form-item label="代码" prop="code">
          <el-input
            v-model="exampleForm.code"
            type="textarea"
            :rows="6"
            placeholder="请输入Python代码示例"
          />
        </el-form-item>
        <el-form-item label="标签" prop="tags">
          <el-select
            v-model="exampleForm.tags"
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
        <el-button @click="showExampleDialog = false">取消</el-button>
        <el-button type="primary" @click="saveExampleForm">确定</el-button>
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
  Search,
  Refresh,
  Document
} from '@element-plus/icons-vue'
import { API_ENDPOINTS, apiCall } from '@/api/http'

const props = defineProps({
  mode: {
    type: String,
    default: 'use' // 'use' or 'manage'
  }
})

const emit = defineEmits(['use-example'])

// 状态变量
const selectedCategory = ref('')
const selectedExampleId = ref('')
const selectedExample = ref(null)
const searchText = ref('')
const showCategoryDialog = ref(false)
const showExampleDialog = ref(false)
const editingCategory = ref(null)
const editingExample = ref(null)

// 表单数据
const categoryForm = ref({
  name: '',
  description: ''
})

const exampleForm = ref({
  title: '',
  description: '',
  code: '',
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

const exampleRules = {
  title: [
    { required: true, message: '请输入示例标题', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入示例描述', trigger: 'blur' },
    { max: 200, message: '最多 200 个字符', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入示例代码', trigger: 'blur' }
  ],
  tags: [
    { required: true, message: '请至少选择一个标签', trigger: 'change' }
  ]
}

// 可用标签列表
const availableTags = ref([
  '基础语法',
  '数据类型',
  '文件操作',
  '数据处理',
  '算法'
])

// 计算属性
const isManageMode = computed(() => props.mode === 'manage')

// 修改模拟数据为实际API调用
const categories = ref([])
const examples = ref([])

// 加载分类列表
const loadCategories = async () => {
  try {
    const result = await apiCall(API_ENDPOINTS.CODE_EXAMPLES.CATEGORIES)
    categories.value = result
  } catch (error) {
    ElMessage.error('加载分类失败')
    console.error('加载分类失败:', error)
    categories.value = []
  }
}

// 加载分类下的示例
const loadExamples = async (categoryId) => {
  try {
    const result = await apiCall(API_ENDPOINTS.CODE_EXAMPLES.CATEGORIES_ID(categoryId))
    examples.value = result
  } catch (error) {
    console.error('加载示例失败:', error)
    ElMessage.error(`加载示例失败: ${error.message}`)
    examples.value = []
  }
}

// 过滤后的示例列表
const filteredExamples = computed(() => {
  if (!searchText.value) return examples.value
  const searchLower = searchText.value.toLowerCase()
  return examples.value.filter(example => 
    example.title.toLowerCase().includes(searchLower) ||
    example.description.toLowerCase().includes(searchLower) ||
    example.tags.some(tag => tag.toLowerCase().includes(searchLower))
  )
})

// 获取分类图标
const getCategoryIcon = (categoryId) => {
  const iconMap = {
    'data_explore': 'Search',
    'data_preprocess': 'Tools',
    'data_visualization': 'PieChart',
    'statistical_analysis': 'TrendCharts',
    'data_export': 'Upload',
    'time_series': 'Timer'
  }
  return iconMap[categoryId] || 'Document'
}

// 方法
const handleCategorySelect = async (categoryId) => {
  selectedCategory.value = categoryId
  selectedExample.value = null
  selectedExampleId.value = ''
  await loadExamples(categoryId)
}

const handleExampleSelect = (exampleId) => {
  selectedExampleId.value = exampleId
  selectedExample.value = examples.value.find(p => p.id === exampleId)
}

const handleAddCategory = () => {
  editingCategory.value = null
  categoryForm.value = {
    name: '',
    description: ''
  }
  showCategoryDialog.value = true
}

const handleAddExample = () => {
  if (!selectedCategory.value) {
    ElMessage.warning('请先选择一个分类')
    return
  }
  
  editingExample.value = null
  exampleForm.value = {
    title: '',
    description: '',
    code: '',
    tags: []
  }
  showExampleDialog.value = true
}

const handleEdit = () => {
  if (!selectedExample.value) return
  editingExample.value = selectedExample.value
  exampleForm.value = {
    title: selectedExample.value.title,
    description: selectedExample.value.description,
    code: selectedExample.value.code,
    tags: [...selectedExample.value.tags]
  }
  showExampleDialog.value = true
}

const handleDelete = async () => {
  if (!selectedExample.value) return
  try {
    await apiCall(API_ENDPOINTS.CODE_EXAMPLES.CODE_EXAMPLES_ID(selectedExample.value.id), {
      method: 'DELETE'
    })
    ElMessage.success('删除成功')
    selectedExample.value = null
    selectedExampleId.value = ''
    await loadExamples(selectedCategory.value)
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const useExample = async () => {
  if (!selectedExample.value) return
  
  // 直接发出事件，不需要调用API
  emit('use-example', selectedExample.value.code)
  
  // 可以添加一个成功提示
  ElMessage.success('代码已添加到单元格')
}

const copyCode = async () => {
  if (!selectedExample.value) return
  try {
    await navigator.clipboard.writeText(selectedExample.value.code)
    ElMessage.success('复制成功')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const handleReload = async () => {
  try {
    await loadCategories()
    if (selectedCategory.value) {
      await loadExamples(selectedCategory.value)
    }
    ElMessage.success('重新加载成功')
  } catch (error) {
    ElMessage.error('重新加载失败')
  }
}

const saveCategoryForm = async () => {
  try {
    const endpoint = editingCategory.value 
      ? API_ENDPOINTS.CODE_EXAMPLES.CATEGORIES_ID(editingCategory.value.id)
      : API_ENDPOINTS.CODE_EXAMPLES.CATEGORIES
    
    const result = await apiCall(endpoint, {
      method: editingCategory.value ? 'PUT' : 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        id: editingCategory.value?.id || undefined,
        ...categoryForm.value
      })
    })
    
    console.log(result)

    ElMessage.success(editingCategory.value ? '更新成功' : '添加成功')
    showCategoryDialog.value = false
    await loadCategories()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const saveExampleForm = async () => {
  if (!selectedCategory.value) {
    ElMessage.warning('请先选择一个分类')
    return
  }
  
  try {
    const endpoint = editingExample.value
      ? API_ENDPOINTS.CODE_EXAMPLES.CODE_EXAMPLES_ID(editingExample.value.id)
      : API_ENDPOINTS.CODE_EXAMPLES.CODE_EXAMPLES
   
    const result = await apiCall(endpoint, {
      method: editingExample.value ? 'PUT' : 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        id: editingExample.value?.id || undefined,
        category_id: selectedCategory.value,
        ...exampleForm.value
      })
    })
    
    console.log(result)
    ElMessage.success(editingExample.value ? '更新成功' : '添加成功')
    showExampleDialog.value = false
    await loadExamples(selectedCategory.value)
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 初始化
onMounted(async () => {
  console.log('组件挂载，开始加载分类...')
  await loadCategories()
})
</script>

<style scoped>
.example-panel {
  display: flex;
  gap: 16px;
  height: 600px;  /* 设置固定高度 */
}

.category-panel {
  width: 200px;
  display: flex;
  flex-direction: column;
}

.example-list {
  width: 300px;
  display: flex;
  flex-direction: column;
}

.example-preview {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 40px; /* 统一header高度 */
  padding: 0 4px;
}

.header-title {
  font-size: 16px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.search-wrapper {
  flex: 1;
  margin-right: 8px;
  max-width: 220px;
}

.search-wrapper :deep(.el-input__wrapper) {
  padding-right: 8px;
}

.search-wrapper :deep(.el-input__inner) {
  height: 32px;
  line-height: 32px;
}

.header-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.icon-btn {
  padding: 6px;
  border: none;
  background: none;
  cursor: pointer;
  color: var(--el-text-color-regular);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.icon-btn:hover {
  color: var(--el-color-primary);
  background-color: var(--el-fill-color-light);
}

.category-menu {
  border-right: none;
}

.example-menu {
  border-right: none;
}

.example-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.example-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.example-title {
  font-size: 14px;
}

.preview-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: 100%;
  overflow: hidden;  /* 防止内容溢出 */
}

.preview-header {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-header h3 {
  margin: 0;
  font-size: 18px;
  color: var(--el-text-color-primary);
}

.preview-desc {
  flex-shrink: 0;
  color: var(--el-text-color-regular);
  margin: 0;
  line-height: 1.5;
}

.preview-tags {
  flex-shrink: 0;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.preview-code {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;  /* 自动填充剩余空间 */
  min-height: 0;  /* 允许内容区域收缩 */
  overflow: hidden;  /* 防止内容溢出 */
}

.code-header {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.code-actions {
  flex-shrink: 0;
  display: flex;
  gap: 8px;
}

.code-input {
  height: 100%;
  font-family: 'Fira Code', monospace;
  overflow: hidden;  /* 防止内容溢出 */
}

.code-input :deep(.el-textarea__inner) {
  height: 100% !important;
  padding: 12px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
  resize: none;
  overflow-y: auto;  /* 添加垂直滚动条 */
}

/* 自定义滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: var(--el-border-color-lighter);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: var(--el-border-color);
}
</style> 