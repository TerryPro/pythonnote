import { defineStore } from 'pinia'

export const useResizePanelStore = defineStore('resizePanel', {
  state: () => ({
    panelWidth: 250,
    isDragging: false,
    startX: 0,
    startWidth: 250,
  }),
  actions: {
    setPanelWidth(width) {
      this.panelWidth = Math.max(250, Math.min(400, width))
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