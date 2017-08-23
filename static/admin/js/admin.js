/*
author: Abel Lee
date: 2017
Copyright: free
 */

window.onload = admin_onload;

var username = '';

function admin_onload() {
    load_page();

    document.getElementById('addArticle').onclick = addArticle;
    document.getElementById('modifyArticle').onclick = modifyArticle;
    document.getElementById('deleteArticle').onclick = deleteArticle;

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
                alert(JSON.stringify(result));
                if (result.ret_code == 0) {
                    var data = result.data;
                    var articleTypes = document.getElementById('addArticleType');
                    var i = 0;
                    for (i = 0; i < data.length; i++) {
                        articleTypes.options.add(new Option(data[i].description,data[i].type_name));
                    }

                    i = 0;
                    articleTypes = document.getElementById('modifyArticleType');
                    for (i = 0; i < data.length; i++) {
                        articleTypes.options.add(new Option(data[i].description,data[i].type_name));
                    }

                    i =0 ;
                    articleTypes = document.getElementById('deleteArticleType');
                    for (i = 0; i < data.length; i++) {
                        articleTypes.options.add(new Option(data[i].description,data[i].type_name));
                    }
                }else{
                    alert("登录失败");
                }
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
            }
    });
}

function addArticle() {
    var title = document.getElementById('addArticleTitle').innerHTML;
    $.ajax({
            async: false,
            url: 'addArticle',
            method: 'post',
            dataType: 'json',
            success: function (result) {
                alert(JSON.stringify(result));
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

function getArticle() {

    $.ajax({
            async: false,
            url: 'addArticle',
            method: 'post',
            dataType: 'json',
            success: function (result) {
                alert(JSON.stringify(result));
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


function modifyArticle() {

    $.ajax({
            async: false,
            url: 'modifyArticle',
            method: 'post',
            dataType: 'json',
            success: function (result) {
                alert(JSON.stringify(result));
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


function deleteArticle() {
    $.ajax({
            async: false,
            url: 'deleteArticle',
            method: 'post',
            dataType: 'json',
            success: function (result) {
                alert(JSON.stringify(result));
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