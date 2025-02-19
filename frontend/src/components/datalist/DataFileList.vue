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
            @click="handlePreview(file)"
            class="icon-btn preview-btn"
            title="预览数据"
          >
            <i class="fas fa-eye"></i>
          </button>
          <button 
            @click="triggerRename(file)"
            class="icon-btn"
            title="重命名"
          >
            <i class="fas fa-edit"></i>
          </button>
          <button 
            @click="handleDelete(file)"
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

    <!-- 添加数据文件重命名对话框 -->
    <el-dialog
      v-model="renameDialogVisible"
      title="重命名数据文件"
      width="30%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <el-form :model="renameForm" label-width="0px">
        <el-form-item>
          <el-input
            v-model="renameForm.newName"
            placeholder="请输入新的文件名"
            @keyup.enter="handleRename"
          >
            <template #append>{{ renameForm.extension }}</template>
          </el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="renameDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleRename">确认</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 添加数据预览组件 -->
    <FileExplore 
      ref="dataImportRef"
      @data-loaded="$emit('data-loaded', $event)"
      @insert-code="$emit('insert-code', $event)"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox, ElDialog, ElForm, ElFormItem, ElInput } from 'element-plus'
import { uploadCsvFile, uploadExcelFile, api_deleteDataFile, api_renameDataFile, previewCsvFile, previewExcelFile } from '@/api/datafile_api'
import FileExplore from '@/components/DataExplorer/FileExplore.vue'

const props = defineProps({
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

const emit = defineEmits(['refresh', 'preview', 'file-uploaded', 'update:currentFile'])

const fileInput = ref(null)

// 添加重命名相关响应式变量
const renameDialogVisible = ref(false)
const renameForm = ref({
  newName: '',
  file: null,
  extension: ''
})

// 添加预览相关的引用
const dataImportRef = ref(null)

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

const handleDelete = async (file) => {
  try {
    const confirm = await ElMessageBox.confirm(
      `确定要永久删除文件 ${file.name} 吗？`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    if (confirm) {
      await api_deleteDataFile(file.path)
      ElMessage.success('文件删除成功')
      emit('refresh')
      // 如果删除的是当前选中文件，清空选中状态
      if (props.currentFile === file.path) {
        emit('update:currentFile', '')
      }
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(`文件删除失败: ${error.message}`)
    }
  }
}

// 重命名处理方法
const handleRename = async () => {
  if (!renameForm.value.newName.trim()) {
    ElMessage.warning('文件名不能为空')
    return
  }
  
  const newFilename = renameForm.value.newName + renameForm.value.extension
  
  try {
    await api_renameDataFile(renameForm.value.file.path, newFilename)
    await emit('refresh')
    renameDialogVisible.value = false
    ElMessage.success('文件重命名成功')
    
    // 如果重命名的是当前选中文件，更新选中状态
    if (props.currentFile === renameForm.value.file.path) {
      emit('update:currentFile', newFilename)
    }
  } catch (error) {
    console.error('文件重命名失败:', error)
    ElMessage.error('文件重命名失败: ' + error.message)
  }
}

// 触发重命名对话框
const triggerRename = (file) => {
  const extension = '.' + file.name.split('.').pop()
  renameForm.value = {
    newName: file.name.replace(extension, ''),
    file: file,
    extension: extension
  }
  renameDialogVisible.value = true
}

// 预览数据文件
const handlePreview = async (file) => {
  emit('update:currentFile', file.path)
  if (dataImportRef.value) {
    try {
      const fileType = file.name.split('.').pop().toLowerCase()
      var result = null
      if (fileType === 'csv') {
        result = await previewCsvFile(file.path)
      } else if (fileType === 'xlsx' || fileType === 'xls') {
        result = await previewExcelFile(file.path)
      } else {
        throw new Error('不支持的文件类型')
      }

      if (result.status === 'success') {
        dataImportRef.value.previewData = result.data
        dataImportRef.value.previewDataFile(file)
      } else {
        throw new Error(result.message || '加载失败')
      }
    } catch (error) {
      console.error('加载数据文件失败:', error)
      ElMessage.error('加载数据文件失败: ' + error.message)
    }
  }
}
</script>

<style scoped>
</style> 