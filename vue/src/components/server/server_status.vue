<template>
  <div
    class="server_status"
    :style="is_remove ? 'display: none' : ''"
    v-loading="Loading"
  >
    <el-dialog title="编辑监控" :visible.sync="editDialogVisible" width="60%">
      <el-form ref="editAll" :rules="rules" :model="res" label-width="80px">
        <el-form-item label="监控名称" prop="name">
          <el-input
            v-model="res.name"
            placeholder="请输入内容"
            disabled
          ></el-input>
        </el-form-item>
         <el-form-item label="服务器ip" prop="ip">
          <el-input v-model="res.ip" placeholder="请输入ip地址"></el-input>
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

    <el-row align="middle" type="flex" class="name-id">
      <el-col :span="4"
        ><el-tooltip placement="bottom-start" class="name" :content="name">
          <div>{{ name }}</div>
        </el-tooltip>
        <div class="id no-line">{{ id }}</div></el-col
      >
      <el-col :span="2">
        <el-tooltip placement="bottom" class="url" content="点击复制">
          <div class="url-copy" :data-clipboard-text="ip" @click="copy">
            {{ ip }}
          </div>
        </el-tooltip>
      </el-col>
      <el-col :span="2"
        >
          <div>{{ cpu_use }}% ({{ cpu_siblings }}H)</div>
          <div>{{ load['load_1'] }}, {{ load['load_5'] }}, {{ load['load_15'] }}</div>
        </el-col>
      <el-col :span="2"
        >
          <div>{{ memory['value'] | formatSize }} / {{memory['total_value'] | formatSize}}</div>
          <div>({{parseFloat(memory['value'] / memory['total_value'] * 100).toFixed(2)}}%)</div>
        </el-col>
      <el-col :span="5"
        >
          <div v-for="data in disk"
      v-bind:key="data.name">
      {{ data.value | formatSize }}/{{ data.total_value | formatSize }}({{parseFloat(data.value / data.total_value * 100).toFixed(2)}}%) - {{ data.name }}
      </div>
        </el-col>
      <el-col :span="2"
        >
          <div>{{ network | formatSize }}</div>
        </el-col>
      <el-col :span="2"
        >
          <div class="utime">{{ utime | formatDate}}</div>
        </el-col>
      <el-col :span="2"
        ><el-tooltip placement="bottom-start" class="desc" :content="desc">
          <div>{{ desc }}</div>
        </el-tooltip>
        </el-col>
      <el-col :span="3"
        ><div class="setting">
          <el-button
            slot="reference"
            type="primary"
            icon="el-icon-edit"
            circle
            style="margin-right: 10px"
            @click="editDialogVisible = true"
          ></el-button>

          <el-popconfirm
            confirm-button-type="danger"
            confirm-button-text="好的"
            cancel-button-text="不用了"
            icon="el-icon-delete"
            icon-color="red"
            title="确定删除吗?"
            @confirm="remove"
          >
            <el-button
              slot="reference"
              type="danger"
              icon="el-icon-delete"
              circle
            ></el-button>
          </el-popconfirm></div
      ></el-col>
    </el-row>
  </div>
</template>
<script>
import Clipboard from "clipboard";
import axios from "axios";
import Qs from "qs";
import { formatDate, formatSize } from "../common/data.js";
export default {
  name: "server_status",
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
      this.current24Status = this.status24;
      this.current24StatusStr =
        this.status24 >= 85
          ? "success"
          : this.status24 >= 25
          ? "warning"
          : "exception";
      this.current24StatusTextColor =
        this.status24 >= 30 ? "color: #fff;" : "color: #000";
      return this.current24Status + "% (最后更新:" + this.LastTime + ")";
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
#server .el-row {
  height: 50px;
}

#server .id {
  font-size: 12px;
  color: #bbb;
  text-align: left;
}

#server .name {
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

#server .url {
  color: rgb(83, 186, 255);
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 0 7%;
}

#server .name-id {
  padding-left: 10px;
}

#server .http_status {
  border-bottom: 1px solid rgb(247 247 247);
}

#server .el-row {
  text-align: center;
}

#server .el-progress-bar__innerText {
  color: inherit;
}

#server .status-24h-msg {
  display: inline-block;
  width: 5px;
  background-color: #bbb;
  margin: 0 1px;
  color: hsla(0, 0%, 100%, 0);
  cursor: default;
  vertical-align: middle;
  transition: height 0.1s;
  height: 22px;
  border-radius: 5px;
}

#server .status-24h-msg:hover {
  height: 30px;
}

#server .box_24h {
  white-space: nowrap;
  overflow: auto;
  text-align: left;
}
</style>