<template>
  <div id="app">
      <navigation></navigation>
  </div>
</template>
<script>
import navigation from './components/navigation.vue'
export default {
  name: 'App',
  components: {
    navigation,
  }
}
</script>

<style>
h3{
  text-align: center;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
.el-submenu .el-menu-item{
  min-width: auto;
}
</style>
