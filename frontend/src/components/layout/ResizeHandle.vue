<template>
  <div 
    class="resize-handle"
    @mousedown="handleMouseDown"
    @touchstart="handleTouchStartWrapper"
  >
    <div class="resize-handle-line"></div>
  </div>
</template>

<script setup>
import { useResizePanel } from '@/composables/useResizePanel'

const { startResize, handleResize, stopResize, handleTouchStart, handleTouchMove, handleTouchEnd } = useResizePanel()

const handleMouseDown = (e) => {
  e.preventDefault()
  startResize(e)
  
  const handleMouseMove = (e) => {
    handleResize(e)
  }
  
  const handleMouseUp = () => {
    document.removeEventListener('mousemove', handleMouseMove)
    document.removeEventListener('mouseup', handleMouseUp)
    stopResize()
  }

  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
}

const handleTouchStartWrapper = (e) => {
  handleTouchStart(e)
  
  const handleTouchMoveWrapper = (e) => {
    handleTouchMove(e)
  }
  
  const handleTouchEndWrapper = () => {
    document.removeEventListener('touchmove', handleTouchMoveWrapper)
    document.removeEventListener('touchend', handleTouchEndWrapper)
    handleTouchEnd()
  }

  document.addEventListener('touchmove', handleTouchMoveWrapper)
  document.addEventListener('touchend', handleTouchEndWrapper)
}
</script>

<style scoped>
</style>