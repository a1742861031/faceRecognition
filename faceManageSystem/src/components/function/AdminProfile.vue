<template>
  <div>
    <!-- 面包屑导航 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>个人中心</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="main">
      <el-col :span="7" class="form1">
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>个人信息</span>
          </div>
          <div class="avatar">
            <el-avatar shape="square" :size="100" fit="contain"
              src="https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=1377979781,1331210068&fm=26&gp=0.jpg">
            </el-avatar>
          </div>
          <ul class="list-group">
            <li class="list-group-item el-icon-user-solid">
              用户名称：
              <div class="pull-right">{{profile.id}}</div>
            </li>
            <br />
            <li class="list-group-item el-icon-phone">
              电话号码：
              <div class="pull-right">{{profile.mobile}}</div>
            </li>
            <br />
            <li class="list-group-item el-icon-user">
              姓名：
              <div class="pull-right">{{profile.name}}</div>
            </li>
            <br />
            <li class="list-group-item el-icon-info">是否为超级管理员：<div class="pull-right">{{profile.issuper}}</div>
            </li>
          </ul>
        </el-card>
      </el-col>
      <el-col :span="9" class="form2">
        <el-card>
          <div slot="header" class="clearfix">
            <span>刷脸信息统计</span>
          </div>
          <div id="myChart" :style="{width: '100%', height: '400px'}"></div>
        </el-card>
      </el-col>
    </el-row>

  </div>

</template>

<script>
  export default {
    data() {
      return {
        profile: {
          id: '',
          mobile: '',
          issuper: '',
          name: '',
        },
        records: {
          time: [],
          num: [],
        },
        time:['3-24','3-25'],
        num:[2,7]
      }
    },

    methods: {
      async getProfile() {
        const res = await this.$http.get("profile");
        this.profile.id = res.data.data.id;
        this.profile.mobile = res.data.data.mobile
        this.profile.name = res.data.data.name
        if (res.data.data.isSuperAdmin == 0)
          this.profile.issuper = '否'
        else
          this.profile.issuper = '是'
        console.log(this.profile);
      },
      async getRecords() {
        const {
          data: res
        } = await this.$http.get("/getAll");
        let data = res.data;
        for (let i = 0; i < data.length; i++) {
          this.records.time.push(data[i].time)
          this.records.num.push(data[i].num)
        }
        this.drawLine()

      },
      drawLine() {
        // 基于准备好的dom，初始化echarts实例
        //this.getRecords()
        let xdata = this.records.time;
        let ydata = this.records.num;
        let myChart = this.$echarts.init(document.getElementById('myChart'))
        myChart.clear();
        window.onresize = myChart.resize // 加这行代码，没错！
        // 绘制图表
        myChart.setOption({

          tooltip: {},
          xAxis: {
            data: xdata
          },
          yAxis: {},
          series: [{
            name: '刷脸次数',
            type: 'line',
            data: ydata
          }]
        });
      }

    },
    mounted() {
      this.getRecords()
    },
    created() {
      this.getProfile();
    },
  }

</script>

<style scoped>
  .main {
    margin-top: 30px;
  }

  .form1 {
    margin-right: 60px;
  }

  .clearfix {
    display: table;
    content: "";
  }

  .list-group {
    padding-left: 0;
    list-style: none;
  }

  .list-group-item {
    width: 100%;
    border-bottom: 1px solid #e7eaec;
    margin-bottom: 10px;
    padding: 11px 0;
    font-size: 15px;
  }

  .avatar {
    text-align: center;
    border-bottom: 1px solid #e7eaec;
  }

  .pull-right {
    float: right !important;
  }

  .form2 {
    margin-left: 200px;

  }

</style>
