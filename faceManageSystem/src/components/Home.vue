<template>
  <el-container class="home-container">
    <!-- 头部区域 -->
    <el-header>
      <div>
        <img src="../assets/logo.png" height="80px" />
        <el-dropdown>
          <span class="el-dropdown-link">
            用户{{ profile.id }}已登录<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item @click.native="jumpToHome()">个人信息</el-dropdown-item>
            <el-dropdown-item @click.native="logout()">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </el-header>
    <!-- 页面主题 -->

    <el-container>
      <!-- 侧边栏 -->

      <el-aside>

        <!-- <el-menu background-color="#e1e6e5" text-color="#409ef"  :router="true"
          :default-active="activePath"> -->
        <el-menu background-color="#e1e6e5" :router="true">
          <el-menu-item index="admin">
            <i class="el-icon-user"></i>
            <span slot="title">管理员管理</span>
          </el-menu-item>
          <el-menu-item index="allface">
            <i class="el-icon-picture-outline"></i>
            <span slot="title">人脸库管理</span>
          </el-menu-item>


        </el-menu>
        <!-- </el-menu> -->
      </el-aside>
      <!-- 右侧主体内容 -->
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>


<script>
  export default {
    data() {
      return {
        profile: {
          id: '',
          mobile: '',
          issuper: '',
        }
      };
    },
    created() {
      this.getProfile()
    },
    methods: {

      jumpToHome() {
        this.$router.push("profile")
      },
      async logout() {
        const res = await this.$http.delete("sessions")
        console.log(res);
        if (res.data.code != 200)
          this.$message.error("登出失败")
        else {
          this.$message.success(res.data.msg);
          this.$router.push("/")
        }
      },
      async getProfile() {
        const res = await this.$http.get("profile");
        this.profile.id = res.data.data.id;
        this.profile.mobile = res.data.data.mobile
        if (res.data.data.isSuperAdmin = 0)
          this.profile.issuper = '否'
        else
          this.profile.issuper = '是'
        console.log(this.profile);
      }
    }
  }

</script>

<style scoped>
  .title {
    color: transparent;
    -webkit-text-stroke: 1px black;
    letter-spacing: 0.04em;
    color: #5595a5;
    font-size: 35px;
    display: inline;
    margin-top: 100px;

  }

  .home-container {
    height: 100%;
  }

  .el-header {
    height: 80px !important;
    padding: 0;
  }

  .el-aside {
    background-color: #e1e6e5;

  }

  .el-main {
    background-color: #eaedf1;
  }

  .logo {
    height: 50px;
    margin-top: 10px;
  }

  .el-dropdown {
    float: right;
    position: relative;
    margin-top: 33px;
    margin-right: 100px;
  }

  .el-dropdown-link {
    cursor: pointer;
    color: #409eff;

  }

  .el-icon-arrow-down {
    font-size: 12px;
  }

</style>
