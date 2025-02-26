import { defineStore } from 'pinia'

export const useLoadingStore = defineStore('loading', {
  state: () => ({
    isLoading: false,
    loadingMessage: '加载中...'
  }),
  actions: {
    startLoading(message = '加载中...') {
      this.loadingMessage = message
      this.isLoading = true
    },
    endLoading() {
      this.isLoading = false
      this.loadingMessage = '加载中...'
    }
  }
}) 