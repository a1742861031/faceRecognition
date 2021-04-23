<template>
  <div class="login-register">
    <div class="contain">
      <div class="big-box" :class="{active:isLogin}">
        <div class="big-contain" v-show="isLogin">
          <div class="btitle">账户登录</div>
          <el-form :model="loginForm" :rules="loginRule" ref="loginForm" label-width="120px" class="bform"
            label-position="left">
            <el-form-item label="账号" prop="id">
              <el-input v-model="loginForm.id"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="pwd">
              <el-input v-model="loginForm.pwd" type="password"></el-input>

            </el-form-item>
            <el-form-item label="验证码" prop="code">
              <el-input v-model="loginForm.code" class="codeinput"></el-input>
              <img width="85px" height="40px" title="点击刷新" :src="captchaImg" @click="getCode" class="imgcode" />
            </el-form-item>

          </el-form>
          <button class="bbutton" @click="login">登录</button>

        </div>

        <div class="big-contain" v-show="!isLogin">
          <div class="btitle">创建账户</div>

          <el-form :model="regForm" status-icon :rules="regRules" ref="regForm" label-width="120px" class="bform"
            id="form1" label-position="left">
            <el-form-item label="账号" prop="id">
              <el-input type="text" v-model="regForm.id"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="pwd1">
              <el-input type="password" v-model="regForm.pwd1"></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="pwd2">
              <el-input type="password" v-model="regForm.pwd2"></el-input>
            </el-form-item>
            <el-form-item label="验证码" prop="code">
              <el-input v-model="regForm.code" class="codeinput"></el-input>
              <img width="85px" height="40px" title="点击刷新" :src="captchaImg" @click="getCode" class="imgcode" />
            </el-form-item>

            <el-form-item label="手机号" prop="mobile">
              <el-input v-model="regForm.mobile"></el-input>
            </el-form-item>

          </el-form>

          <button class="bbutton" @click="register">注册</button>
        </div>
      </div>
      <div class="small-box" :class="{active:isLogin}">
        <div class="small-contain" v-if="isLogin">
          <div class="stitle">你好，朋友!</div>
          <p class="scontent">人脸识别管理系统</p>
          <button class="sbutton" @click="changeType">注册</button>
        </div>
        <div class="small-contain" v-else>
          <div class="stitle">欢迎回来!</div>
          <p class="scontent">人脸识别管理系统</p>
          <button class="sbutton" @click="changeType">登录</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'login-register',
    data() {

      var validatePass2 = (rule, value, callback) => {
        if (value == '')
          callback(new Error('请确认密码'));
        else if (value !== this.regForm.pwd1) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback()
        }
      };
      var validatemobile = (rule, value, callback) => {
        if (value == '')
          callback(new Error('请确认手机号'));
        else if (!(/^[1][3,4,5,6,7,8,9][0-9]{9}$/.test(value))) {
          callback(new Error('手机号输入有误!'));
        } else {
          callback()
        }
      };
      return {
        isLogin: true,
        emailError: false,
        passwordError: false,
        existed: false,
        captchaImg: '',
        uuid: '',
        regForm: {
          id: '134',
          pwd1: '123',
          pwd2: '123',
          code: '1234',
          mobile: '18323667740',
        },

        loginForm: {
          id: '123',
          pwd: '123',
          code: ''
        },

        loginRule: {
          id: [{
            required: true,
            message: '请输入账号',
            trigger: 'blur'
          }, ],
          pwd: [{
            required: true,
            message: '请输入密码',
            trigger: 'blur'
          }],
          code: [{
            required: true,
            message: '请输入验证码',
            trigger: 'blur'
          }, {
            min: 4,
            max: 4,
            message: '长度为4位',
            trigger: 'blur'
          }]
        },
        regRules: {

          id: [{
            required: true,
            message: '请输入账号',
            trigger: 'blur'
          }, ],
          pwd1: [{
            required: true,
            message: '请输入密码',
            trigger: 'blur'
          }],
          pwd2: [{
            validator: validatePass2,
            trigger: 'blur'
          }],
          code: [{
            required: true,
            message: '请输入验证码',
            trigger: 'blur'
          }, {
            min: 4,
            max: 4,
            message: '长度为4位',
            trigger: 'blur'
          }],
          mobile: [{
            validator: validatemobile,

            trigger: 'blur'
          }],
        }
      }
    },
    methods: {
      changeType() {
        this.isLogin = !this.isLogin
        this.getCode()
        for (let key in this.loginForm)
          this.loginForm[key] = ''
        for (let key in this.regForm)
          this.regForm[key] = ''
      },
      login() {
        this.$refs.loginForm.validate(async (valid) => {
          if (valid) {
              const res = await this.$http.post('sessions',{
                id:this.loginForm.id,
                code:this.loginForm.code,
                pwd:this.loginForm.pwd,
                codeid:this.uuid
              })
              if(res.data.code == 200)
                {
                  //登录成功
                  this.$message.success(res.data.msg);
                   this.$refs.loginForm.resetFields();
                   localStorage.setItem("id",this.loginForm.id)
                   this.$router.push('/home')
                  }
                else{
                  this.$message.error(res.data.msg);
                  this.$refs.loginForm.resetFields();
                }
          } else
            return
        })
      },
      register() {
        this.$refs.regForm.validate(async (valid) => {
          if (valid) {
            const res = await this.$http.post("users", {
              id: this.regForm.id,
              pwd: this.regForm.pwd1,
              code: this.regForm.code,
              mobile: this.regForm.mobile,
              codeid: this.uuid
            })
            console.log(res.data);
            if (res.data.code != 201) {
              this.getCode();
              this.$message.error(res.data.msg);
                this.$refs.regForm.resetFields();
            } else {
              this.$message.success(res.data.msg);
              this.$refs.regForm.resetFields();
            }
          }
        });
      },
      generateUUID() {
        var d = new Date().getTime();
        if (window.performance && typeof window.performance.now === "function") {
          d += performance.now(); //use high-precision timer if available
        }
        var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
          var r = (d + Math.random() * 16) % 16 | 0;
          d = Math.floor(d / 16);
          return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
        return uuid;
      },
      async getCode() {
        this.uuid = this.generateUUID();
        const res = await this.$http.get('image_codes/' + this.uuid, {
          responseType: 'blob'

        });
        this.captchaImg = window.URL.createObjectURL(res.data)
        console.log(this.captchaImg)

      }
    },
    created() {
      this.getCode()
    },
  }

</script>

<style scoped="scoped">
  .login-register {
    width: 100vw;
    height: 100vh;
    box-sizing: border-box;
  }

  .contain {
    width: 60%;
    height: 60%;
    position: relative;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;
    border-radius: 20px;
    box-shadow: 0 0 3px #f0f0f0,
      0 0 6px #f0f0f0;
  }

  .el-form-item__label {
    text-align: left;
  }

  .big-box {
    width: 70%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 30%;
    transform: translateX(0%);
    transition: all 1s;
  }

  .el-input {
    width: 150%;
  }

  .big-contain {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .btitle {
    font-size: 1.5em;
    font-weight: bold;
    color: rgb(57, 167, 176);
  }

  .bform {
    width: 100%;
    height: 40%;
    padding: 2em 0;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
  }

  .bform .errTips {
    display: block;
    width: 50%;
    text-align: left;
    color: red;
    font-size: 0.7em;
    margin-left: 1em;
  }

  .bform input {
    width: 50%;
    height: 30px;
    border: none;
    outline: none;
    border-radius: 10px;
    padding-left: 2em;
    background-color: #f0f0f0;
  }


  .bbutton {
    width: 20%;
    height: 40px;
    border-radius: 24px;
    border: none;
    outline: none;
    background-color: rgb(57, 167, 176);
    color: #fff;
    font-size: 0.9em;
    cursor: pointer;
  }

  .small-box {
    width: 30%;
    height: 100%;
    background: linear-gradient(135deg, rgb(57, 167, 176), rgb(56, 183, 145));
    position: absolute;
    top: 0;
    left: 0;
    transform: translateX(0%);
    transition: all 1s;
    border-top-left-radius: inherit;
    border-bottom-left-radius: inherit;
  }

  .small-contain {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .stitle {
    font-size: 2em;
    font-weight: bold;
    color: #fff;
  }

  .scontent {
    font-size: 1.2em;
    color: #fff;
    text-align: center;
    padding: 2em 4em;
    line-height: 3em;
  }

  .sbutton {
    width: 60%;
    height: 40px;
    border-radius: 24px;
    border: 1px solid #fff;
    outline: none;
    background-color: transparent;
    color: #fff;
    font-size: 0.9em;
    cursor: pointer;
  }

  .big-box.active {
    left: 0;
    transition: all 0.5s;
  }

  .small-box.active {
    left: 100%;
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
    border-top-right-radius: inherit;
    border-bottom-right-radius: inherit;
    transform: translateX(-100%);
    transition: all 1s;
  }

  .codeinput {
    width: 120px;

  }

  .imgcode {
    display: inline-block;
    float: right;
    vertical-align: middle;
  }

  #form1 {
    padding: 3em;
  }

</style>
