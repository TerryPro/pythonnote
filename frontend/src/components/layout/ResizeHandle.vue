<template>
  <div 
    class="resize-handle"
    @mousedown="handleMouseDown"
    @touchstart="handleTouchStart"
  >
    <div class="resize-handle-line"></div>
  </div>
</template>

<script setup>

const emit = defineEmits(['resize-start', 'resize-move', 'resize-end'])

const handleMouseDown = (e) => {
  e.preventDefault()
  emit('resize-start', e)
  
  const handleMouseMove = (e) => {
    emit('resize-move', e)
  }
  
  const handleMouseUp = () => {
    document.removeEventListener('mousemove', handleMouseMove)
    document.removeEventListener('mouseup', handleMouseUp)
    emit('resize-end')
  }

  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
}

const handleTouchStart = (e) => {
  const touch = e.touches[0]
  emit('resize-start', touch)
  
  const handleTouchMove = (e) => {
    const touch = e.touches[0]
    emit('resize-move', touch)
  }
  
  const handleTouchEnd = () => {
    document.removeEventListener('touchmove', handleTouchMove)
    document.removeEventListener('touchend', handleTouchEnd)
    emit('resize-end')
  }

  document.addEventListener('touchmove', handleTouchMove)
  document.addEventListener('touchend', handleTouchEnd)
}
</script>

<style scoped>
.resize-handle {
  position: relative;
  width: 6px;
  cursor: col-resize;
  background-color: transparent;
  z-index: 100;
  height: 100%;
}

.resize-handle-line {
  position: absolute;
  left: 2px;
  width: 2px;
  height: 100%;
  background-color: var(--el-border-color);
  transition: background-color 0.2s;
}

.resize-handle:hover .resize-handle-line,
.resize-handle:active .resize-handle-line {
  background-color: var(--el-color-primary);
}
</style> 