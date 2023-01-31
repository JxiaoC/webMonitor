<template>
  <div id="ssl" v-loading.lock="Loading">
    <el-row class="menu" type="flex" :gutter="20" align="middle">
      <el-col :span="10"
        ><el-button type="primary" class="add" @click="addDialogVisible = true"
          >添加监控</el-button
        >
        <el-button type="success" @click="loadMonitor(false)"
          >刷新</el-button
        >
        <el-button type="warning" @click="refAll"
          >重新查询到期时间</el-button
        >
        </el-col
      >
      
      <el-col :span="14" class="auto-ref"
        ><el-switch
          v-model="autoRef"
          active-text="自动刷新"
          active-color="#13ce66"
          inactive-color="#ff4949"
        >
        </el-switch
      ></el-col>
    </el-row>

    <el-dialog title="添加监控" :visible.sync="addDialogVisible" width="60%">
      <el-form ref="addData" :rules="rules" :model="addData" label-width="80px">
        <el-form-item label="监控名称" prop="name">
          <el-input v-model="addData.name" placeholder="请输入内容"></el-input>
        </el-form-item>
        <el-form-item label="监控host" prop="host">
          <el-input
            v-model="addData.host"
            placeholder="www.baidu.com"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addMonitor">立即创建</el-button>
          <el-button @click="addDialogVisible = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-row class="header">
      <el-col :span="3"><div>监控名称</div></el-col>
      <el-col :span="6"><div>域名</div></el-col>
      <el-col :span="2" class="status"><div>状态</div></el-col>
      <el-col :span="10"><div>剩余天数</div></el-col>
      <el-col :span="3"><div>管理</div></el-col>
    </el-row>
    <sslstatus
      v-for="data in list"
      v-bind:key="data._id"
      :name="data.name"
      :id="data._id"
      :host="data.host"
      :enable="data.enable"
      :rstDay="data.rst_day"
      :LastTime="data.ltime_str"
    ></sslstatus>
  </div>
</template>

<script>
import Qs from "qs";
import axios from "axios";
import sslstatus from "./ssl_status.vue";
export default {
  name: "http",
  props: {
    msg: String,
  },
  data: function () {
    return {
      autoRef: true,
      Loading: true,
      addData: {
        name: "",
        host: "",
      },
      rules: {
        name: [{ required: true, message: "请输入监控名称", trigger: "blur" }],
        host: [
          { required: true, message: "请输入监控host", trigger: "blur" },
        ],
      },
      addDialogVisible: false,
      list: [],
    };
  },
  components: {
    sslstatus,
  },
  created: function () {
    this.loadMonitor(false);
    let self = this;
    clearInterval(window.setI);
    window.setI = setInterval(function () {
      if (self.autoRef && !window.pauseAutoRef) {
        self.loadMonitor(true);
      }
    }, 10000);
  },
  methods: {
    loadMonitor: function (quiet) {
      if (!quiet) this.Loading = true;
      const self = this;
      axios({
        method: "get",
        url: window.host + "/ssl_monitor/list",
      }).then(function (res) {
        self.list = res.data.res.list;
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
#ssl {
  margin: 0 20px;
}

#ssl .menu {
  margin-top: 20px;
  text-align: left;
}

#ssl .header {
  padding-left: 10px;
  height: 40px !important;
  font-weight: 700;
  color: #909399;
  padding-bottom: 5px;
  margin-top: 20px;
  margin-bottom: 5px;
  border-bottom: 1px solid rgb(216, 216, 216);
}

#ssl .auto-ref {
  text-align: right;
}

#ssl .ssl_status:nth-child(2n) {
    background-color: #f9f9f9;
}
</style>