/*
author: Abel Lee
date: 2017
Copyright: free
 */

window.onload = admin_onload;

var username = '';

function admin_onload() {
    load_page();
    /*
    getArticleTitles('modify');
    getArticleTitles('delete');
    getArticle('modify');
    getArticle('delete');
    */

    document.getElementById('addArticle').onclick = addArticle;
    document.getElementById('modifyArticle').onclick = modifyArticle;
    document.getElementById('deleteArticle').onclick = deleteArticle;

    $("#modifyArticleType").change(function() {
        getArticleTitles('modify');
        getArticle('modify');
    });
    $("#deleteArticleType").change(function() {
        getArticleTitles('delete');
        getArticle('delete');
    });

    $("#modifyArticleTitle").change(function() { getArticle('modify'); });
    $("#deleteArticleTitle").change(function() { getArticle('delete'); });

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
    data.auther = username;
    data.type_id = $('#addArticleType option:selected').val();
    data.htlm_context = UE.getEditor('editor').getContent();

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

function getArticleTitles(module) {
    var url = '/getArticleTitles?type_id=';
    if(module == 'modify'){
        url = url + $('#modifyArticleType option:selected').val();
    }else if(module == 'delete'){
        url = url + $('#deleteArticleType option:selected').val();
    }else{
        alert('参数错误');
        return 0;
    }

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
                    if (module == 'modify'){
                        $("#modifyArticleTitle").empty();
                        selectObj = document.getElementById('modifyArticleTitle');
                    }else if(module == 'delete'){
                        $("#deleteArticleTitle").empty();
                        selectObj = document.getElementById('deleteArticleTitle');
                    }else{
                        alert('参数错误');
                        return 0;
                    }

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

function getArticle(module) {
    var url = '/getArticleContent?article_id=';
    if(module == 'modify'){
        url = url + $('#modifyArticleTitle option:selected').val();
    }else if(module == 'delete'){
        url = url + $('#deleteArticleTitle option:selected').val();
    }else{
        alert('参数错误');
        return 0;
    }

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

    $.ajax({
            async: false,
            url: 'modifyArticle',
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