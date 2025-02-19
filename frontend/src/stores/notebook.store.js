import { defineStore } from 'pinia'

export const useNotebookStore = defineStore('notebook', {
  state: () => ({
    // 笔记本相关状态（后续迁移）
    cells: [],
    cellContents: {},
    cellOutputs: {},
    cellTypes: {},
    currentFile: null
  }),
  actions: {
    // 笔记本操作方法（后续迁移）
    async createNewNotebook() {},
    async saveNotebook() {}
  }
}) 