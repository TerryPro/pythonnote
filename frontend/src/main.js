import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(ElementPlus)

// 添加 ResizeObserver 错误处理
window.addEventListener('error', (event) => {
  if (event.message.includes('ResizeObserver')) {
    event.stopImmediatePropagation();
  }
});

app.mount('#app')
