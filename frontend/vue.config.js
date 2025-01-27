const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin')

module.exports = {
  configureWebpack: {
    plugins: [
      new MonacoWebpackPlugin({
        languages: ['python', 'markdown'],
        features: ['!gotoSymbol']
      })
    ]
  }
} 