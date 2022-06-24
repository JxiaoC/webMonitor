<template>
  <el-row class="tac">
    <el-col :span="3">
      <div id="nav">
        <h4>Web综合监测系统</h4>
        <el-menu default-active="1" class="el-menu-vertical-demo">
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-menu"></i>
              <span>监控类型</span>
            </template>
            <el-menu-item-group>
              <el-menu-item index="1-1" @click="currentTab = 'http'"
                >可用性监控</el-menu-item
              >
              <el-menu-item index="1-2" @click="currentTab = 'server'"
                >服务器监控</el-menu-item
              >
              <el-menu-item index="1-3" @click="currentTab = 'ssl'"
                >SSL证书监控</el-menu-item
              >
              <el-menu-item index="1-4" @click="currentTab = 'host_expire'"
                >域名到期监控</el-menu-item
              >
            </el-menu-item-group>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title">
              <i class="el-icon-setting"></i>
              <span>系统设置</span>
            </template>
            <el-menu-item-group>
              <el-menu-item index="2-1" @click="currentTab = 'setting'"
                >基础设置</el-menu-item
              >
            </el-menu-item-group>
          </el-submenu>
        </el-menu>
      </div>
    </el-col>
    <el-col :span="21">
      <component v-bind:is="currentTabComponent" class="tab"></component>
    </el-col>
  </el-row>
</template>

<script>
import Vue from "vue";
import home from "./home/home.vue";
import http from "./http/http.vue";
import server from "./server/server_box.vue";
import ssl from "./ssl/ssl.vue";
import host_expire from "./host_expire/host.vue";
import setting from "./setting/setting.vue";
Vue.component("tab-http", http);
Vue.component("tab-home", home);
Vue.component("tab-server", server);
Vue.component("tab-ssl", ssl);
Vue.component("tab-host_expire", host_expire);
Vue.component("tab-setting", setting);
export default {
  name: "navigation",
  props: {
    msg: String,
  },
  data: function () {
    return {
      currentTab: "Home",
    };
  },
  computed: {
    currentTabComponent: function () {
      return "tab-" + this.currentTab.toLowerCase();
    },
  },
};
</script>

<style>
h4 {
  text-align: center;
}
</style>