<template>
  <div id="setting">
    <el-form
      v-loading="Loading"
      label-position="top"
      ref="data"
      :rules="rules"
      :model="data"
      label-width="80px"
    >
      <el-form-item label="Server酱Token" prop="server_jiang_token">
        <el-row>
          <el-col :span="22"
            ><el-input
              v-model="data.server_jiang_token"
              placeholder="配置Server酱Token即可接受报警信息"
            ></el-input
          ></el-col>
          <el-col :span="2"
            ><el-button type="success" @click="sendTest"
              >测试</el-button
            ></el-col
          >
        </el-row>
      </el-form-item>
      <el-form-item label="HTTP可用性报警阈值(次)">
        <el-input-number
          v-model="data.max_error_num"
          :min="1"
          :max="15"
          label="连续错误N次后触发报警"
        ></el-input-number>
      </el-form-item>
      <el-form-item label="报警沉默时间(分钟)">
        <el-input-number
          v-model="data.silence_time"
          :min="0"
          :max="3600"
          label="连续错误N次后触发报警"
        ></el-input-number>
      </el-form-item>
      <el-form-item label="SSL证书报警天数">
        <el-input-number
          v-model="data.ssl_min_day"
          :min="0"
          :max="30"
          label="<=此天数将会触发报警"
        ></el-input-number>
      </el-form-item>
      <el-form-item label="域名过期报警天数">
        <el-input-number
          v-model="data.host_expire_min_day"
          :min="0"
          :max="365"
          label="<=此天数将会触发报警"
        ></el-input-number>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="save">保存</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from "axios";
import Qs from "qs";
export default {
  name: "setting",
  data: function () {
    return {
      Loading: true,
      data: {
        server_jiang_token: "",
        max_error_num: 3,
        silence_time: 60,
        ssl_min_day: 10,
        host_expire_min_day: 30,
      },
      rules: {
        name: [
          { required: false, message: "请输入Server酱Token", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    save: function () {
      this.$refs["data"].validate((valid) => {
        if (!valid) {
          return false;
        } else {
          let self = this;
          this.Loading = true;
          axios({
            method: "post",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            url: window.host + "/setting/save",
            data: Qs.stringify(this.data),
          }).then(function (res) {
            if (res.data.code != 0) {
              self.$notify.error({
                title: "错误",
                message: res.data.msg,
              });
              self.Loading = false;
            } else {
              self.Loading = false;
              self.$notify({
                title: "成功",
                message: "状态修改成功",
                type: "success",
              });
            }
          });
        }
      });
    },
    load: function () {
      let self = this;
      this.Loading = true;
      axios({
        method: "get",
        url: window.host + "/setting/info",
      }).then(function (res) {
        self.data = res.data.res;
        self.Loading = false;
      });
    },
    sendTest: function () {
      let self = this;
      this.Loading = true;
      axios({
        method: "post",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        url: window.host + "/setting/send",
        data: Qs.stringify(this.data),
      }).then(function (res) {
        self.Loading = false;
        if (res.data.code == 0) {
          self.$notify({
            title: "成功",
            message: "发送成功",
            type: "success",
          });
        } else {
          self.$notify({
            title: "失败",
            message: res.data.msg,
            type: "error",
          });
        }
      });
    },
  },
  created: function () {
    this.load();
  },
};
</script>

<style>
#setting {
  margin: 20px 20px 0 20px;
  text-align: left;
}
</style>