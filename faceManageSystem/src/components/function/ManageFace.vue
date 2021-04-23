<template>
  <div>

    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>人脸库管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="faceCard">
      <el-row>
        <el-button @click="getFace"> 获取人脸数据</el-button>
        <el-table :data="faceData" style="width: 100%">
          <el-table-column prop="name" label="姓名" width="300">
          </el-table-column>
          <el-table-column prop="mobile" label="电话" width="300">
          </el-table-column>
          <el-table-column prop="image" width="600" label="图片">
            <template slot-scope="scope">
              <el-image class="view-img" :src="'data:image/jpeg;base64,'+scope.row.image"  style="width: 100px; height: 100px" ></el-image>

            </template>
          </el-table-column>
          <el-table-column label="操作">
          </el-table-column>
        </el-table>
      </el-row>
    </el-card>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        faceData: []
      }
    },
    methods: {
      async getFace() {
        const res = await this.$http.get('/allface');
        console.log(res);
        if (res.data.code == 200) {
          this.faceData = res.data.data;
          this.$message.success("获取图片信息成功")
          console.log(this.faceData);

        }
      }
    },
    created() {
      this.getFace()
    },
  }

</script>

<style scoped>
  .faceCard {
    margin-top: 50px !important;
  }

</style>
