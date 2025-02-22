<template>
  <div>
    <div class="list-toolbar">
      <el-button @click="dataframeStore.fetchDataFrames()" class="refresh-btn icon-btn">
        <i class="fas fa-sync-alt"></i>
      </el-button>
    </div>
    
    <div class="file-list">
      <!-- 右键菜单 -->
      <div 
        v-show="contextMenu.visible"
        class="context-menu"
        :style="{ left: contextMenu.x + 'px', top: contextMenu.y + 'px' }"
      >
        <div class="menu-item" @click="handlePreview">
          <i class="fas fa-eye mr-2"></i>预览变量
        </div>
      </div>

      <!-- 修改文件项添加右键事件 -->
      <div 
        v-for="name in dataframes" 
        :key="name" 
        class="file-item"
        @contextmenu.prevent="showContextMenu($event, name)"
      >
        <div class="file-content">
          <i class="fas fa-table text-blue-500"></i>
          <span class="file-name">{{ name }}</span>
        </div>
      </div>
    </div>

    <!-- 添加DataFrame预览组件 -->
    <DataFramePreview
      v-model="showPreview"
      :title="previewTitle"
      :dataframe-name="currentDataframe"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import DataFramePreview from '@/components/datapanel/DataFramePreview.vue'
import { useDataFrameStore } from '@/stores/dataframeStore'

const dataframeStore = useDataFrameStore()

// 组件挂载时启动自动刷新
onMounted(async () => {
  await dataframeStore.fetchDataFrames()
  dataframeStore.startAutoRefresh()
})

// 组件卸载时停止自动刷新
onUnmounted(() => {
  dataframeStore.stopAutoRefresh()
})

const dataframes = computed(() => dataframeStore.dataframes)

const showPreview = ref(false)
const previewTitle = ref('')
const currentDataframe = ref('')

// 添加右键菜单状态
const contextMenu = ref({
  visible: false,
  x: 0,
  y: 0,
  selectedName: ''
});

// 显示右键菜单
const showContextMenu = (event, name) => {
  contextMenu.value = {
    visible: true,
    x: event.clientX,
    y: event.clientY,
    selectedName: name
  };
  // 添加点击外部关闭菜单的监听
  document.addEventListener('click', closeContextMenu);
};

// 处理预览操作
const handlePreview = () => {
  if (contextMenu.value.selectedName) {
    previewDataFrame(contextMenu.value.selectedName);
  }
  closeContextMenu();
};

// 关闭右键菜单
const closeContextMenu = () => {
  contextMenu.value.visible = false;
  document.removeEventListener('click', closeContextMenu);
};

const previewDataFrame = (name) => {
  currentDataframe.value = name
  previewTitle.value = name
  showPreview.value = true
}
</script>

<style scoped lang="scss">
@import '@/styles/components/_menu.scss'; // 直接使用已定义的类

.file-item {
  padding: 0.5rem;
  &:hover {
    background-color: #dbeafe;
  }
  &.active {
    background-color: #eff6ff;
  }
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>