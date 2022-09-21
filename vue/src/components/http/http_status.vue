<template>
  <div
    class="http_status"
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
        <el-form-item label="请求类型">
          <el-select v-model="res.method" placeholder="GET/POST">
            <el-option label="GET" value="GET"></el-option>
            <el-option label="POST" value="POST"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item
          :style="res.method == 'POST' ? '' : 'display:none;'"
          label="Post Data"
          prop="data"
        >
          <el-input
            v-model="res.data"
            placeholder="key=%E7%8B%97&type=json"
          ></el-input>
        </el-form-item>

        <el-form-item label="URL" prop="url">
          <el-input
            v-model="res.url"
            placeholder="https://www.baidu.com"
            disabled
          ></el-input>
        </el-form-item>

        <el-form-item label="状态码" prop="allow_http_code">
          <el-input v-model="res.allow_http_code" placeholder=""></el-input>
          <div class="tip">
            多个http状态码使用半角逗号隔开, 当返回http code包含设置值时,
            则认为正常
          </div>
        </el-form-item>

        <el-form-item label="Header" prop="header">
          <el-input
            type="textarea"
            v-model="res.header"
            :rows="5"
            placeholder="Referer: http://localhost:8856/
Accept-Language: zh-CN,zh;q=0.9
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
          ></el-input>
        </el-form-item>

        <el-form-item label="匹配文本">
          <el-input
            v-model="res.find_str"
            placeholder="匹配请求返回的文本内容"
          ></el-input>
        </el-form-item>

        <el-form-item
          label="匹配模式"
          :style="res.find_str != '' ? '' : 'display:none;'"
        >
          <el-select v-model="res.find_str_type" placeholder="白名单">
            <el-option label="白名单(必须包含匹配文本)" value="0"></el-option>
            <el-option label="黑名单(不能包含匹配文本)" value="1"></el-option>
          </el-select>
          <div class="tip">
            白名单模式下, 如果返回文本不包含设置的匹配文本, 则失败;
            黑名单模式下, 返回文本包含设置的匹配文本, 则失败
          </div>
        </el-form-item>

        <el-form-item label="回调地址">
          <el-row>
            <el-col :span="14"
              ><el-input
                v-model="res.callback_url"
                placeholder="回调地址"
              ></el-input
            ></el-col>
            <el-col :span="5" style="padding: 0 0 0 1%"
              ><el-button
                style="width: 100%"
                type="success"
                @click="callbackTest('success')"
                >模拟可用性恢复</el-button
              ></el-col
            >
            <el-col :span="5" style="padding: 0 0 0 1%"
              ><el-button
                style="width: 100%"
                type="danger"
                @click="callbackTest('fail')"
                >模拟可用性报错</el-button
              ></el-col
            >
          </el-row>
          <div class="tip" style="line-height: 20px; margin-top: 10px">
            将会往指定URL POST数据,具体POST内容为status(报错状态: fail(报错),
            success(恢复))<br />
            回调地址需要返回"ok"字符串以表示正确收到回调, 否则将会间隔1分钟,
            连续请求直到超过3次或者正常返回"ok"字符串为止
          </div>
        </el-form-item>

        <el-form-item label="监控频率" prop="rate">
          <el-input-number
            v-model="res.rate"
            :min="1"
            :max="60"
            label="单位为分钟"
          ></el-input-number>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="editMonitor">修改</el-button>
          <el-button
            type="success"
            @click="testMonitor"
            :loading="testMonitoring"
            >模拟</el-button
          >
          <el-button @click="editDialogVisible = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-row align="middle" type="flex" class="name-id">
      <el-col :span="3"
        ><el-tooltip placement="bottom-start" class="name" :content="name">
          <div>{{ name }}</div>
        </el-tooltip>
        <div class="id no-line">{{ id }}</div></el-col
      >
      <el-col :span="6">
        <el-tooltip placement="bottom" class="url" content="点击复制">
          <div class="url-copy" :data-clipboard-text="url" @click="copy">
            {{ url }}
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
      <el-col :span="8"
        ><div class="24h">
          <div class="box_24h">
            <el-tooltip
              placement="bottom-end"
              :class="
                !item.normal ? 'warning status-24h-msg' : 'status-24h-msg'
              "
              v-for="item in status24_list"
              v-bind:key="item.id"
              :style="
                !item.normal
                  ? 'background-color: rgb(255, 0, 0)'
                  : item.delay > 5000
                  ? 'background-color: rgb(255 193 140)'
                  : item.delay > 3000
                  ? 'background-color: rgb(255 177 0)'
                  : item.delay > 1000
                  ? 'background-color: rgb(255 235 0)'
                  : item.delay > 500
                  ? 'background-color: rgb(228 255 0)'
                  : item.delay > 300
                  ? 'background-color: rgb(157 255 0)'
                  : 'background-color: rgb(16 206 102)'
              "
            >
              <div slot="content">
                [{{ item.atime | formatDate }}]
                <br />
                http code: {{ item.http_code }}
                <br />
                delay: {{ item.delay }}ms
                <br />
                normal: {{ item.normal }}
                <br />
                24h usability: {{ status24 }}%
                <br />
                {{ item.err_data ? "err_data: " + item.err_data : "" }}
              </div>
              <div class="progress">0</div>
            </el-tooltip>
          </div>
        </div></el-col
      >
      <el-col :span="2"
        ><div class="rate">{{ rate }}分钟</div></el-col
      >
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
import { formatDate } from "../common/data.js";
export default {
  name: "http_status",
  props: {
    id: String,
    name: String,
    url: String,
    LastTime: String,
    enable: {
      type: Boolean,
      default: false,
    },
    status24: {
      type: Number,
      default: 99,
    },
    status24_list: {
      type: Array,
      default: null,
    },
    rate: {
      type: Number,
      default: 15,
    },
    res: Object,
  },
  filters: {
    formatDate(time) {
      time = time * 1000;
      let date = new Date(time);
      return formatDate(date, "yyyy-MM-dd hh:mm");
    },
  },
  data: function () {
    return {
      Loading: false,
      is_remove: false,
      currentEnable: this.enable,
      current24Status: this.status24,
      current24StatusStr:
        this.status24 >= 85
          ? "success"
          : this.status24 >= 25
          ? "warning"
          : "exception",
      current24StatusTextColor:
        this.status24 >= 30 ? "color: #fff;" : "color: #000",
      rules: {
        name: [{ required: true, message: "请输入监控名称", trigger: "blur" }],
        url: [
          { required: true, message: "请输入监控url", trigger: "blur" },
          {
            pattern: /^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+/,
            message: "url格式不对",
            trigger: "blur",
          },
        ],
        rate: [
          { required: true, message: "间隔时间不能为空", trigger: "blur" },
          { pattern: /^\d+$/, message: "间隔必须为数字" },
        ],
        allow_http_code: [
          { required: true, message: "请输入正常的http code", trigger: "blur" },
          {
            pattern: /^\d*,{0,1}\d*$/,
            message: "http状态码格式不正确",
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
      var temp_res = {...this.res};
      console.log(temp_res);
      temp_res['status24_list'] = '';
      let postData = Qs.stringify(temp_res);
      console.log(postData);
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
            url: window.host + "/http_monitor/edit_all",
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
    testMonitor: function () {
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
            url: window.host + "/http_monitor/test",
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
                message: res.data.msg,
              });
            }
          });
        }
      });
    },
    callbackTest: function (status) {
      if (!this.res.callback_url) {
        this.$alert("请输入回调url");
        return;
      }
      let postData = "status=" + status + "&callback_url=" + encodeURIComponent(this.res.callback_url);
      let self = this;
      self.$msgbox({
        dangerouslyUseHTMLString: true,
        title: "模拟请求",
        message:
          "即将发起模拟请求, 具体请求参数如下:<br/> Url: " +
          self.res.callback_url +
          "<br/>Method: POST<br/>Data: status=" +
          status,
        beforeClose: (action, instance, done) => {
          instance.confirmButtonLoading = true;
          instance.confirmButtonText = "执行中...";
          axios({
            method: "post",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
            url: window.host + "/http_monitor/callback_test",
            data: postData,
          }).then(function (res) {
            done();
            instance.confirmButtonLoading = false;
            if (res.data.code != 0) {
              self.$notify.error({
                title: "模拟发生了错误",
                message: res.data.msg,
              });
            } else {
              self.$notify.success({
                title: "成功",
                message: "模拟成功",
              });
            }
          });
        },
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
        url: window.host + "/http_monitor/remove",
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
        url: window.host + "/http_monitor/edit",
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
#http .el-row {
  height: 50px;
}

#http .id {
  font-size: 12px;
  color: #bbb;
  text-align: left;
}

#http .name {
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

#http .url {
  color: rgb(83, 186, 255);
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 0 7%;
}

#http .name-id {
  padding-left: 10px;
}

#http .http_status {
  border-bottom: 1px solid rgb(247 247 247);
}

#http .el-row {
  text-align: center;
}

#http .el-progress-bar__innerText {
  color: inherit;
}

#http .status-24h-msg {
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

#http .status-24h-msg:hover {
  height: 30px;
}

#http .box_24h {
  white-space: nowrap;
  overflow: hidden;
  text-align: left;
}
</style>