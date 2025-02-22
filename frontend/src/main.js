import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import './styles/index.scss'  // 导入主样式文件
const app = createApp(App)
const pinia = createPinia()
// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(ElementPlus)
app.use(pinia)
// 添加 ResizeObserver 错误处理
window.addEventListener('error', (event) => {
  if (event.message.includes('ResizeObserver')) {
    event.stopImmediatePropagation();
  }
});

app.mount('#app')
