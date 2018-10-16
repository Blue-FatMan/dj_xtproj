// 点击切换图形验证码
$(function(){
   var imgCaptcha = $('.img-captcha');
   imgCaptcha.click(function () {
      imgCaptcha.attr("src",'/account/img_captcha'+"?random="+Math.random());
   });
});

// 点击发送短信验证码
$(function(){
   var smsCaptcha = $('.sms-captcha-btn');
   function send_sms(){
      var telephone = $('input[name="telephone"]').val();
      console.log('coming...');
      $.get({
          'url':'/account/sms_captcha/',
          'telephone':telephone,
          'data':{'telephone':telephone},
          'success':function(result){
              var count = 60;
              smsCaptcha.addClass('disabled');
              smsCaptcha.unbind('click');
              var timer = setInterval(function(){
                  smsCaptcha.text(count);
                  count--;
                  if(count <=0){
                      clearInterval(timer);
                      smsCaptcha.text('send sms_code');
                      smsCaptcha.removeClass('disabled');
                      smsCaptcha.click(send_sms);
                  }
              },1000);
          },
          'fail':function(error){
              console.log(error);
          }
      });
   }
    smsCaptcha.click(send_sms);
});

// 登陆注册功能
$(function () {
    var telephoneInput = $("input[name='telephone']");
    var usernameInput = $("input[name='username']");
    var imgCaptchaInput = $("input[name='img_captcha']");
    var password1Input = $("input[name='password1']");
    var password2Input = $("input[name='password2']");
    var smsCaptchaInput = $("input[name='sms_captcha']");
    var submitBtn = $(".submit-btn");

    submitBtn.click(function (event) {
        // 禁止传统表单发送数据方式，避免点击click就登陆了
        event.preventDefault();

        var telephone = telephoneInput.val();
        var username = usernameInput.val();
        var imgCaptcha = imgCaptchaInput.val();
        var password1 = password1Input.val();
        var password2 = password2Input.val();
        var smsCaptcha = smsCaptchaInput.val();

        if (!telephone||telephone.length != 11){
            alert('手机号码输入不正确！');
            return;
        }
        if (!username){
            alert('用户名不存在或输入不正确！');
            return;
        }
        // 同理其他的字段验证也是一样

        xfzajax.post({
            'url':'/account/register/',
            'data':{
                'telephone':telephone,
                'username':username,
                'img_captcha':imgCaptcha,
                'password1':password1,
                'password2':password2,
                'sms_captcha':smsCaptcha
            },
            'success':function (result) {
                if(result['code'] === 200){
                    window.location = '/'
                }else {
                    // alert(result['message']);
                    var message = result['message'];
                    window.messageBox.showError(message);
                }
            },
            'fail':function (error) {
                console.log(error);
            }
        });
    });
});