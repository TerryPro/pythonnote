import { ref, provide, inject } from 'vue'
import { themes } from '@/themes'

const ThemeSymbol = Symbol('theme')

// 组合式函数实现
export function useThemeManager() {
  const currentTheme = ref('light')
  
  const applyTheme = (themeKey) => {
    const theme = themes[themeKey]
    Object.entries(theme.colors).forEach(([key, value]) => {
      document.documentElement.style.setProperty(`--${key}`, value)
    })
    currentTheme.value = themeKey
  }

  // 提供主题给子组件
  const provideTheme = () => {
    provide(ThemeSymbol, {
      currentTheme,
      applyTheme,
      themes
    })
  }

  return {
    currentTheme,
    applyTheme,
    provideTheme
  }
}

// 子组件注入用
export function useTheme() {
  return inject(ThemeSymbol, {
    currentTheme: ref('light'),
    applyTheme: () => {},
    themes: {}
  })
} 