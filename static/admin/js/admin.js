/*
author: Abel Lee
date: 2017
Copyright: free
 */

window.onload = admin_onload;

var username = '';

function admin_onload() {
    load_page();
    getArticleTitles();
    getArticle();

    document.getElementById('addArticle').onclick = addArticle;
    document.getElementById('modifyArticle').onclick = modifyArticle;

    $("#modifyArticleType").change(function() {
        getArticleTitles();
        getArticle();
    });

    $("#modifyArticleTitle").change(function() { getArticle(); });

    $("#addArticleTitle").focus(function(){ UE.getEditor('editor').setContent('', false); });

    document.getElementById('logout').onclick = logout;
}

function load_page() {
    username = getUrlPara('username');
    document.getElementById('username').innerHTML = username + ', ';

    $.ajax({
            async: false,
            url: '/getArticleType',
            method: 'get',
            dataType: 'json',
            success: function (result) {
                //alert(JSON.stringify(result));
                if (result.ret_code == 0) {
                    var data = result.data;
                    var articleTypes = document.getElementById('addArticleType');
                    var i = 0;
                    for (i = 0; i < data.length; i++) {
                        articleTypes.options.add(new Option(data[i].type_name,data[i].type_id));
                    }

                    i = 0;
                    articleTypes = document.getElementById('modifyArticleType');
                    for (i = 0; i < data.length; i++) {
                        articleTypes.options.add(new Option(data[i].type_name,data[i].type_id));
                    }

                    i =0 ;
                    articleTypes = document.getElementById('deleteArticleType');
                    for (i = 0; i < data.length; i++) {
                        articleTypes.options.add(new Option(data[i].type_name,data[i].type_id));
                    }
                }else{
                    alert("载入数据失败");
                }
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
            }
    });
}

function addArticle() {
    var data = new Object();
    data.title = document.getElementById('addArticleTitle').value;
    data.author = username;
    data.type_id = $('#addArticleType option:selected').val();
    data.html_context = UE.getEditor('editor').getContent();

    //alert(JSON.stringify(data));
    $.ajax({
            async: false,
            url: 'addArticle',
            method: 'post',
            data: JSON.stringify(data),
            dataType: 'json',
            success: function (result) {
                //alert(JSON.stringify(result));
                if (result.ret_code == 0) {
                    //window.location = '/admin';
                }else{
                    alert("添加文章失败");
                }
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
            }
    });
}

function getArticleTitles() {
    var url = '/getArticleTitles?type_id=';
    url = url + $('#modifyArticleType option:selected').val();

    $.ajax({
            async: false,
            url: url,
            method: 'get',
            dataType: 'json',
            success: function (result) {
                //alert(JSON.stringify(result));
                if (result.ret_code == 0) {
                    var data = result.data;
                    var selectObj = null;
                    $("#modifyArticleTitle").empty();
                    selectObj = document.getElementById('modifyArticleTitle');

                    var i = 0;
                    for (i = 0; i < data.length; i++) {
                        selectObj.options.add(new Option(data[i].title,data[i].article_id));
                    }
                }else{
                    alert("载入数据失败");
                }
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
            }
    });
}

function getArticle() {
    var url = '/getArticleContent?article_id=';
    url = url + $('#modifyArticleTitle option:selected').val();

    //alert(url);
    $.ajax({
            async: false,
            url: url,
            method: 'get',
            dataType: 'json',
            success: function (result) {
                //alert(JSON.stringify(result));
                if (result.ret_code == 0) {
                    UE.getEditor('editor').setContent(result.data, false);
                }else{
                    alert("载入数据失败");
                }
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
            }
    });
}

function modifyArticle() {
    var data = new Object();
    data.article_id = $('#modifyArticleTitle option:selected').val();
    data.operation = $("input[type='radio']:checked").val();
    data.html_context = UE.getEditor('editor').getContent();

    //alert(JSON.stringify(data));
    $.ajax({
            async: false,
            url: '/modifyArticle',
            method: 'post',
            data: JSON.stringify(data),
            dataType: 'json',
            success: function (result) {
                //alert(JSON.stringify(result));
                if (result.ret_code == 0) {
                    //window.location = '/admin';
                }else{
                    alert("添加文章失败");
                }
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
            }
    });
}


function deleteArticle() {
    $.ajax({
            async: false,
            url: 'deleteArticle',
            method: 'post',
            dataType: 'json',
            success: function (result) {
                alert(JSON.stringify(result));
                if (result.ret_code == 0) {
                    //window.location = '/admin';
                }else{
                    alert("登录失败");
                }
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
            }
    });
}

function logout() {
    var requestUrl = '';
    requestUrl = '/logout?username=' + username;
    $.ajax({
            async: false,
            url: requestUrl,
            method: "get",
            dataType: "json",
            success: function (result) {
                //alert(JSON.stringify(result));
                if (result.ret_code == 0) {
                    window.location = '/admin';
                }else{
                    alert("登录失败");
                }
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
            }
    });
}