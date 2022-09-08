layui.use(function () {
    var $ = layui.$
        , layer = layui.layer
        , notify = layui.notify
        , form = layui.form;

    //猫头鹰
    $('.password_owl').focus(function () {
        // 密码框获得焦点，追加样式.password
        $('#owl').addClass('password');
    }).blur(function () {
        // 密码框失去焦点，移除样式.password
        $('#owl').removeClass('password');
    });//猫头鹰
    //切换登录注册
    $('.re_register').on('click', function () {
        $('#register').show();
        $('#login').hide();
        $('#retrieve').hide();
        $('#login_form')[0].reset();
        $('#retrieve_form')[0].reset();
        form.render();
    });
    //注册窗口密码验证
    form.verify({
        email: function (value) {
            var email_regex = /(^$)|^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/
            if (!email_regex.test(value)) {
                return notify.warning("邮箱不正确！", 'center');
            }
        },
        check_password: function (value) {
            if ($('#register_form input[name="password"]').val() !== value) {
                return notify.warning("两次输入的密码不一致！", 'center');
            }
        },
        check_password2: function (value) {
            if ($('#retrieve_form input[name="password"]').val() !== value) {
                return notify.warning("两次输入的密码不一致！", 'center');
            }
        },
        password: function (value) {
            var reg = /^[a-zA-Z0-9\~\!\@\#\$\%\^]{6,16}$/;
            if (!reg.test(value)) {
                return notify.warning("请输入6到16位密码，可包含字符为（a~z,A~Z,0~9,~,!,@,#,$,%,^）", 'center');
            }
        }
    });

    $('.re_login').on('click', function () {
        $('#login').show();
        $('#register').hide();
        $('#retrieve').hide();
        $('#register_form')[0].reset();
        $('#retrieve_form')[0].reset();
        form.render();
    });
    $('.re_retrieve').on('click', function () {
        $('#retrieve').show();
        $('#register').hide();
        $('#login').hide();
        $('#register_form')[0].reset();
        $('#login_form')[0].reset();
        form.render();
    });

    //发送验证码
    function bindcaptcha_btn() {
        $('#register_form .captcha_btn').on('click', function () {
            var email = $('#register_form input[name="email"]').val();
            var subject = 'Secret账户注册';
            var message = '您好，您正在注册Secret树洞账号。'
            $.ajax({
                url: '/user/captcha',
                method: 'POST',
                data: {
                    'email': email,
                    'subject': subject,
                    'message': message
                },
                success: function (res) {
                    if (res['status'] === 200) {
                        notify.success("发送成功！", 'center', 1000);
                        $('#register_form .captcha_btn').off('click');
                        var countdown = 60;
                        var timer = setInterval(function () {
                            countdown--;
                            if (countdown > 0) {
                                $('#register_form .captcha_btn').css('width', '130px')
                                $('#register_form .captcha_btn').text(countdown + 's 后重新发送');
                            } else {
                                $('#register_form .captcha_btn').css('width', '90px')
                                $('#register_form .captcha_btn').text('发送验证码');
                                bindcaptcha_btn();
                                clearInterval(timer);
                            }
                        }, 1000);

                    } else {
                        notify.error(res['msg'], 'center', 1000);
                    }
                }
            })
        });
    }

    function bindcaptcha_btn2() {
        $('#retrieve_form .captcha_btn').on('click', function () {
            var email = $('#retrieve_form input[name="email"]').val();
            var subject = 'Secret找回密码';
            var message = '您好，您正在找回Secret树洞账号。'
            $.ajax({
                url: '/user/captcha',
                method: 'POST',
                data: {
                    'email': email,
                    'subject': subject,
                    'message': message
                },
                success: function (res) {
                    if (res['status'] === 200) {
                        notify.success("发送成功！", 'center', 1000);
                        $('#retrieve_form .captcha_btn').off('click');
                        var countdown = 60;
                        var timer = setInterval(function () {
                            countdown--;
                            if (countdown > 0) {
                                $('#retrieve_form .captcha_btn').css('width', '130px')
                                $('#retrieve_form .captcha_btn').text(countdown + 's 后重新发送');
                            } else {
                                $('#retrieve_form .captcha_btn').css('width', '90px')
                                $('#retrieve_form .captcha_btn').text('发送验证码');
                                bindcaptcha_btn2();
                                clearInterval(timer);
                            }
                        }, 1000);

                    } else {
                        notify.error(res['msg'], 'center', 1000);
                    }
                }
            })
        });
    }

    $(function () {
        bindcaptcha_btn();
        bindcaptcha_btn2();
    });

    //登录
    $('#login_btn').on('click', function (e) {
        var email = $('#login_form input[name="email"]').val();
        var password = $('#login_form input[name="password"]').val();
        $.ajax({
            url: '/user/login',
            method: 'POST',
            data: {
                'email': email,
                'password': password
            },
            success: function (res) {
                if (res['status'] === 404) {
                    notify.error(res['msg'], 'center', 1000);
                } else {
                    notify.success(res['msg'], 'center', 1000);
                    setTimeout(function () {
                        location.reload();
                    }, 1500);
                }
            }
        });
    });

    //注册
    $('#register_btn').on('click', function (e) {
        var email = $('#register_form input[name="email"]').val();
        var password = $('#register_form input[name="password"]').val();
        var captcha = $('#register_form input[name="checkCode"]').val();
        $.ajax({
            url: '/user/register',
            method: 'POST',
            data: {
                'email': email,
                'password': password,
                'captcha': captcha
            },
            success: function (res) {
                if (res['status'] === 404) {
                    notify.error(res['msg'], 'center', 1000);
                } else {
                    notify.success(res['msg'], 'center', 1000);
                    setTimeout(function () {
                        $.ajax({
                            url: '/user/login',
                            method: 'POST',
                            data: {
                                'email': email,
                                'password': password
                            },
                            success: function (res) {
                                if (res['status'] === 404) {
                                    notify.error(res['msg'], 'center', 1000);
                                } else {
                                    notify.success(res['msg'], 'center', 1000);
                                    setTimeout(function () {
                                        location.reload();
                                    }, 1500);
                                }
                            }
                        });
                    }, 1500);
                }
            }
        });
    });

    //找回密码
    $('#retrieve_btn').on('click', function (e) {
        var email = $('#retrieve_form input[name="email"]').val();
        var password = $('#retrieve_form input[name="password"]').val();
        var captcha = $('#retrieve_form input[name="checkCode"]').val();
        $.ajax({
            url: '/user/retrieve',
            method: 'POST',
            data: {
                'email': email,
                'password': password,
                'captcha': captcha
            },
            success: function (res) {
                if (res['status'] === 404) {
                    notify.error(res['msg'], 'center', 1000);
                } else {
                    notify.success(res['msg'], 'center', 1000);
                    setTimeout(function () {
                        location.reload();
                    }, 1500);
                }
            }
        });
    });

});