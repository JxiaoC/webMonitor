<template>
  <div
    class="host_status"
    :style="isRemove ? 'display: none' : ''"
    v-loading="Loading"
  >
    <el-row align="middle" type="flex" class="name-id">
      <el-col :span="3"
        ><el-tooltip placement="bottom-start" class="name" :content="name">
          <div>{{ name }}</div>
        </el-tooltip>
        <div class="id no-line">{{ id }}</div></el-col
      >
      <el-col :span="6">
        <el-tooltip placement="bottom" class="url" content="点击复制">
          <div class="host-copy" :data-clipboard-text="host" @click="copy">
            {{ host }}
          </div>
        </el-tooltip>
      </el-col>
      <el-col :span="2"
        ><div class="status">
          <el-switch
            v-model="currentEnable"
            @click.native="switchEnable(currentEnable)"
            active-color="#13ce66"
            inactive-color="#ff4949"
          >
          </el-switch></div
      ></el-col>
      <el-col :span="10"
        ><div class="24h">
          <el-progress
            :text-inside="true"
            :stroke-width="24"
            :percentage="currentRstDayRate"
            :status="currentRstDayStr"
            :format="format"
            :style="currentRstDayTextColor"
          ></el-progress></div
      ></el-col>
      <el-col :span="3"
        ><div class="setting">
          <el-tooltip placement="bottom" content="刷新剩余天数">
            <el-button
              type="primary"
              icon="el-icon-refresh"
              circle
              @click="ref"
              style="margin-right: 10px"
            ></el-button>
          </el-tooltip>
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
export default {
  name: "host_status",
  props: {
    id: String,
    name: String,
    host: String,
    LastTime: String,
    enable: {
      type: Boolean,
      default: false,
    },
    rstDay: {
      type: Number,
      default: 98,
    },
  },
  data: function () {
    return {
      Loading: false,
      isRemove: false,
      currentEnable: this.enable,
      currentRstDay: this.rstDay,
      currentRstDayRate:
        (this.rstDay / 365) * 100 > 100 ? 100 : (this.rstDay / 365) * 100,
      currentRstDayStr:
        this.rstDay >= 30
          ? "success"
          : this.rstDay >= 10
          ? "warning"
          : "exception",
      currentRstDayTextColor:
        (this.rstDay / 365) * 100 >= 40 ? "color: #fff;" : "color: #000",
    };
  },
  watch: {},
  methods: {
    copy() {
      let clipboard = new Clipboard(".host-copy");
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
      this.currentRstDay = this.rstDay;
      this.currentRstDayRate =
        (this.rstDay / 365) * 100 > 100 ? 100 : (this.rstDay / 365) * 100;
      this.currentRstDayStr =
        this.rstDay >= 30
          ? "success"
          : this.rstDay >= 10
          ? "warning"
          : "exception";
      this.currentRstDayTextColor =
        (this.rstDay / 365) * 100 >= 40 ? "color: #fff;" : "color: #000";
      return this.rstDay + "天 (最后更新:" + this.LastTime + ")";
    },
    remove: function () {
      this.dialogVisible = false;
      this.isRemove = true;
      axios({
        method: "post",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        url: window.host + "/expire_monitor/remove",
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
        url: window.host + "/expire_monitor/edit",
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
    ref: function () {
      this.Loading = true;
      let self = this;
      axios({
        method: "post",
        data: Qs.stringify({
          id: this.id,
        }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        url: window.host + "/expire_monitor/ref",
      }).then(function (res) {
        if (res.data.code != 0) {
          self.$notify.error({
            title: "错误",
            message: res.data.msg,
          });
        } else {
          self.$notify.success({
            title: "成功",
            message: self.name + " 刷新成功",
          });
          self.rstDay = res.data.res;
          self.addDialogVisible = false;
        }
        self.Loading = false;
      });
    },
  },
};
</script>

<style>
#host_expire .el-row {
  height: 50px;
}

#host_expire .id {
  font-size: 12px;
  text-align: left;
  color: #bbb;
}

#host_expire .name {
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

#host_expire .url {
  color: rgb(83, 186, 255);
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 0 7%;
}

#host_expire .name-id {
  padding-left: 10px;
}

#host_expire .host_status {
  border-bottom: 1px solid rgb(247 247 247);
}

#host_expire .el-row {
  text-align: center;
}

#host_expire .el-progress-bar__innerText {
  color: inherit;
}
</style>