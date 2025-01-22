if (!localStorage.getItem('pageLoaded')) {
    if (typeof location.search.split('order_by=')[1] == "undefined") {
        reload();
    }
}

function setOrder_by(name) {
    window.sessionStorage.setItem('order_by', name);
    reload();
}

function setFilter_vm(name) {
    window.sessionStorage.setItem('vm', "&vm=" + name);
    reload();
}

function setFilter_em(name) {
    window.sessionStorage.setItem('em', "&em=" + name);
    reload();
}

function setFilter_tr(name) {
    window.sessionStorage.setItem('tr', "&tr=" + name);
    reload();
}

function setFilter_dam(name) {
    window.sessionStorage.setItem('dam', "&dam=" + name);
    reload();
}

function setFilter_sam(name) {
    window.sessionStorage.setItem('sam', "&sam=" + name);
    reload();
}

function reset() {
    sessionStorage.clear();
    reload();
}

function reload() {
    if (window.sessionStorage.getItem('order_by') === null) {
        order_by = "?order_by=shipment_date";
    }
    else {
        order_by = window.sessionStorage.getItem('order_by');
    }

    if (window.sessionStorage.getItem('vm') === null) { te = ""; } else { te = window.sessionStorage.getItem('vm'); }
    if (window.sessionStorage.getItem('em') === null) { en = ""; } else { en = window.sessionStorage.getItem('em'); }
    if (window.sessionStorage.getItem('tr') === null) { tr = ""; } else { tr = window.sessionStorage.getItem('tr'); }
    if (window.sessionStorage.getItem('dam') === null) { da = ""; } else { da = window.sessionStorage.getItem('dam'); }
    if (window.sessionStorage.getItem('sam') === null) { sa = ""; } else { sa = window.sessionStorage.getItem('sam'); }

    httpParam = order_by + te + en + tr + da + sa;

    window.location.href = httpParam;
}
