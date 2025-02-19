<template>
  <div>
    <div class="list-toolbar">
      <el-button @click="$emit('refresh')" class="refresh-btn icon-btn">
        <i class="fas fa-sync-alt"></i>
      </el-button>
      <el-button @click="triggerFileUpload" class="upload-btn icon-btn">
        <i class="fas fa-upload"></i>
      </el-button>
    </div>
    
    <div class="file-list">
      <div 
        v-for="file in files" 
        :key="file.path" 
        class="file-item"
        :class="{ active: currentFile === file.path }"
      >
        <div class="file-content">
          <i :class="['fas', getFileIcon(file)]"></i>
          <span class="file-name">{{ file.name }}</span>
        </div>
        <div class="file-actions">
          <button 
            @click="$emit('preview', file)"
            class="icon-btn preview-btn"
            title="预览数据"
          >
            <i class="fas fa-eye"></i>
          </button>
          <button 
            @click="$emit('rename', file)"
            class="icon-btn"
            title="重命名"
          >
            <i class="fas fa-edit"></i>
          </button>
          <button 
            @click="$emit('delete', file)"
            class="icon-btn delete-btn"
            title="删除"
          >
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- 隐藏的文件输入框 -->
    <input
      type="file"
      ref="fileInput"
      @change="handleFileSelect"
      accept=".csv,.xlsx,.xls"
      style="display: none"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { uploadCsvFile, uploadExcelFile } from '@/api/datafile_api'

defineProps({
  files: {
    type: Array,
    required: true
  },
  currentFile: {
    type: String,
    default: ''
  },
  getFileIcon: {
    type: Function,
    required: true
  }
})

const emit = defineEmits(['refresh', 'preview', 'rename', 'delete', 'file-uploaded'])

const fileInput = ref(null)

const triggerFileUpload = () => {
  fileInput.value.click()
}

const handleFileSelect = async (event) => {
  const files = event.target.files
  if (files.length > 0) {
    const file = files[0]
    
    try {
      const fileType = file.name.split('.').pop().toLowerCase()
      let result = null

      if (fileType === 'csv') {
        result = await uploadCsvFile(file)
      } else if (fileType === 'xlsx' || fileType === 'xls') {
        result = await uploadExcelFile(file)
      } else {
        throw new Error('不支持的文件类型')
      }

      if (result.status === 'success') {
        emit('refresh')
        ElMessage.success('文件上传成功')
        emit('file-uploaded', result.data.file_path)
      } else {
        throw new Error(result.message || '上传失败')
      }
    } catch (error) {
      console.error('文件上传失败:', error)
      ElMessage.error('文件上传失败: ' + error.message)
    }
    
    event.target.value = ''
  }
}
</script>

<style scoped>
</style> 