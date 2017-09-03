window.onload = admin_onload;

function admin_onload() {
    document.getElementById('prevPage').onclick = prevPage;
    document.getElementById('nextPage').onclick = nextPage;
}

function getParam(decode_url, name) {
    try{
        var params = decode_url.split("?");
        params = params[1].split("&");
        for(var i=0; i<params.length; i++) {
            var param = params[i];
            kv = param.split('=');
            if(kv[0] == name){
                var index = kv[1].indexOf('#');
                if(index > 0){
                    var keywords = kv[1].substring(0, index);
                    return keywords;
                }else{
                    return kv[1];
                }
            }
        }
    }catch(err){
        return null;
    }
    return null;
}

function prevPage() {

    var page_index = 1;
    var baseUri = window.location.pathname;
    var str_index = getUrlPara('page_index');
    if (str_index != null){
        page_index = parseInt(str_index);
    }

    page_index = page_index - 1;
    if (page_index < 1){
        page_index = 1;
    }
    var uri = baseUri + '?page_index=' + page_index;

    var decode_url = decodeURIComponent(window.location);
    var keywords = getParam(decode_url, 'keywords');

    if(keywords != null){
        uri = uri + '&keywords=' + keywords;
    }

    window.location.href = uri;
}

function nextPage() {
    var page_index = 1;
    var baseUri = window.location.pathname;
    var str_index = getUrlPara('page_index');
    if (str_index != null){
        page_index = parseInt(str_index);
    }

    page_index = page_index + 1;
    if (page_index > window.g_total){
        page_index = window.g_total;
    }
    var uri = baseUri + '?page_index=' + page_index;


    var decode_url = decodeURIComponent(window.location);
    var keywords = getParam(decode_url, 'keywords');

    if(keywords != null){
        uri = uri + '&keywords=' + keywords;
    }

    window.location.href = uri;
}