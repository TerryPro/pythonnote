<template>
  <Transition name="fade">
    <div v-if="loading.isLoading" class="loading-mask">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <div class="loading-text">{{ loading.loadingMessage }}</div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { useLoadingStore } from '@/stores/loadingStore'

const loading = useLoadingStore()
</script>

<style scoped>
.loading-mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-content {
  text-align: center;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

.loading-text {
  color: #333;
  font-size: 18px;
  font-weight: bold;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 