// ==UserScript==
// @name         小鹅通
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        *://*.h5.xiaoeknow.com/*
// @grant        none
// ==/UserScript==

(function() {
    function hook() {
    var oriXOpen = XMLHttpRequest.prototype.open;
    console.log("do hook...");
    var x = document.getElementById('url_result');
    if (x == undefined) {
        var y = document.createElement("div");
        y.setAttribute("style", "position:absolute;font-size: small; width: 400px;word-break:break-all;margin: 100px 20px;");
        document.body.insertBefore(y, document.body.firstChild);
        var title = document.createElement("span");
        title.innerText = "下载链接：";
        y.appendChild(title);

        x = document.createElement("div");
        x.setAttribute("type", "text");
        x.setAttribute("id", "url_result");
        x.setAttribute("data_url", "");
        x.setAttribute("key_url", "");
        var referer_url = location.protocol + "//" + location.host;
        x.setAttribute("referer_url", referer_url);
        var detail_title = document.getElementsByClassName('detail-title')[0];
        if (detail_title == undefined) {
            x.setAttribute("video_name", "");
        } else {
            x.setAttribute("video_name", detail_title.innerText);
        }
        x.setAttribute("style", "font-size: small; width: 400px;word-break:break-all;");
        x.innerHTML = "";
        y.appendChild(x);
    }

    XMLHttpRequest.prototype.open = function(method,url,asncFlag,user,password) {
        if (url.indexOf("ts") != -1 || url.indexOf("key") != -1) {
            var x = document.getElementById('url_result');
            if (x != undefined) {
                var title = document.getElementsByClassName('detail-title')[0];
                if (title != undefined) {
                    x.setAttribute("video_name", title.innerText);
                }
                if (url.indexOf("ts") != -1) {
                    x.setAttribute("data_url", url);
                }
                if (url.indexOf("key") != -1) {
                    x.setAttribute("key_url", url);
                }
                x.innerHTML = "<span style='color:blue;'>" + x.getAttribute("video_name") + "</span>|" +
                    "<span style='color:green;'>" + x.getAttribute("data_url") + "</span>|" +
                    "<span style='color:red;'>" + x.getAttribute("key_url") + "</span>|" +
                    "<span style='color:blue;'>" + x.getAttribute("referer_url") + "</span>";
            }
            console.log(url);
        }
        oriXOpen.call(this,method,url,asncFlag,user,password);
    };
}

var url_result = document.getElementById('url_result');
if (url_result == undefined){
    hook();
}

})();
