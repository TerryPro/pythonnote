import { useResizePanelStore } from '@/stores/resizePanelStore'

export function useResizePanel() {
  const store = useResizePanelStore()

  const startResize = (e) => {
    store.setIsDragging(true)
    store.setStartX(e.clientX)
    store.setStartWidth(store.panelWidth)
    document.body.classList.add('resizing')
  }

  const handleResize = (e) => {
    if (!store.isDragging) return
    const newWidth = store.startWidth + (e.clientX - store.startX)
    store.setPanelWidth(newWidth)
  }

  const stopResize = () => {
    store.setIsDragging(false)
    document.body.classList.remove('resizing')
  }

  const handleTouchStart = (e) => {
    const touch = e.touches[0]
    store.setIsDragging(true)
    store.setStartX(touch.clientX)
    store.setStartWidth(store.panelWidth)
    document.body.classList.add('resizing')
  }

  const handleTouchMove = (e) => {
    if (!store.isDragging) return
    const touch = e.touches[0]
    const newWidth = store.startWidth + (touch.clientX - store.startX)
    store.setPanelWidth(newWidth)
  }

  const handleTouchEnd = () => {
    store.setIsDragging(false)
    document.body.classList.remove('resizing')
  }

  return {
    panelWidth: store.panelWidth,
    startResize,
    handleResize,
    stopResize,
    handleTouchStart,
    handleTouchMove,
    handleTouchEnd
  }
}