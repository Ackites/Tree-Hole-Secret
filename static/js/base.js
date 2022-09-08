layui.use(function () {
    var $ = layui.$
        , layer = layui.layer
        , notify = layui.notify
        , form = layui.form;

    //侧边返回顶部按钮
    $('#back_top').hide();
    $(window).scroll(function () {
        var scrollT = $(window).scrollTop();
        if (scrollT > 200) {
            $('#back_top').fadeIn();
        } else {
            $('#back_top').fadeOut();
        }
        $('#back_top').on("click", function () {
            $('body, html').stop().animate({
                scrollTop: 0
            });
        })
    });

    //侧边发布内容按钮
    $('#write_story').on("click", function () {
        $.ajax({
            url: '/article/write',
            method: 'POST',
            success: function (res) {
                if (res['status'] === 404) {
                    notify.warning(res['msg'], 'center', 1000);
                } else {
                    location.assign('/article/write');
                }
            }
        })
    });

    //粘性导航
    var basic = 80;
    $(window).scroll(function () {
        var top = $(window).scrollTop();
        if (top > basic) {
            $('header').removeClass("header_fixed");
            $('.header_nav > ul > li > a').removeClass("pad");
        } else if (top < basic && top > 80) {
            $('header').addClass("header_fixed");
            $('.header_nav > ul > li > a').addClass("pad");
        }else if(top < 80){
            $('header').removeClass("header_fixed");
            $('.header_nav > ul > li > a').removeClass("pad");
        }
        basic = top;
    });

    //导航栏切换高亮
    $('.ul_nav li').eq(0).addClass("ul_nav_a");
    $('.ul_nav li').each(function () {
        $(this).on('click', function () {
            $(this).addClass('ul_nav_a').siblings().removeClass('ul_nav_a');
        })
    });

    //弹出登录框
    $('#user_box').on('click', function () {
        var u = $('.user_login');
        layer.open({
            type: 1,
            title: false,
            content: u,
            area: '330px',
            closeBtn: 1,
            anim: 0,
            resize: false,
            move: false,
            shadeClose: true,
            id: 'userbox',
            end: function () {
                $('#login').show();
                $('#register').hide();
                $('#retrieve').hide();
                $('.user_login').hide();
                $('#retrieve_form')[0].reset();
                $('#register_form')[0].reset();
                $('#login_form')[0].reset();
                form.render();
            }
        });
        u.parent('.layui-layer-content').css('overflow', 'visible');
        u.parents('.layui-layer').css('border-radius', '10px');
        $('#login').on('keydown', function (e) {
            if (e.keyCode == 13) {
                $('#login_btn').click();
            }
        });
        $('#register').on('keydown', function (e) {
            if (e.keyCode == 13) {
                $('#register_btn').click();
            }
        });
        $('#retrieve').on('keydown', function (e) {
            if (e.keyCode == 13) {
                $('#retrieve_btn').click();
            }
        });
    });

    //login user_avatar
    $(document).on('click', function (e) {
        $('.avatar_click').fadeOut();
    });
    $('#user_avatar').on('click', function (e) {
        e.stopPropagation();
        $('.avatar_click').fadeToggle();
    });

});