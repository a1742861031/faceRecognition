<template>
  <div>
    <div class="header">
      <van-nav-bar class="header_nav" title="拍照增加用户" />
    </div>
    <div class="camera_outer">

      <video id="videoCamera" :width="videoWidth" :height="videoHeight" autoplay></video>
      <canvas style="display: none" id="canvasCamera" :width="videoWidth" :height="videoHeight"></canvas>

      <van-button type="primary" @click="getCompetence()">打开摄像头</van-button>
      <van-button type="danger" @click="stopNavigator()">关闭摄像头</van-button>
      <van-button type="info" @click="setImage()">拍照</van-button>
      <van-popup v-model="showModel" closeable close-icon="close" :style="{ height: '47%' }" @close="destory">
        <div v-if="imgSrc" class="img_bg_camera">
          <img :src="imgSrc" alt="" class="tx_img" />

        </div>
        <van-cell-group>
          <van-field v-model="username" label="姓名" placeholder="请输入用户名" />
        </van-cell-group>
        <van-button class="sendBtn" type="primary" @click="summitUser" size="small" v-if="notsending">上传照片</van-button>
        <van-button class="sendBtn" loading type="primary" v-if="!notsending" loading-type="spinner" />

      </van-popup>

    </div>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        videoWidth: 300,
        videoHeight: 300,
        imgSrc: "",
        thisCancas: null,
        thisContext: null,
        thisVideo: null,
        showModel: false,
        notsending: true,
        username: '',

      };
    },
    mounted() {
      this.getCompetence();
    },
    methods: {

      async summitUser() {
        if (this.username == "") {
          this.$toast("请输入姓名")
          return
        }
        if (this.imgSrc == "") {
          this.$toast("请拍照")
          return
        }
        this.notsending = false
        const formData = new FormData()
        formData.append('image', this.imgSrc)
        formData.append('name', this.username)
        const config = {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
        const {
          data: res
        } = await this.$http.post('addUser', formData, config)
        this.notsending = true;
        this.showModel = false;
        this.$toast(res)
      },
      // 调用权限（打开摄像头功能）
      getCompetence() {
        var _this = this;
        this.thisCancas = document.getElementById("canvasCamera");
        this.thisContext = this.thisCancas.getContext("2d");
        this.thisVideo = document.getElementById("videoCamera");
        // 旧版本浏览器可能根本不支持mediaDevices，我们首先设置一个空对象
        if (navigator.mediaDevices === undefined) {
          navigator.mediaDevices = {};
        }
        // 一些浏览器实现了部分mediaDevices，我们不能只分配一个对象
        // 使用getUserMedia，因为它会覆盖现有的属性。
        // 这里，如果缺少getUserMedia属性，就添加它。
        if (navigator.mediaDevices.getUserMedia === undefined) {
          navigator.mediaDevices.getUserMedia = function (constraints) {
            // 首先获取现存的getUserMedia(如果存在)
            var getUserMedia =
              navigator.webkitGetUserMedia ||
              navigator.mozGetUserMedia ||
              navigator.getUserMedia;
            // 有些浏览器不支持，会返回错误信息
            // 保持接口一致
            if (!getUserMedia) {
              return Promise.reject(
                new Error("getUserMedia is not implemented in this browser")
              );
            }
            // 否则，使用Promise将调用包装到旧的navigator.getUserMedia
            return new Promise(function (resolve, reject) {
              getUserMedia.call(navigator, constraints, resolve, reject);
            });
          };
        }
        var constraints = {
          audio: false,
          video: {
            width: this.videoWidth,
            height: this.videoHeight,
            transform: "scaleX(-1)",
          },
        };
        navigator.mediaDevices
          .getUserMedia(constraints)
          .then(function (stream) {
            // 旧的浏览器可能没有srcObject
            if ("srcObject" in _this.thisVideo) {
              _this.thisVideo.srcObject = stream;
            } else {
              // 避免在新的浏览器中使用它，因为它正在被弃用。
              _this.thisVideo.src = window.URL.createObjectURL(stream);
            }
            _this.thisVideo.onloadedmetadata = function (e) {
              _this.thisVideo.play();
            };
          })
          .catch((err) => {
            console.log(err);
          });
      },
      //  绘制图片（拍照功能）
      setImage() {
        this.showModel = true
        var _this = this;
        // 点击，canvas画图

        _this.thisContext.drawImage(
          _this.thisVideo,
          0,
          0,
          _this.videoWidth,
          _this.videoHeight
        );
        // 获取图片base64链接
        var image = this.thisCancas.toDataURL("image/png");
        _this.imgSrc = image; //base64 编码
        this.$emit("refreshDataList", this.imgSrc);
      },
      // base64转文件
      dataURLtoFile(dataurl, filename) {
        var arr = dataurl.split(",");
        var mime = arr[0].match(/:(.*?);/)[1];
        var bstr = atob(arr[1]);
        var n = bstr.length;
        var u8arr = new Uint8Array(n);
        while (n--) {
          u8arr[n] = bstr.charCodeAt(n);
        }
        return new File([u8arr], filename, {
          type: mime
        });
      },
      destory() {

        this.notsending = true;
        this.username = "";
        this.imgSrc = ""
      },
      // 关闭摄像头
      stopNavigator() {
        this.thisVideo.srcObject.getTracks()[0].stop();
      },

    },

  };

</script>
<style scoped>
  .sendBtn {
    display: block;
    margin: 0 auto
  }

  .header_nav {
    background-color: cadetblue;
    padding: 0;
    margin: 0;
  }
.camera_outer{
   margin-left: 30px;
    margin-top: 30px;
}
</style>
