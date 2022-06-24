<template>
  <div
    class="server_box_status"
    :style="is_remove ? 'display: none' : ''"
    v-loading="Loading"
  >
    <el-dialog title="编辑监控" :visible.sync="editDialogVisible" width="60%">
      <el-form ref="editAll" :rules="rules" :model="res" label-width="80px">
        <el-form-item label="监控名称" prop="name">
          <el-input
            v-model="res.name"
            placeholder="请输入内容"
          ></el-input>
        </el-form-item>
         <el-form-item label="服务器ip" prop="ip">
          <el-input v-model="res.ip" placeholder="请输入ip地址" disabled></el-input>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="res.desc" placeholder="备注"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="editMonitor">修改</el-button>
          <el-button @click="editDialogVisible = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
    <div class="item">
      <div class="title">
        <el-tooltip placement="bottom" class="url" :content="'点击复制IP: ' + ip">
          <div class="url-copy" :data-clipboard-text="ip" @click="copy">
            {{ name }}
          </div>
        </el-tooltip>
      </div>
      <div class="cpu">
        <el-row>
          <el-col :span="3">CPU</el-col>
          <el-col :span="21">
            <el-progress
                :text-inside="true"
                :stroke-width="18"
                :percentage="cpu_use"
                :status="CpuStatusStr"
                :format="formatCPU"
              ></el-progress>
          </el-col>
        </el-row>
      </div>
      <div class="memory">
        <el-row>
          <el-col :span="3">内存</el-col>
          <el-col :span="21">
            <el-progress
                :text-inside="true"
                :stroke-width="18"
                :percentage="parseFloat(memory['value'] / memory['total_value'] * 100)"
                :status="MemoryStatusStr"
                :format="format"
              ></el-progress>
          </el-col>
        </el-row>
      </div>
      <div class="disks">
        <el-row>
          <el-col :span="3">硬盘</el-col>
          <el-col :span="21">
            <div v-for="data in disk"
              v-bind:key="data.name">
              <el-progress
                    :text-inside="true"
                    :stroke-width="16"
                    :percentage="data.value / data.total_value * 100"
                    :status=' data.value / data.total_value * 100 >= 85
                  ? "exception"
                  : data.value / data.total_value * 100 >= 70
                  ? "warning"
                  : "success"'
                  :format="formatDisk(data)"
              ></el-progress>
          </div>
          </el-col>
        </el-row>
      </div>
      <div class="network">
        <el-row>
          <el-col :span="3">流量</el-col>
          <el-col :span="21">
            <el-progress
                :text-inside="true"
                :stroke-width="18"
                :percentage="100"
                :format="()=>{return this.formatSize(this.network);}"
              ></el-progress>
          </el-col>
        </el-row>
      </div>
      <div class="time">
        <el-row>
          <el-col :span="3">上报</el-col>
          <el-col :span="21">
            <el-progress
                :text-inside="true"
                :stroke-width="18"
                :percentage="100"
                :format="()=>{return this.formatDate(this.utime);}"
              ></el-progress>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>
<script>
import Clipboard from "clipboard";
import axios from "axios";
import Qs from "qs";
import { formatDate, formatSize } from "../common/data.js";
export default {
  name: "server_box_status",
  props: {
    id: String,
    name: String,
    ip: String,
    desc: String,
    cpu_use: Number,
    cpu_siblings: Number,
    load: Object,
    memory: Object,
    network: Number,
    disk: Array,
    atime: Number,
    utime: Number,
    res: Object,
  },
  filters: {
    formatDate(time) {
      time = time * 1000;
      let date = new Date(time);
      return formatDate(date, "yyyy-MM-dd hh:mm");
    },
    formatSize(size) {
      return formatSize(size);
    },
  },
  data: function () {
    return {
      Loading: false,
      is_remove: false,
      currentName: this.name,
      currentIP: this.ip,
      currentDesc: this.desc,
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
      editDialogVisible: false,
      memoryRate: parseInt(this.memory['value'] / this.memory['total_value'] * 100),
      MemoryStatusStr:
        this.memoryRate >= 90
          ? "exception"
          : this.memoryRate >= 60
          ? "warning"
          : "success",
      CpuStatusStr:
        this.cpu_use >= 90
          ? "exception"
          : this.cpu_use >= 60
          ? "warning"
          : "success",
    };
  },
  watch: {
    editDialogVisible: function () {
      window.pauseAutoRef = this.editDialogVisible;
    },
  },
  methods: {
    editMonitor: function () {
      let temp_header = this.res.header;
      let temp_data = this.res.data;
      this.res.header = window.btoa(this.res.header);
      this.res.data = window.btoa(this.res.data);
      this.res.id = this.id;
      let postData = Qs.stringify(this.res);
      this.res.header = temp_header;
      this.res.data = temp_data;
      let self = this;
      this.$refs["editAll"].validate((valid) => {
        if (!valid) {
          return false;
        } else {
          axios({
            method: "post",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            url: window.host + "/server_monitor/edit",
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
              self.editDialogVisible = false;
            }
          });
        }
      });
    },
    copy() {
      let clipboard = new Clipboard(".url-copy");
      clipboard.on("success", () => {
        this.$notify.success({
          title: "成功",
          message: "复制成功",
        });
        clipboard.destroy();
      });
      clipboard.on("error", () => {
        this.$notify.error({
          title: "失败",
          message: "该浏览器不支持自动复制",
        });
        clipboard.destroy();
      });
    },
    format() {
      this.currentEnable = this.enable;
      this.memoryRate = parseInt(this.memory['value'] / this.memory['total_value'] * 100);
      this.MemoryStatusStr =
        this.memoryRate >= 90
          ? "exception"
          : this.memoryRate >= 60
          ? "warning"
          : "success";
      return formatSize(this.memory['value']) + '/' + formatSize(this.memory['total_value']) + '(' + this.memoryRate + "%)";
    },
    formatDate(time) {
      time = time * 1000;
      let date = new Date(time);
      return formatDate(date, "yyyy-MM-dd hh:mm");
    },
    formatSize(size) {
      return formatSize(size);
    },
    formatCPU() {
      this.CpuStatusStr =
        this.cpu_use >= 90
          ? "exception"
          : this.cpu_use >= 60
          ? "warning"
          : "success";
      return this.cpu_use + "% " + this.cpu_siblings + "Core (" + this.load['load_1'] + ", " + this.load['load_5'] + ", " + this.load['load_15'] + ")";
    },
    formatDisk(data) {
      return function(){
        return  data['name'] + ' ' + formatSize(data['value'], 0) + '/' + formatSize(data['total_value'], 0) + '(' + parseInt(data['value'] / data['total_value'] * 100) + "%)";
      }
    },
    
    remove: function () {
      this.dialogVisible = false;
      this.is_remove = true;
      axios({
        method: "post",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        url: window.host + "/server_monitor/remove",
        data: Qs.stringify({
          id: this.id,
        }),
      }).then(function () {});
    },
    switchEnable: function (val) {
      var self = this;
      this.Loading = true;
      axios({
        method: "post",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        url: window.host + "/server_monitor/edit",
        data: Qs.stringify({
          id: this.id,
          key: "enable",
          value: val,
        }),
      }).then(function () {
        self.Loading = false;
        self.$notify({
          title: "成功",
          message: "状态修改成功",
          type: "success",
        });
      });
    },
  },
};
</script>

<style>
.server_box_status{
    display: inline-block;
    vertical-align: top;
}
.server_box_status .item{
    font-size: 14px;
    border: 1px solid rgb(233, 233, 233);
    border-radius: 5px;
    margin: 10px;
    padding: 10px;
    width: 300px;
    background-color: rgb(252, 252, 252);
}

.server_box_status .item .el-progress-bar__outer{
  background-color: #d6d6d6;
}

.server_box_status .item .cpu .el-col-3{
  margin-top: 1px;
}

.server_box_status .item .memory .el-col-3{
  margin-top: -1px;
}

.server_box_status .item .disks .el-col-3{
  margin-top: -2px;
}

.server_box_status .item>div{
  margin: 0 5px 5px 5px;
}

.server_box_status .item .title{
  text-align: center;
  margin-bottom: 10px;
}

.server_box_status .item .disks .el-col-21>div{
  margin: 2px 0;
}
</style>