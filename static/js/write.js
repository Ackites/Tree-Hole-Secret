$(function () {
    $('footer').hide();
    $(window).scroll(function () {
        $('header').removeClass("header_fixed");
        var top = $(window).scrollTop();
        if (top > 80) {
            $('#wangeditor_toolbar').addClass("wangeditor_toolbar_fixed");
        } else {
            $('#wangeditor_toolbar').removeClass("wangeditor_toolbar_fixed");
        }
    });
    //write

    const E = window.wangEditor

// 切换语言
    const LANG = location.href.indexOf('lang=en') > 0 ? 'en' : 'zh-CN'
    E.i18nChangeLanguage(LANG)

    //编辑器配置
    const editorConfig = {
        placeholder: '请输入正文',
        scroll: false, // 禁止编辑器滚动
        MENU_CONF: {
            uploadImage: {
                server: '/api/upload',
                fieldName: 'your-fileName',
                timeout: 5 * 1000, // 5 秒
                // 上传进度的回调函数
                onProgress(progress) {       // JS 语法
                    // progress 是 0-100 的数字
                    console.log('progress', progress)
                },

                // 单个文件上传失败
                onFailed(file, res) {           // JS 语法
                    notify.error(`${file.name} 上传失败`, 'center', 1000);
                },

                // 上传错误，或者触发 timeout 超时
                onError(file, err, res) {               // JS 语法
                    notify.error(`${file.name} 上传出错`, 'center', 1000);
                },

                customUpload(file, insertFn) {                   // JS 语法
                    var data = new FormData();
                    data.append('f', file);
                    $.ajax({
                        url: "/article/write/upload",
                        method: 'post',
                        data: data,
                        contentType: false,
                        processData: false,
                        success: function (res) {
                            //将返回的本地地址插入到wangeditor中
                            insertFn(res['img_url'], res['filename'], res['img_url']);
                        }

                    })
                }
            }
        },
        onChange(editor) {
            $('.words span').text(editor.getText().length);
        }
    }


// 先创建 editor
    const editor = E.createEditor({
        selector: '#editor-text-area',
        content: [],
        config: editorConfig,
        mode: 'default', // or 'simple'
    })


    //菜单栏配置
    const toolbarConfig = {
        excludeKeys: ['group-video', 'fullScreen'],
    }

// 创建 toolbar
    const toolbar = E.createToolbar({
        editor,
        selector: '#editor-toolbar',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })

// 点击空白处 focus 编辑器
    document.getElementById('editor-text-area').addEventListener('click', e => {
        if (e.target.id === 'editor-text-area') {
            editor.blur()
            editor.focus(true) // focus 到末尾
        }
    })

    //保存文章
    $('#save_btn').on('click', () => {
        if (location.pathname === '/article/write') {
            $.ajax({
                url: '/article/publish',
                method: 'POST',
                data: {
                    title: $('#content input[name=title]').val(),
                    content: editor.getHtml(),
                    length: editor.getText().length,
                    id: 1
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
            });
        } else {
            $.ajax({
                url: '/article/publish',
                method: 'POST',
                data: {
                    title: $('#content input[name=title]').val(),
                    content: editor.getHtml(),
                    length: editor.getText().length,
                    id: 1,
                    aid: location.pathname.split('/')[2]
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
            });
        }
    });

    //发布文章
    $('#publish_btn').on('click', () => {
        if (location.pathname === '/article/write') {
            $.ajax({
                url: '/article/publish',
                method: 'POST',
                data: {
                    title: $('#content input[name=title]').val(),
                    content: editor.getHtml(),
                    length: editor.getText().length,
                    id: 2
                },
                success: function (res) {
                    if (res['status'] === 200) {
                        notify.success(res['msg'], 'center', 1000);
                        setTimeout(() => {
                            location.assign(res['id']);
                        }, 2000);
                    } else {
                        notify.error(res['msg'], 'center', 1000);
                    }
                }
            });
        } else {
            $.ajax({
                url: '/article/publish',
                method: 'POST',
                data: {
                    title: $('#content input[name=title]').val(),
                    content: editor.getHtml(),
                    length: editor.getText().length,
                    id: 2,
                    aid: location.pathname.split('/')[2]
                },
                success: function (res) {
                    if (res['status'] === 200) {
                        notify.success(res['msg'], 'center', 1000);
                        setTimeout(() => {
                            location.assign('/article/'+res['id']);
                        }, 2000);
                    } else {
                        notify.error(res['msg'], 'center', 1000);
                    }
                }
            });
        }

    });

    //检测
    if (location.pathname === '/article/write') {
    } else {
        $.ajax({
            url: location.pathname,
            method: 'post',
            success: function (res) {
                if (res['status'] === 200) {
                    $('#content input[name=title]').val(res['title']);
                    editor.setHtml(res['content']);
                }
            }
        })
    }
});