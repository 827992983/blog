window.onload = admin_onload;

function admin_onload() {
    document.getElementById('submitCommentContext').onclick = addCommentContext;
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
                }else{
                    alert("添加评论失败");
                }
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
            }
    });
}
