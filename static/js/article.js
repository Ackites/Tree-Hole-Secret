$(function () {
    //添加jq 图片插件
    $(".editor-content-view img").each(function () {
        var element = document.createElement("a");
        $(element).attr("data-fancybox", "gallery");
        $(element).attr("href", $(this).attr("src"));
        $(this).wrap(element);
    });

    //文章点赞
    $("#like").on("click", function (e) {
        $.ajax({
            url: location.pathname + '/like',
            method: "POST",
            success: function (res) {
                if (res['status'] === 200) {
                    location.reload();
                } else {
                    notify.error(res['msg'], 'center', 1000);
                }
            }
        })
    });

    //打开留言
    $("#comment").on("click", function (e) {
        $('.article_box').toggleClass('article_box_toggles');
        $('.comment_box').toggle('slow');
    });

    //滚动调整左侧侧边按钮位置
    $(window).scroll(function () {
        var scrollTop = $(window).scrollTop();
        if (scrollTop > 0) {
            $('.article_sidebar').css('top', scrollTop + 165 + 'px');
        }
    });

    //评论框
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

    //发布按钮隐藏
    $('.textarea_css').on('click', function () {
        $('#comment_bottom').show();
    });

    $(document).on('dblclick', function (e) {
        $('#comment_bottom').hide();
    });

    //实时获取字数
    $('.textarea_css').bind('input propertychange', function () {
        $('.comment_bottom .box_info span').text($('.textarea_css').val().length);
    });

    //发布评论
    $("#btn_1").on("click", function (e) {
        $.ajax({
            url: location.pathname + '/comment',
            method: "POST",
            data: {
                'content': $('#textarea_1').val(),
                'id': 1
            },
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
        })
    });

    //评论点赞
    $(".comment_df").on("click", function (e) {
        $.ajax({
            url: location.pathname +'/comment' + '/like',
            method: "POST",
            data: {
              'comment_id': $(this).data('comment_id'),
            },
            success: function (res) {
                if (res['status'] === 200) {
                    location.reload();
                } else {
                    notify.error(res['msg'], 'center', 1000);
                }
            }
        })
    });
});