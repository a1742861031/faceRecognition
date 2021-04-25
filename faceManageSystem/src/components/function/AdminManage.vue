<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>管理员管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="faceCard">
      <el-row>
        <el-table :data="adminList" style="width:100%">
          <el-table-column label="管理员id" prop="id">

          </el-table-column>
          <el-table-column label="管理员姓名" prop="name">

          </el-table-column>
          <el-table-column label="电话" prop="mobile">

          </el-table-column>
          <el-table-column label="状态" prop="state">
            <template slot-scope="scope">
              <el-tag type="success" v-show="scope.row.state==1" effect="dark">
                正在使用
              </el-tag>
              <el-tag v-show="scope.row.state==0" type="warning" effect="dark">
                已停用
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-tooltip class="item" effect="dark" content="编辑" placement="bottom-start">
                <el-button type="primary" icon="el-icon-edit" @click="editAdminModel(scope.row.id)"></el-button>
              </el-tooltip>
              <el-dialog title="修改管理员信息" :visible.sync="editAdminVisible" width="30%">
                <el-form :model="adminInfo" status-icon ref="adminInfo" label-width="100px">
                  <el-form-item label="id" prop="id">
                    <el-input disabled type="text" v-model="adminInfo.id" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="姓名" prop="name">
                    <el-input type="text" v-model="adminInfo.name" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="电话" prop="id">
                    <el-input type="text" v-model="adminInfo.mobile" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="状态" prop="state">
                    <el-switch v-model="adminInfo.state" active-color="#13ce66" inactive-color="#ff4949">
                    </el-switch>
                  </el-form-item>
                  <el-form-item label="是否是超管" prop="isSuperAdmin">
                    <el-switch v-model="adminInfo.isSuperAdmin" :active-value=1 :inactive-value=0 active-color="#13ce66"
                      inactive-color="#ff4949">
                    </el-switch>
                  </el-form-item>
                  <el-form-item label="密码" prop="pwd">
                    <el-input type="password" v-model="adminInfo.pwd" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="确认密码" prop="pwd1">
                    <el-input type="password" v-model="pwd1" autocomplete="off"></el-input>
                  </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                  <el-button @click="editAdminVisible = false">取 消</el-button>
                  <el-button type="primary" @click="uploadEdit()">确 定</el-button>
                </span>
              </el-dialog>
              <el-tooltip class="item" effect="dark" content="删除该管理员" placement="bottom-start">
                <el-button type="danger" icon="el-icon-delete" @click="openDeleteBox(scope.row.id)">
                </el-button>
              </el-tooltip>
            </template>
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
        queryadmin: '',
        adminList: [],
        editAdminVisible: false,
        pwd1: '',
        adminInfo: {
          id: '',
          name: '',
          mobile: '',
          state: false,
          isSuperAdmin: 0,
          pwd: '',
        }

      }
    },
    methods: {
      async getAdmins() { //获取管理员列表
        const res = await this.$http.get("/admins")
        console.log(res);
        if (res.data.code == 200) {
          this.$message.success("获取管理员列表成功");
          this.adminList = res.data.data
        }
        console.log(this.adminList);
      },
      async editAdminModel(id) {
        this.pwd1 = ''
        this.adminInfo.pwd = ''
        const res = await this.$http.get("admin", {
          params: {
            id: id
          }
        })
        console.log(res.data.data);
        if (res.data.code == 200) {
          this.editAdminVisible = true,
            this.adminInfo.id = res.data.data.id;
          this.adminInfo.name = res.data.data.name;
          this.adminInfo.mobile = res.data.data.mobile;
          this.adminInfo.state = res.data.data.state;
          this.adminInfo.isSuperAdmin = res.data.data.isSuperAdmin;
          this.$message.success("获取管理员信息成功")
          console.log(this.adminInfo);
        }
      },
      async uploadEdit() {
        if (this.pwd1 != this.adminInfo.pwd)
          this.$message.warning("输入的两次密码不一致")
        const res = await this.$http.post('admin', this.adminInfo)
        if (res.data.code == 201) {
          this.$message.success("修改成功！")
          this.editAdminVisible = false
          this.getAdmins()
        }
      },
      async deleteAdmin(id) {
       const res = await this.$http.delete("admin", {
          params: {
            id: id
          }
        })
        if (res.data.code == 201) {
          this.$message.success("删除成功");
          this.getAdmins();
        } else
          this.$message.error("删除失败")

      },
      openDeleteBox(id) {
        this.$confirm('此操作将永久删除该人脸用户, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.deleteAdmin(id)
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
    },
    created() {
      this.getAdmins();
    },
  }

</script>

<style scoped>
  .search {
    margin-top: 10px;
  }

  .faceCard {
    margin-top: 30px !important;
  }

</style>
