<template>
  <div id="host_expire" v-loading.lock="Loading">
    <el-row class="menu" type="flex" :gutter="20" align="middle">
      <el-col :span="10"
        ><el-button type="primary" class="add" @click="addDialogVisible = true"
          >添加监控</el-button
        >
        <el-button type="success" @click="loadMonitor(false)"
          >刷新</el-button
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
    <span class="tip">只有到期时间小于等于设置的报警时间时, 才会在每天自动刷新过期时间</span>
    <el-dialog title="添加监控" :visible.sync="addDialogVisible" width="60%">
      <el-form ref="addData" :rules="rules" :model="addData" label-width="80px">
        <el-form-item label="监控名称" prop="name">
          <el-input v-model="addData.name" placeholder="请输入内容"></el-input>
        </el-form-item>
        <el-form-item label="监控域名" prop="host">
          <el-input
            v-model="addData.host"
            placeholder="baidu.com"
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
    <hoststatus
      v-for="data in list"
      v-bind:key="data._id"
      :name="data.name"
      :id="data._id"
      :host="data.host"
      :enable="data.enable"
      :rstDay="data.rst_day"
      :LastTime="data.ltime_str"
    ></hoststatus>
  </div>
</template>

<script>
import Qs from "qs";
import axios from "axios";
import hoststatus from "./host_status.vue";
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
          { required: true, message: "请输入监控域名", trigger: "blur" },
        ],
      },
      addDialogVisible: false,
      list: [],
    };
  },
  components: {
    hoststatus,
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
        url: window.host + "/expire_monitor/list",
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
            url: window.host + "/expire_monitor/add",
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
              self.addData.name = "";
              self.addData.host = "";
              self.addDialogVisible = false;
              self.loadMonitor();
            }
          });
        }
      });
    },
  },
};
</script>

<style>
#host_expire {
  margin: 0 20px;
}

#host_expire .menu {
  margin-top: 20px;
  text-align: left;
}

#host_expire .header {
  padding-left: 10px;
  height: 40px !important;
  font-weight: 700;
  color: #909399;
  padding-bottom: 5px;
  margin-top: 20px;
  margin-bottom: 5px;
  border-bottom: 1px solid rgb(216, 216, 216);
}

#host_expire .auto-ref {
  text-align: right;
}

#host_expire .tip{
  font-size: 12px;
  color: rgb(160, 160, 160);
}

#host_expire .host_status:nth-child(2n) {
    background-color: #f9f9f9;
}
</style>