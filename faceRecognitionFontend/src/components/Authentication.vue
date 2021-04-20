<template>
  <div>
    <div class="header">
      <van-nav-bar class="header_nav" title="人脸认证" />
    </div>
    <div class="container">
      <div class="buttonList">
        <van-button type="primary" @click="showAuthModel">人脸登录</van-button>
        <van-popover v-model="showPopover" trigger="click" :actions="actions" @select="onSelect">
          <template #reference>
            <van-button type="primary">人脸注册</van-button>
          </template>
        </van-popover>
        <van-popup @close="destory" v-model="isshowAuthModel" closeable>
          <div class="model">
            <canvas id="canvas" width="300" height="300" style="position:absolute;top:0;left:0;"></canvas>
            <video id="video" preload autoplay loop muted></video>
          </div>
        </van-popup>
        <van-popup v-model="showImageFile">
          <div class="model">
            <van-field v-model="username" label="姓名" placeholder="请输入要添加的用户名" />
            <van-uploader class="imageUploader" v-model="imgList" :after-read="afterRead" :max-count="1" />
            <van-button class="summitBtn" type="primary" @click="summitUser" >提交</van-button>
          </div>
        </van-popup>
        <div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  require('../assets/tracking-min')
  require('../assets/data/face-min')
  import {
    Notify,
  } from 'vant';
  export default {
    data() {
      return {
        isshowAuthModel: false,
        videoEle: null,
        trackerTask: null,
        first: null,
        imageBase64: '',
        showPopover: false,
        actions: [{
          text: '拍照上传'
        }, {
          text: '选择图片上传'
        }],
        isSendImg: false,
        showImageFile: false,
        imgList: [],
        username: ''
      }
    },
    mounted() {

    },
    methods: {
      afterRead(file) {
        console.log(this.imgList[0].content);
      },
      async summitUser() {
        const formData = new FormData()
        formData.append('image', this.imgList[0].content)
        formData.append('name', this.username)
        const config = {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
        const {
          data: res
        } = await this.$http.post('addUser', formData, config)
        this.$toast(res);
        this.showImageFile = false;
        this.imgList = [];
        this.username = '';
      },
      onSelect(action) {
        if (action.text == "拍照上传") {
          this.$router.push('/adduser')
        } else {
          this.showImageFile = true
        }
      },
      async sendImage(image) {
        const formData = new FormData()
        formData.append('image', image)
        const config = {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
        const {
          data: res
        } = await this.$http.post('recongise', formData, config)
        this.$toast.clear() //清除加载框  
        if (res != 'Unknown')
          Notify({
            type: 'primary',
            message: `认证成功，用户为：${res}`
          });
        else
          Notify({
            type: 'warning',
            message: `认证失败，无此人`
          });
      },
      showAuthModel() {
        setTimeout(() => {
          this.openCamera();
        }, 0)
        this.isshowAuthModel = true
      },
      openCamera() {

        var video = document.getElementById('video');
        var canvas = document.getElementById('canvas');
        var context = canvas.getContext('2d')

        var tracker = new tracking.ObjectTracker('face'); // 引入第三方 库
        tracker.setInitialScale(1);
        tracker.setStepSize(2);
        tracker.setEdgesDensity(0.1);

        this.trackerTask = tracking.track('#video', tracker, {
          camera: true
        });
        //-------  指定 canvas 的宽高 ，auto 自动播放
        let constraints = {
          video: {
            width: 300,
            height: 300
          },
          audio: true
        };

        let promise = navigator.mediaDevices.getUserMedia(constraints); // h5 新的API

        promise.then(function (MediaStream) {
          video.srcObject = MediaStream;
          video.play();
        }).catch(function (PermissionDeniedError) {
          console.log(PermissionDeniedError);
        })
        let that = this;
        that.tracker_fun(tracker, video, context, canvas); //open 摄像头，执行tracker_fun( 传入参数 )
      },
      tracker_fun(tracker, video, context, canvas) {
        let that = this;
        let set_clear;
        set_clear = setTimeout(function () { // 每秒 检测人脸 结果
          tracker.on('track', function (event) { // 视频流
            // context.clearRect(0, 0, canvas.width, canvas.height);
            if (!that.first) { // if  --- > else  检测到人脸 success() =>{}
              event.data.forEach(function (rect) {
                if (rect.x) {
                  //检测到人脸 加载框弹出
                  that.$toast.loading({
                    message: '加载中',
                    forbidClick: true,
                  })
                  that.first = rect.x;
                  video.pause(); // success  将暂停 video
                  context.drawImage(video, 0, 0, 300, 300); // 绘制到 canvas
                  that.imageBase64 = canvas.toDataURL('image/png'); //base64 request
                  console.log("发送数据")
                  console.log(that.imageBase64)
                  that.sendImage(that.imageBase64)
                  // video.load();
                  // that.first = null;
                  // that.tracker_fun(tracker,video,context,canvas)
                  return;
                }
              });
            }
          });
          clearTimeout(set_clear)

        }, 5000)
      },
      destory() { //模态框关闭后重新刷新页面
        location.reload();
      },
    },

  };

</script>

<style scoped>
  .header_nav {
    background-color: cadetblue;
    padding: 0;
    margin: 0;
  }

  .buttonList {
    margin: auto;
    width: 50%;
    padding: 50px;
  }

  .model {
    width: 300px;
    height: 300px;
  }

  .imageUploader {
    margin-top: 50px;
    left: 50%;
    transform: translate(-50%);
  }

  .summitBtn {
    display: block;
    margin: 0 auto;
    margin-top: 50px;
  }

</style>
