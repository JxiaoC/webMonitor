const path = require("path");

module.exports = {
  // webpack配置 - 简单配置方式
  configureWebpack: {
    resolve: {
      alias: {
        // 别名
        vue$: "vue/dist/vue.esm.js", //加上这一句
        "@api": path.resolve(__dirname, "./src/api"),
        "@utils": path.resolve(__dirname, "./src/utils")
      }
    }
  },
  devServer: {
    port: 8856,   // 端口号
    disableHostCheck: true,
  },
  assetsDir: './static',
  chainWebpack: config => {
    config
      .plugin('html')
      .tap(args => {
        args[0].title= 'Web综合监测系统'
        return args
      })
  },
}