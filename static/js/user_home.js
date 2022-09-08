$(function () {
    $('footer').hide();
    //编辑个人资料
    $('#edit_btn').on('click', function (e) {
        location.assign('/user/settings');
    });

    //头像旋转
    $('.user_avatar').on('mouseenter', function (e) {
        $(this).addClass('layui-anim-rotate').addClass('layui-anim-loop');
    });

    $('.user_avatar').on('mouseleave', function (e) {
        $(this).removeClass('layui-anim-rotate').removeClass('layui-anim-loop');
    });

    //个人设置侧边栏切换
    $('.settings_left a').eq(0).addClass("active");
    $('.settings_left a').each(function () {
        $(this).on('click', function () {
            $(this).addClass('active').siblings().removeClass('active');
        })
    });

    //切换
    $('#personal_information_btn').on('click', function () {
        $('#personal_information').show();
        $('#Account_Settings').hide();
    });
    $('#Account_Settings_btn').on('click', function () {
        $('#personal_information').hide();
        $('#Account_Settings').show();
    });

    //个人介绍
    $.fn.autoHeight = function () {
        function autoHeight(elem) {
            elem.style.height = 'auto';
            elem.scrollTop = 0; //防抖动
            elem.style.height = elem.scrollHeight + 'px';
        }

        this.each(function () {
            autoHeight(this);
            $(this).on('keyup', function () {
                autoHeight(this);
            });
        });
    }
    $('textarea[autoHeight]').autoHeight();

    //字数统计
    $('input[name=username]').bind('input propertychange', function () {
        $('#yonghuming').text($('input[name=username]').val().length + '/20');
    });
    $('textarea[name=user_description]').bind('input propertychange', function () {
        $('#miaoshu').text($('textarea[name=user_description]').val().length + '/100');
    });

    //上传头像
    $('.avatar_upload').on('mouseenter', function () {
        $('.avatar_upload_shadow').css('visibility', 'visible');
    });
    $('.avatar_upload').on('mouseleave', function () {
        $('.avatar_upload_shadow').css('visibility', 'hidden');
    });


    layui.use(['element', 'layer', 'upload', 'form'], function () {
        var element = layui.element,
            $ = layui.$,
            layer = layui.layer,
            upload = layui.upload,
            form = layui.form;

        //删除文章
        $('.article_delete').on('click', function (e) {
            var $this = $(this);
            layer.msg('确定删除吗？', {
                btn: ['确定', '取消']
                , yes: function (index, layero) {
                    $.ajax({
                        url: '/article/' + $this.data('article_id') + '/delete',
                        method: 'post',
                        success: function (res) {
                            if (res['status'] === 200) {
                                notify.success(res['msg'], 'center', 1000);
                                setTimeout(() => {
                                    location.reload();
                                }, 2000);
                            } else {
                                notify.error(res['msg'], 'center', 1000);
                            }
                        }
                    });
                }
                , btn2: function (index, layero) {
                    layer.close(index);
                }
            });
        });

        //修改资料
        $('#commit_edit').on('click', function (e) {
            var username = $('#username_input').val();
            var description = $('#des_textarea').val();

            function che_username(value) {
                if (!new RegExp("^[a-zA-Z0-9_\u4e00-\u9fa5·]+$").test(value)) {
                    notify.warning('用户名不能有特殊字符', 'center');
                    return false;
                }
                if (/(^\_)|(\__)|(\_+$)/.test(value)) {
                    notify.warning('用户名首尾不能出现下划线\'_\'', 'center');
                    return false;
                }
                if (/^\d+\d+\d$/.test(value)) {
                    notify.warning('用户名不能全为数字', 'center');
                    return false;
                }
                if (value.length === 0) {
                    notify.warning('用户名不能为空', 'center');
                    return false;
                }
                return true;
            }

            function che_description(value) {
                if (value.length === 0) {
                    notify.warning('个人介绍不能为空', 'center');
                    return false;
                }
                return true;
            }

            if (che_username(username) && che_description(description)) {
                $.ajax({
                    url: '/user/settings/upload',
                    method: 'POST',
                    data: {
                        username: $('#username_input').val(),
                        description: $('#des_textarea').val(),
                    },
                    success: function (res) {
                        if (res['code'] === 0) {
                            notify.success(res['msg'], 'center', 1000);
                            setTimeout(function () {
                                location.reload();
                            }, 2000);
                        } else {
                        }
                    }
                });
            } else {
            }
        });


        // 上传头像
        upload.render({
            elem: '.avatar_upload_shadow' //绑定元素
            , url: '/user/settings/upload' //上传接口
            , accept: 'images'
            , acceptMime: 'image/jpg, image/png, image/jpeg'
            , exts: 'jpg|png|jpeg'
            , auto: false
            , number: 1
            , bindAction: '#commit_edit'
            , size: 5120 //最大允许上传的文件大小
            , choose: function (obj) {
                obj.preview(function (index, file, result) {
                    $('.avatar_upload_img').attr('src', result); //图片链接（base64）
                });
                $('.my_avatar').text('预览').css('color', '#1d7dfa');
                $('.my_avatar_format').text('点击下方保存修改后生效');
            }
            , done: function (res, index, upload) {
                //上传完毕回调
                if (res.code === 0) {
                    notify.success(res['msg'], 'center', 1000);
                    setTimeout(function () {
                        location.reload();
                    }, 2000);
                }
            }
            , error: function (index, upload) {
                //请求异常回调
            }
        });
    });
});