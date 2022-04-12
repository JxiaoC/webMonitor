<template>
  <div id="server" v-loading.lock="Loading">
    <el-row class="menu" type="flex" :gutter="20" align="middle">
      <el-col :span="10"
        ><el-button type="primary" class="add" @click="addDialogVisible = true"
          >添加监控</el-button
        >
        <el-button type="success" @click="loadMonitor(false)">刷新</el-button>
      </el-col>
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
        <el-form-item label="服务器ip" prop="ip">
          <el-input v-model="addData.ip" placeholder="请输入ip地址"></el-input>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="addData.desc" placeholder="备注"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addMonitor">立即创建</el-button>
          <el-button @click="addDialogVisible = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-row class="header">
      <el-col :span="4"><div>监控名称</div></el-col>
      <el-col :span="2"><div>IP地址</div></el-col>
      <el-col :span="2"><div>CPU</div></el-col>
      <el-col :span="2"><div>内存</div></el-col>
      <el-col :span="5"><div>硬盘</div></el-col>
      <el-col :span="2"><div>本月流出流量</div></el-col>
      <el-col :span="2"><div>上报时间</div></el-col>
      <el-col :span="2"><div>备注</div></el-col>
      <el-col :span="3"><div>管理</div></el-col>
    </el-row>
    <serverstatus
      v-for="data in list"
      v-bind:key="data._id"
      :name="data.name"
      :id="data._id"
      :ip="data.ip"
      :desc="data.desc"
      :cpu_use="data.cpu.use"
      :cpu_siblings="data.cpu.siblings"
      :load="data.load"
      :memory="data.memory"
      :disk="data.disk"
      :network="data.network"
      :atime="data.atime"
      :utime="data.utime"
      :res="data"
    ></serverstatus>
  </div>
</template>

<script>
import Qs from "qs";
import axios from "axios";
import serverstatus from "./server_status.vue";
export default {
  name: "http",
  props: {
    msg: String,
  },
  data: function () {
    return {
      testMonitoring: false,
      autoRef: true,
      Loading: true,
      addData: {
        name: "",
        url: "",
        rate: 5,
        data: "",
        method: "GET",
        header: "",
        allow_http_code: "200",
        find_str_type: "0",
        find_str: "",
        callback_url: "",
      },
      rules: {
        name: [{ required: true, message: "请输入监控名称", trigger: "blur" }],
        ip: [
          { required: true, message: "请输入ip地址", trigger: "blur" },
          {
            pattern: /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/,
            message: "ip格式不对",
            trigger: "blur",
          },
        ],
      },
      addDialogVisible: false,
      list: [],
    };
  },
  components: {
    serverstatus,
  },
  created: function () {
    this.loadMonitor(false);
    let self = this;
    clearInterval(window.setI);
    window.setI = setInterval(function () {
      if (self.autoRef && !window.pauseAutoRef) {
        self.loadMonitor(true);
      }
    }, 60000);
  },
  methods: {
    loadMonitor: function (quiet) {
      if (!quiet) this.Loading = true;
      const self = this;
      axios({
        method: "get",
        url: window.host + "/server_monitor/list",
      }).then(function (res) {
        let list = [];
        for (let f of res.data.res.list) {
          f["allow_http_code"] = f.allow_http_code
            ? f["allow_http_code"].join(",")
            : "200";
          f["find_str_type"] = f.find_str_type
            ? f["find_str_type"].toString()
            : "0";
          if (f.header) {
            f.header = JSON.parse(f.header);
            let header = "";
            for (var item in f.header) {
              header += item + ":" + f.header[item] + "\n";
            }
            f.header = header;
          }
          list.push(f);
        }
        self.list = list;
        self.Loading = false;
      });
    },
    addMonitor: function () {
      let postData = Qs.stringify(this.addData);
      let self = this;
      this.$refs["addData"].validate((valid) => {
        if (!valid) {
          return false;
        } else {
          axios({
            method: "post",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            url: window.host + "/server_monitor/add",
            data: postData,
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
                message: "添加成功",
              });
              self.addDialogVisible = false;
              self.addData.name = "";
              self.addData.ip = "";
              self.addData.desc = "";
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
#server {
  margin: 0 20px;
}

#server .menu {
  margin-top: 20px;
  text-align: left;
}

#server .header {
  padding-left: 10px;
  height: 40px !important;
  font-weight: 700;
  color: #909399;
  padding-bottom: 5px;
  margin-top: 20px;
  margin-bottom: 5px;
  border-bottom: 1px solid rgb(216, 216, 216);
}

#server .auto-ref {
  text-align: right;
}

#server .tip {
  font-size: 12px;
  color: #979797;
}

.el-message-box__message p {
  word-break: break-all;
}
</style>