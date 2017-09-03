window.onload = admin_onload;

function admin_onload() {

    document.getElementById('prevPage').onclick = prevPage;
    document.getElementById('nextPage').onclick = nextPage;
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
    var uri = baseUri + '?page_index=' + String(page_index);

    var keywords = getUrlPara('keywords');
    if(keywords != null){
        uri = uri + '&keywords=' + String(keywords);
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
    var uri = baseUri + '?page_index=' + String(page_index);

    var keywords = getUrlPara('keywords');
    if(keywords != null){
        uri = uri + '&keywords=' + String(keywords);
    }

    window.location.href = uri;
}