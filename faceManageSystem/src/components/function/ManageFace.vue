<template>
  <div>

    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>人脸库管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="search">
      <el-col :span="6">
        <el-input placeholder="通过姓名搜索图片" v-model="queryFace">
          <el-button slot="append" icon="el-icon-search" @click="getFace(queryFace)"></el-button>
        </el-input>
      </el-col>
    </el-row>
    <el-card class="faceCard">
      <el-row>
        <el-table :data="faceData.slice((currentPage-1)*pageSize,currentPage*pageSize)" style="width: 100%">
          <el-table-column prop="id" label="人脸id" width="250">
          </el-table-column>
          <el-table-column prop="name" label="姓名" width="250">
          </el-table-column>

          <el-table-column prop="image" width="400" label="图片">
            <template slot-scope="scope">
              <el-image class="view-img" :src="'data:image/jpeg;base64,'+scope.row.image"
                style="width: 100px; height: 100px"></el-image>
            </template>
          </el-table-column>
          <el-table-column prop="state" width="300" label="状态">
            <template slot-scope="scope">
              {{scope.row.state==1?'该人像正在使用':'该人像已停用'}}
            </template>
          </el-table-column>

          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-tooltip class="item" effect="dark" content="编辑" placement="bottom-start">
                <el-button type="primary" icon="el-icon-edit" @click="openFaceModel(scope.row.id)"></el-button>
              </el-tooltip>
              <el-dialog title="修改人脸相关信息" :visible.sync="faceDialogVisible" width="30%">

                <el-form :model="oneFace" status-icon ref="oneFace" label-width="100px">
                  <el-form-item label="姓名" prop="name">
                    <el-input type="text" v-model="oneFace.name" autocomplete="off"></el-input>
                  </el-form-item>

                  <el-form-item label="人脸状态" prop="state">
                    <el-switch v-model="oneFace.state" active-color="#13ce66" inactive-color="#ff4949">
                    </el-switch>
                  </el-form-item>
                  <el-form-item label="人脸头像" prop="imageSrc">
                    <el-upload class="avatar-uploader" action="" :show-file-list="false" :auto-upload="false"
                      :on-change="changeFile">
                      <el-image class="view-img" :src="oneFace.imageSrc" style="width: 100px; height: 100px"></el-image>
                    </el-upload>

                  </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                  <el-button @click="faceDialogVisible = false">取 消</el-button>
                  <el-button type="primary" @click="uploadOneFace">确 定</el-button>
                </span>
              </el-dialog>

              <el-tooltip class="item" effect="dark" content="删除该用户" placement="bottom-start">
                <el-button type="danger" icon="el-icon-delete" @click="openDeleteBox(scope.row.id)">
                </el-button>
              </el-tooltip>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination background layout="prev, pager, next" :total="pages" :page-size="pageSize"
          @current-change="handelCurrentChange" :current_page.sync="currentPage">
        </el-pagination>
      </el-row>
    </el-card>

  </div>
</template>

<script>
  export default {
    data() {
      return {
        faceData: [],
        faceDialogVisible: false,
        pages: 0,
        pageSize: 4,
        currentPage: 1,
        queryFace: '',
        oneFace: {
          id: '',
          name: '',
          imageSrc: '',
          state: ''
        },
    

      }
    },

    methods: {
      async getFace() {
        let res;
        if (this.queryFace == '')
          res = await this.$http.get('/allfaces')
        else
          res = await this.$http.get('/allfaces', {
            params: {
              name: this.queryFace
            }
          })
        console.log(res);
        if (res.data.code == 200) {
          this.faceData = res.data.data;
          this.$message.success("获取图片信息成功")
          console.log(this.faceData);
          this.pages = this.faceData.length
        }
      },
      async deleteFace(id) {
        const res = await this.$http.delete('/face', {
          params: {
            id: id
          }
        })
        if (res.data.code == 200)
          this.$message.success("删除成功")
        else
          this.$message.error("删除失败")

      },


      handelCurrentChange(currentPage) {
        console.log(currentPage);
        this.currentPage = currentPage
      },
      openDeleteBox(id) {
        this.$confirm('此操作将永久删除该人脸用户, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.deleteFace(id)
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },

      changeFile(file) {
        var This = this;
        var reader = new FileReader();
        reader.readAsDataURL(file.raw);
        reader.onload = function () {
          // this.result // 这个就是base64编码了
          console.log(this.result);
          This.oneFace.imageSrc = this.result
        }
      },
      async uploadOneFace() {
        const res = await this.$http.post("/face", {
          id: this.oneFace.id,
          name: this.oneFace.name,
          state: this.oneFace.state,
          image: this.oneFace.imageSrc,

        })
        if (res.data.code != 201) {
          this.$message.error("修改信息失败")
          this.faceDialogVisible = false
        } else {
          this.$message.success(res.data.msg)
          this.faceDialogVisible = false
          this.getFace()
        }
      },
      // 获取单张人脸信息
      async getOneFace(id) {
        const res = await this.$http.get('/face', {
          params: {
            id: id,
          },

        })
        console.log(res);
        if (res.data.code != 200)
          this.$message.error("获取人脸信息失败")
        else {
          this.$message.success("获取人脸信息成功")
          this.oneFace.id = res.data.data.id;
          this.oneFace.imageSrc = 'data:image/jpeg;base64,' + res.data.data.image;
          this.oneFace.state = res.data.data.state;
          this.oneFace.name = res.data.data.name;
        }
      },
      openFaceModel(id) {
        this.getOneFace(id)
        this.faceDialogVisible = true

      }
    },
    created() {
      this.getFace()
    },
  }

</script>

<style scoped>
  .faceCard {
    margin-top: 30px !important;
  }

  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }

  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }

  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }

  .search {
    margin-top: 10px;
  }

</style>
