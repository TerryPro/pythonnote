<template>
  <el-tooltip
    content="AI 代码助手"
    placement="top"
    :hide-after="1000"
  >
    <el-button
      class="ai-btn"
      type="primary"
      :icon="Magic"
      circle
      @click="$emit('click')"
    />
  </el-tooltip>
</template>

<script setup>
import { Magic } from '@element-plus/icons-vue'
</script>

<style scoped>
.ai-btn {
  background: linear-gradient(45deg, #409EFF, #79bbff);
  border: none;
  transition: all 0.3s ease;
}

.ai-btn:hover {
  transform: scale(1.05);
  background: linear-gradient(45deg, #79bbff, #409EFF);
  border: none;
}
</style> 