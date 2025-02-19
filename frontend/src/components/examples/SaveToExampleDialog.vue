<template>
  <el-dialog
    title="保存到示例库"
    v-model="dialogVisible"
    width="50%"
    :before-close="handleClose"
  >
    <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
      <el-form-item label="标题" prop="title">
        <el-input v-model="form.title" placeholder="请输入示例代码标题"/>
      </el-form-item>
      
      <el-form-item label="分类" prop="category_id">
        <el-select v-model="form.category_id" placeholder="请选择分类">
          <el-option
            v-for="category in categories"
            :key="category.id"
            :label="category.name"
            :value="category.id"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="描述" prop="description">
        <el-input
          type="textarea"
          v-model="form.description"
          :rows="4"
          placeholder="请输入示例代码描述"
        />
      </el-form-item>
      
      <el-form-item label="标签">
        <el-select
          v-model="form.tags"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="请选择或输入标签"
        >
          <el-option
            v-for="tag in recommendedTags"
            :key="tag"
            :label="tag"
            :value="tag"
          />
        </el-select>
      </el-form-item>
    </el-form>
    
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">
          保存
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { API_ENDPOINTS, apiCall } from '@/api/http'

const props = defineProps({
  modelValue: Boolean,
  code: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'saved'])

// 表单数据
const form = ref({
  title: '',
  category_id: '',
  description: '',
  tags: []
})

// 表单验证规则
const rules = {
  title: [
    { required: true, message: '请输入标题', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  category_id: [
    { required: true, message: '请选择分类', trigger: 'change' }
  ]
}

// 分类列表
const categories = ref([])
// 推荐标签
const recommendedTags = ref([
  'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly',
  '数据处理', '数据分析', '数据可视化', '机器学习', '深度学习',
  '基础操作', '进阶操作', '高级操作'
])

const formRef = ref(null)
const saving = ref(false)

// 计算属性：对话框可见性
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 获取分类列表
const fetchCategories = async () => {
  try {
    const result = await apiCall(API_ENDPOINTS.CODE_EXAMPLES.CATEGORIES)
    categories.value = result
  } catch (error) {
    console.error('获取分类失败:', error)
    ElMessage.error('获取分类失败')
  }
}

// 保存示例
const handleSave = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    saving.value = true
    try {
      const result = await apiCall(API_ENDPOINTS.CODE_EXAMPLES.SAVE_FROM_CELL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...form.value,
          code: props.code
        })
      })
      ElMessage.success('保存成功')
      emit('saved', result)
      handleClose()
    } catch (error) {
      console.error('保存失败:', error)
      ElMessage.error(error.message || '保存失败')
    } finally {
      saving.value = false
    }
  })
}

// 关闭对话框
const handleClose = () => {
  formRef.value?.resetFields()
  dialogVisible.value = false
}

// 组件挂载时获取分类列表
onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style> 