<template>
  <div id="http" v-loading.lock="Loading">
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
        <el-form-item label="请求类型">
          <el-select v-model="addData.method" placeholder="GET/POST">
            <el-option label="GET" value="GET"></el-option>
            <el-option label="POST" value="POST"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item
          :style="addData.method == 'POST' ? '' : 'display:none;'"
          label="Post Data"
          prop="data"
        >
          <el-input
            v-model="addData.data"
            placeholder="key=%E7%8B%97&type=json"
          ></el-input>
        </el-form-item>

        <el-form-item label="URL" prop="url">
          <el-input
            v-model="addData.url"
            placeholder="https://www.baidu.com"
          ></el-input>
        </el-form-item>

        <el-form-item label="状态码" prop="allow_http_code">
          <el-input v-model="addData.allow_http_code" placeholder=""></el-input>
          <div class="tip">
            多个http状态码使用半角逗号隔开, 当返回http code包含设置值时,
            则认为正常
          </div>
        </el-form-item>

        <el-form-item label="Header" prop="header">
          <el-input
            type="textarea"
            v-model="addData.header"
            :rows="5"
            placeholder="Referer: http://localhost:8856/
Accept-Language: zh-CN,zh;q=0.9
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
          ></el-input>
        </el-form-item>

        <el-form-item label="匹配文本">
          <el-input
            v-model="addData.find_str"
            placeholder="匹配请求返回的文本内容"
          ></el-input>
        </el-form-item>

        <el-form-item
          label="匹配模式"
          :style="addData.find_str != '' ? '' : 'display:none;'"
        >
          <el-select v-model="addData.find_str_type" placeholder="白名单">
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
                v-model="addData.callback_url"
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
            v-model="addData.rate"
            :min="1"
            :max="60"
            label="单位为分钟"
          ></el-input-number>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addMonitor">立即创建</el-button>
          <el-button
            type="success"
            @click="testMonitor"
            :loading="testMonitoring"
            >模拟</el-button
          >
          <el-button @click="addDialogVisible = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-row class="header">
      <el-col :span="3"><div>监控名称</div></el-col>
      <el-col :span="6"><div>地址</div></el-col>
      <el-col :span="2" class="status"><div>状态</div></el-col>
      <el-col :span="8"><div>24小时可用性</div></el-col>
      <el-col :span="2"><div>频率</div></el-col>
      <el-col :span="3"><div>管理</div></el-col>
    </el-row>
    <httpstatus
      v-for="data in list"
      v-bind:key="data._id"
      :name="data.name"
      :id="data._id"
      :url="data.url"
      :enable="data.enable"
      :status24="data.status24"
      :status24_list="data.status24_list"
      :rate="data.rate"
      :res="data"
      :LastTime="data.ltime_str"
    ></httpstatus>
  </div>
</template>

<script>
import Qs from "qs";
import axios from "axios";
import httpstatus from "./http_status.vue";
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
      addDialogVisible: false,
      list: [],
    };
  },
  components: {
    httpstatus,
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
        url: window.host + "/http_monitor/list",
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
      let temp_header = this.addData.header;
      let temp_data = this.addData.data;
      this.addData.header = window.btoa(this.addData.header);
      this.addData.data = window.btoa(this.addData.data);
      let postData = Qs.stringify(this.addData);
      this.addData.header = temp_header;
      this.addData.data = temp_data;
      let self = this;
      this.$refs["addData"].validate((valid) => {
        if (!valid) {
          return false;
        } else {
          axios({
            method: "post",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            url: window.host + "/http_monitor/add",
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
              self.addData.url = "";
              self.addData.header = "";
              self.addData.data = "";
              self.addData.find_str = "";
              self.addData.find_str_type = "0";
              self.addData.allow_http_code = "200";
              self.addData.callback_url = "";
              self.loadMonitor();
            }
          });
        }
      });
    },
    testMonitor: function () {
      let temp_header = this.addData.header;
      let temp_data = this.addData.data;
      this.addData.header = window.btoa(this.addData.header);
      this.addData.data = window.btoa(this.addData.data);
      let postData = Qs.stringify(this.addData);
      this.addData.header = temp_header;
      this.addData.data = temp_data;
      let self = this;
      this.$refs["addData"].validate((valid) => {
        if (!valid) {
          return false;
        } else {
          self.testMonitoring = true;
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
            } else {
              self.$notify.success({
                title: "成功",
                message: res.data.msg,
              });
            }
            self.testMonitoring = false;
          });
        }
      });
    },
    callbackTest: function (status) {
      if (!this.addData.callback_url) {
        this.$alert("请输入回调url");
        return;
      }
      let postData = "status=" + status + "&callback_url=" + encodeURIComponent(this.addData.callback_url);
      let self = this;
      self.$msgbox({
        dangerouslyUseHTMLString: true,
        title: "模拟请求",
        message:
          "即将发起模拟请求, 具体请求参数如下:<br/> Url: " +
          self.addData.callback_url +
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
  },
};
</script>

<style>
#http {
  margin: 0 20px;
}

#http .menu {
  margin-top: 20px;
  text-align: left;
}

#http .header {
  padding-left: 10px;
  height: 40px !important;
  font-weight: 700;
  color: #909399;
  padding-bottom: 5px;
  margin-top: 20px;
  margin-bottom: 5px;
  border-bottom: 1px solid rgb(216, 216, 216);
}

#http .auto-ref {
  text-align: right;
}

#http .tip {
  font-size: 12px;
  color: #979797;
}

.el-message-box__message p {
  word-break: break-all;
}
</style>