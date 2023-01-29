<template>
  <div id="server_real" v-loading.lock="Loading">
    <el-row class="header">
      <el-col :span="3"><div>IP</div></el-col>
      <el-col :span="3"><div>负载</div></el-col>
      <el-col :span="5"><div>CPU</div></el-col>
      <el-col :span="5"><div>内存</div></el-col>
      <el-col :span="3"><div>网络</div></el-col>
      <el-col :span="3"><div>磁盘</div></el-col>
      <el-col :span="2"><div>设置</div></el-col>
    </el-row>
    <server_real_status
      v-for="data in list"
      v-bind:key="data.ip"
      :name="data.name"
      :ip="data.ip"
      :cpuUse="data.cpu.use"
      :cpuSiblings="data.cpu.siblings"
      :load="data.load"
      :memoryTotal="data.memory.total"
      :memoryAvailable="data.memory.available"
      :networkRX="data.network.rx"
      :networkTX="data.network.tx"
      :ioWrite="data.io.write"
      :ioRead="data.io.read"
    ></server_real_status>
  </div>
</template>

<script>
import Qs from "qs";
import axios from "axios";
import server_real_status from "./server_real_status.vue";
export default {
  name: "http",
  props: {
    msg: String,
  },
  data: function () {
    return {
      autoRef: true,
      Loading: true,
      addDialogVisible: false,
      list: [],
    };
  },
  components: {
    server_real_status,
  },
  created: function () {
    this.loadMonitor(false);
    let self = this;
    clearInterval(window.setI);
    window.setI = setInterval(function () {
      if (self.autoRef && !window.pauseAutoRef) {
        self.loadMonitor(true);
      }
    }, 1000);
  },
  methods: {
    loadMonitor: function (quiet) {
      if (!quiet) this.Loading = true;
      const self = this;
      axios({
        method: "get",
        url: window.host + "/server_monitor/real",
      }).then(function (res) {
        self.list = res.data.res;
        self.Loading = false;
      });
    },
    addMonitor: function () {
      let self = this;
      this.$refs["addData"].validate((valid) => {
        if (!valid) {
          return false;
        } else {
          axios({
            method: "post",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            url: window.host + "/ssl_monitor/add",
            data: Qs.stringify(this.addData),
          }).then(function (res) {
            if (res.data.code != 0) {
              self.$notify.error({
                title: "错误",
                message: res.data.msg,
              });
              this.Loading = false;
            } else {
              self.$notify.success({
                title: "成功",
                message: "添加成功",
              });
              self.addDialogVisible = false;
              self.addData.name = "";
              self.addData.host = "";
              self.loadMonitor();
            }
          });
        }
      });
    },
    refAll: function () {
      this.Loading = true;
      let self = this;
      axios({
        method: "post",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        url: window.host + "/ssl_monitor/ref_all",
      }).then(function (res) {
        if (res.data.code != 0) {
          self.$notify.error({
            title: "错误",
            message: res.data.msg,
          });
          self.Loading = false;
        } else {
          self.$notify.success({
            title: "成功",
            message: "全部重新查询完成",
          });
          self.addDialogVisible = false;
          self.loadMonitor();
        }
      });
    },
  },
};
</script>

<style>
#server_real {
  margin: 0 20px;
}

#server_real .menu {
  margin-top: 20px;
  text-align: left;
}

#server_real .header {
  padding-left: 10px;
  height: 40px !important;
  font-weight: 700;
  color: #909399;
  padding-bottom: 5px;
  margin-top: 20px;
  margin-bottom: 5px;
  border-bottom: 1px solid rgb(216, 216, 216);
}

#server_real .auto-ref {
  text-align: right;
}
</style>