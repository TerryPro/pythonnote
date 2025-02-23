import { defineStore } from 'pinia'

export const useResizePanelStore = defineStore('resizePanel', {
  state: () => ({
    panelWidth: 300,
    isDragging: false,
    startX: 0,
    startWidth: 300,
  }),
  actions: {
    setPanelWidth(width) {
      this.panelWidth = Math.max(200, Math.min(500, width))
    },
    setIsDragging(value) {
      this.isDragging = value
    },
    setStartX(value) {
      this.startX = value
    },
    setStartWidth(value) {
      this.startWidth = value
    },
  },
})