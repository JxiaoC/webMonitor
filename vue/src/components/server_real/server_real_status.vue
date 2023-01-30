<template>
  <div
    class="server_real_status"
    v-loading="Loading"
  >
  <el-dialog title="添加别名" :visible.sync="showAddAlias" :model="editAlias" width="60%">
      <el-form ref="editAll" label-width="80px">
        <el-form-item label="别名">
          <el-input
          v-model="editAlias.name"
            placeholder="请输入别名"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addAlias">修改</el-button>
          <el-button @click="showAddAlias = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-row align="middle" type="flex" class="name-id">
      <el-col :span="3"
        ><el-tooltip placement="bottom-start" class="name" :content="name">
          <div>{{ name }}</div>
        </el-tooltip>
        <div class="id no-line">{{ ip }}</div></el-col
      >
      <el-col :span="3">
        <div class="load">{{ load.join(' ') }} ({{ cpuSiblings }}H)</div>
      </el-col>
      <el-col :span="5"
        ><div class="cpu">
          <el-progress
            :text-inside="true"
            :stroke-width="24"
            :percentage="cpuUse"
            :status="cpuDayStr"
            :format="formatCPU"
            :style="cpuTextColor"
          ></el-progress></div
      ></el-col>
      <el-col :span="5"
        ><div class="memory">
          <el-progress
            :text-inside="true"
            :stroke-width="24"
            :percentage="memoryRate"
            :status="MemoryStr"
            :format="formatMemory"
            :style="memoryTextColor"
          ></el-progress>
          </div
      ></el-col>
      <el-col :span="3"
        ><div class="network">
          <div v-if="networkTX == -1" style="color:#999;">
            未安装sysstat
          </div>
          <div v-else>
            <div>发送: {{ formatSize(networkTX) }}/S</div>
            <div>接收: {{ formatSize(networkRX) }}/S</div>
          </div>
          </div
      ></el-col>
      <el-col :span="3"
        ><div class="io">
          <div v-if="ioWrite == -1" style="color:#999;">
            未安装sysstat
          </div>
          <div v-else>
            <div>读取: {{ formatSize(ioWrite) }}/S</div>
            <div>写入: {{ formatSize(ioRead) }}/S</div>
          </div>
          </div
      ></el-col>
      <el-col :span="2"
        ><div class="setting">
          <el-button slot="add_alias" type="primary" icon="el-icon-edit" circle @click="showAddAlias=true"></el-button>
          </div
      ></el-col>
    </el-row>
  </div>
</template>
<script>

import Qs from "qs";
import axios from "axios";
import { formatSize } from "../common/data.js";
import Clipboard from "clipboard";
export default {
  name: "server_real_status",
  props: {
    ip: String,
    name: String,
    cpuUse: Number,
    cpuSiblings: Number,
    memoryTotal: Number,
    memoryAvailable: Number,
    networkRX: Number,
    networkTX: Number,
    ioWrite: Number,
    ioRead: Number,
    load: Array,
  },
  data: function () {
    return {
      showAddAlias: false,
      Loading: false,
      editAlias: {
        ip: this.ip,
        name: this.name,
      },
      cpuDayStr:
        this.cpuUse <= 50
          ? "success"
          : this.cpuUse <= 70
          ? "warning"
          : "exception",
      cpuTextColor:
        this.cpuUse > 30 ? "color: #fff;" : "color: #000",
      memoryRate: (this.memoryTotal - this.memoryAvailable) / this.memoryTotal * 100,
      MemoryStr: this.memoryRate <= 50
          ? "success"
          : this.memoryRate <= 85
          ? "warning"
          : "exception",
      memoryTextColor: this.memoryRate > 30 ? "color: #fff;" : "color: #000",
    };
  },
  watch: {},
  methods: {
    copy() {
      let clipboard = new Clipboard('.host-copy');
      clipboard.on("success", () => {
        this.$notify.success({
          title: '成功',
          message: '复制成功',
        });
        clipboard.destroy();
      });
      clipboard.on("error", () => {
        this.$notify.error({
          title: '失败',
          message: '该浏览器不支持自动复制',
        });
        clipboard.destroy();
      });
    },
    formatCPU() {
      this.cpuStr = this.cpuUse <= 50
          ? "success"
          : this.cpuUse <= 70
          ? "warning"
          : "exception";
      this.cpuTextColor = this.cpuUse > 30 ? "color: #fff;" : "color: #000";
      return this.cpuUse + "%";
    },
    formatMemory() {
      this.memoryRate = (this.memoryTotal - this.memoryAvailable) / this.memoryTotal * 100;
      this.MemoryStr = this.memoryRate <= 50
          ? "success"
          : this.memoryRate <= 85
          ? "warning"
          : "exception";
      this.memoryTextColor = this.memoryRate > 40 ? "color: #fff;" : "color: #000";
      return this.memoryRate.toFixed(1) + '% (' + formatSize((this.memoryTotal - this.memoryAvailable)) + "/" + formatSize(this.memoryTotal) + ')';
    },
    formatSize(d){
      return formatSize(d);
    },
    addAlias(){
      let self = this;
      axios({
            method: "post",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            url: window.host + "/server_monitor/add_alias",
            data: Qs.stringify(this.editAlias),
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
                message: "修改成功",
              });
              self.showAddAlias = false;
            }
          });
    },
  },
};
</script>

<style>
#server_real .load{
  font-size: 14px;
}

#server_real .network, #server_real .io{
  font-size: 12px;
}

#server_real .el-row {
  height: 50px;
}

#server_real .id {
  font-size: 12px;
  text-align: left;
  color: #bbb;
}

#server_real .name {
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

#server_real .url {
  color: rgb(83, 186, 255);
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 0 7%;
}

#server_real .name-id {
  padding-left: 10px;
}

#server_real .server_real_status {
  border-bottom: 1px solid rgb(247 247 247);
}

#server_real .el-row {
  text-align: center;
}

#server_real .el-progress-bar__innerText {
  color: inherit;
  margin: 0 10px;
}

#server_real .el-progress-bar__outer{
  margin: 0 10px;
}

#server_real .el-progress-bar__inner{
  transition: width .2s ease;
}
</style>