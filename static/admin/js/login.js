/*
author: Abel Lee
date: 2017
Copyright: free
 */

window.onload = login_onload;

function login_onload() {
    document.getElementById('login').onclick = login;
}

function login() {
    var data = new Object();
    data.username = document.getElementById('username').value;
    data.password = document.getElementById('password').value;
    $.ajax({
            async: false,
            url: "/login",
            method: "post",
            data: JSON.stringify(data),
            dataType: "json",
            success: function (result) {
                alert(JSON.stringify(result));
                if (result.ret_code == 0) {
                    alert("登录成功！");
                } else {
                    alert("登录失败");
                }
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"))
            }
    });
}
