window.onload = admin_onload;

function admin_onload() {
    load_page();

    document.getElementById('submitCommentContext').onclick = addCommentContext;
    document.getElementById('addFavoriteNumber').onclick = addFavoriteNumber;
}

function load_page() {
    var baseUri = window.location.pathname
    var start = baseUri.lastIndexOf("\/");
    var uri = 'addReadNumber/';
    uri = uri + baseUri.substring(start+1, baseUri.length);
    //alert(uri);
    $.ajax({
            async: false,
            url: uri,
            method: 'get',
            dataType: 'json',
            success: function (result) {
                //alert(JSON.stringify(result));
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
            }
    });
}

function addCommentContext() {
    var data = new Object();
    data.context = document.getElementById('commentContext').value;
    var uri = window.location.pathname
    var start = uri.lastIndexOf("\/");
    data.article_id = uri.substring(start+1, uri.length);

    //alert(JSON.stringify(data));
    $.ajax({
            async: false,
            url: 'addComment',
            method: 'post',
            data: JSON.stringify(data),
            dataType: 'json',
            success: function (result) {
                //alert(JSON.stringify(result));
                if (result.ret_code == 0) {
                     window.location.reload(true);
                }else if (result.ret_code == 10000){
                    alert("文章评论数超过最大限制");
                }else {
                    alert("添加评论失败");
                }
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
            }
    });
}

function addFavoriteNumber() {
    var baseUri = window.location.pathname
    var start = baseUri.lastIndexOf("\/");
    var uri = 'addFavoriteNumber/';
    uri = uri + baseUri.substring(start+1, baseUri.length);
    //alert(uri);
    $.ajax({
            async: false,
            url: uri,
            method: 'get',
            dataType: 'json',
            success: function (result) {
                //alert(JSON.stringify(result));
                return false;
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
            }
    });
    self.location.reload(true);
}