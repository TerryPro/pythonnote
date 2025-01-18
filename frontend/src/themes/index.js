// 主题配置
export const themes = {
  light: {
    name: '浅色主题',
    colors: {
      primary: '#1976D2',
      background: '#f5f7fa',
      text: '#2c3e50',
      border: '#e0e0e0',
      cellBackground: '#ffffff',
      toolbarBackground: '#1976D2',
      toolbarText: '#ffffff',
      codeBackground: '#f8f9fa',
      markdownBackground: '#ffffff',
      buttonHover: '#f5f5f5',
      buttonActive: '#e8e8e8',
      selection: '#e3f2fd',
      filePanel: '#ffffff',
      filePanelHover: '#f5f7fa',
      filePanelActive: '#e3f2fd',
      filePanelText: '#2c3e50'
    }
  },
  dark: {
    name: '深色主题',
    colors: {
      primary: '#64B5F6',
      background: '#1a1a1a',
      text: '#e0e0e0',
      border: '#333333',
      cellBackground: '#242424',
      toolbarBackground: '#1e1e1e',
      toolbarText: '#e0e0e0',
      codeBackground: '#1e1e1e',
      markdownBackground: '#242424',
      buttonHover: '#2c2c2c',
      buttonActive: '#404040',
      selection: '#0d47a1',
      filePanel: '#242424',
      filePanelHover: '#2c2c2c',
      filePanelActive: '#333333',
      filePanelText: '#e0e0e0'
    }
  },
  sepia: {
    name: '护眼模式',
    colors: {
      primary: '#795548',
      background: '#f4ecd8',
      text: '#5b4636',
      border: '#d7cbb5',
      cellBackground: '#fdf6e3',
      toolbarBackground: '#8b6b5f',
      toolbarText: '#fdf6e3',
      codeBackground: '#eee8d5',
      markdownBackground: '#fdf6e3',
      buttonHover: '#efe4cc',
      buttonActive: '#e6d9bc',
      selection: '#d7cbb5',
      filePanel: '#fdf6e3',
      filePanelHover: '#f4ecd8',
      filePanelActive: '#e6d9bc',
      filePanelText: '#5b4636'
    }
  },
  ocean: {
    name: '海洋主题',
    colors: {
      primary: '#006064',
      background: '#e0f7fa',
      text: '#00363a',
      border: '#b2ebf2',
      cellBackground: '#ffffff',
      toolbarBackground: '#00838f',
      toolbarText: '#ffffff',
      codeBackground: '#e0f7fa',
      markdownBackground: '#ffffff',
      buttonHover: '#e0f7fa',
      buttonActive: '#b2ebf2',
      selection: '#80deea',
      filePanel: '#ffffff',
      filePanelHover: '#e0f7fa',
      filePanelActive: '#b2ebf2',
      filePanelText: '#00363a'
    }
  }
}

// 获取主题变量
export const getThemeVariables = (themeName) => {
  const theme = themes[themeName]
  if (!theme) return themes.light.colors

  return theme.colors
}

// 应用主题到文档
export const applyTheme = (themeName) => {
  const colors = getThemeVariables(themeName)
  const root = document.documentElement

  // 设置 CSS 变量
  Object.entries(colors).forEach(([key, value]) => {
    root.style.setProperty(`--${key}`, value)
  })

  // 设置 body 背景色和文字颜色
  document.body.style.backgroundColor = colors.background
  document.body.style.color = colors.text

  // 设置 Monaco Editor 主题
  let editorTheme = 'vs'
  switch (themeName) {
    case 'dark':
      editorTheme = 'vs-dark'
      break
    case 'sepia':
      editorTheme = 'vs'
      document.body.style.backgroundColor = colors.background
      break
    case 'ocean':
      editorTheme = 'vs'
      break
    default:
      editorTheme = 'vs'
  }

  // 更新所有 Monaco Editor 实例的主题
  if (window.monaco) {
    const editors = window.monaco.editor.getEditors()
    editors.forEach(editor => {
      editor.updateOptions({ theme: editorTheme })
    })
  }

  return editorTheme
} 