layui.use(function () {
    var $ = layui.$
        , carousel = layui.carousel
        , flow = layui.flow;

    //首页轮播图
    carousel.render({
        elem: '#index_carousel'
        , width: '100%'
        , arrow: 'hover'
        , anim: 'default'
    });

    //首页情感卡片
    function col() {
        var width = $(window).width()
            , colNum = 4;
        if (width >= 1200) {
            colNum = 4; //大屏幕 4列
        } else if (width >= 992) {
            colNum = 3; //中屏幕 3列
        } else if (width >= 768) {
            colNum = 2; //小屏幕 2列
        } else {
            colNum = 1; //超小屏幕 1列
        }
        return colNum;
    }

    flow.load({
        elem: '#card_container',
        isAuto: false,
        isLazyimg: true,
        done: function (page, next) {
            setTimeout(function () {
                var lis = [];
                for (var i = 0; i < 20; i++) {
                    lis.push('<div class="lite_card box_shadow">测试</div>');
                }
                next(lis.join(''), page < 6); //假设总页数为 6
                $('#card_container').BlocksIt({
                    numOfCol: col(),
                    offsetX: 8,
                    offsetY: 8
                });
            }, 500);
        }
    });
    $(window).resize(function () {
        $('#card_container').BlocksIt({
            numOfCol: col(),
            offsetX: 8,
            offsetY: 8
        });
    });

});