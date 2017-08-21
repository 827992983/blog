/*
author: Abel Lee
date: 2017
Copyright: free
 */

window.onload = admin_onload;

var username = '';

function admin_onload() {
    username = getUrlPara('username');
    document.getElementById('username').innerHTML = username + ', ';

    document.getElementById('logout').onclick = logout;
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