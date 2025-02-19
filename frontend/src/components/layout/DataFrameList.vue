<template>
  <div>
    <div class="list-toolbar">
      <el-button @click="$emit('refresh')" class="refresh-btn icon-btn">
        <i class="fas fa-sync-alt"></i>
      </el-button>
    </div>
    
    <div class="file-list">
      <div 
        v-for="name in dataframes" 
        :key="name" 
        class="file-item"
      >
        <div class="file-content">
          <i class="fas fa-table text-blue-500"></i>
          <span class="file-name">{{ name }}</span>
        </div>
        <div class="file-actions">
          <button 
            @click="$emit('preview', name)"
            class="icon-btn preview-btn"
            title="预览变量"
          >
            <i class="fas fa-eye"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  dataframes: {
    type: Array,
    required: true
  }
})

defineEmits(['refresh', 'preview'])
</script> 