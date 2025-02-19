const { defineConfig } = require('@vue/cli-service')
const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin')

module.exports = defineConfig({
  configureWebpack: {
    plugins: [
      new MonacoWebpackPlugin({
        languages: ['python', 'markdown'],
        features: ['!gotoSymbol']
      })
    ]
  },
  css: {
    loaderOptions: {
      scss: {
        additionalData: `@import "~@/styles/_variables.scss";`
      }
    }
  }
}) 