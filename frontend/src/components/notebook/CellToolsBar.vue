<template>
  <div class="cell-type-selector">
    <select 
      :value="type" 
      @change="(e) => $emit('update:type', e.target.value)"
      class="type-select"
    >
      <option value="code">代码单元格</option>
      <option value="markdown">Markdown单元格</option>
    </select>
    <div class="cell-actions">
      <button 
        v-if="type === 'code'"
        @click="$emit('execute')"
        class="icon-btn" 
        title="运行代码"
      >
        <i class="fas fa-play"></i>
      </button>
      <button 
        v-if="type === 'code'"
        @click="$emit('openExample')"
        class="icon-btn"
        title="代码示例"
      >
        <i class="fas fa-file-code"></i>
      </button>
      <button 
        v-if="type === 'code'"
        @click="$emit('openAiDialog')"
        class="icon-btn ai-btn" 
        title="AI代码助手"
      >
        <i class="fas fa-magic"></i>
      </button>
      <button 
        v-else
        @click="$emit('toggleEdit')"
        class="icon-btn" 
        :title="isEditing ? '预览' : '编辑'"
      >
        <i :class="isEditing ? 'fas fa-eye' : 'fas fa-edit'"></i>
      </button>
      <button 
        @click="$emit('copy')"
        class="icon-btn"
        title="复制内容"
      >
        <i class="fas fa-copy"></i>
      </button>
      <button 
        @click="$emit('addAbove')"
        class="icon-btn"
        title="在上方添加单元格"
      >
        <i class="fas fa-file-circle-plus" style="transform: rotate(-90deg);"></i>
      </button>
      <button 
        @click="$emit('addBelow')"
        class="icon-btn"
        title="在下方添加单元格"
      >
        <i class="fas fa-file-circle-plus" style="transform: rotate(90deg);"></i>
      </button>
      <button 
        @click="$emit('moveUp')"
        class="icon-btn" 
        title="向上移动"
        :disabled="isFirst"
      >
        <i class="fas fa-arrow-up"></i>
      </button>
      <button 
        @click="$emit('moveDown')"
        class="icon-btn" 
        title="向下移动"
        :disabled="isLast"
      >
        <i class="fas fa-arrow-down"></i>
      </button>
      <button 
        @click="$emit('delete')"
        class="icon-btn delete-btn" 
        title="删除单元格"
      >
        <i class="fas fa-trash"></i>
      </button>
      <button 
        v-if="type === 'code'"
        @click="$emit('saveToExample')"
        class="icon-btn"
        title="保存到示例库"
      >
        <i class="fas fa-save"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    required: true
  },
  isEditing: {
    type: Boolean,
    default: false
  },
  isFirst: {
    type: Boolean,
    default: false
  },
  isLast: {
    type: Boolean,
    default: false
  }
})

defineEmits([
  'update:type',
  'execute',
  'openExample',
  'openAiDialog',
  'toggleEdit',
  'copy',
  'addAbove',
  'addBelow',
  'moveUp',
  'moveDown',
  'delete',
  'saveToExample'
])
</script>

<style lang="scss" scoped>
.cell-type-selector {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 4px 0;
  margin-bottom: 2px;
}

.type-select {
  padding: 6px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: var(--cell-background);
  color: var(--text-color);
  font-size: 13px;
  cursor: pointer;
  outline: none;
  min-width: 100px;
  transition: all 0.3s ease;
}

.cell-actions {
  display: flex;
  gap: 4px;
  align-items: center;
}

</style>