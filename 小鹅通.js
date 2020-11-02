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
    var x = document.getElementsByClassName('url_result')[0];
    if (x == undefined) {
        x = document.createElement("div");
        x.setAttribute("type", "text");
        x.setAttribute("class", "url_result");
        x.setAttribute("data_url", "");
        x.setAttribute("key_url", "");
        var title = document.getElementsByClassName('detail-title')[0];
        if (title == undefined) {
            x.setAttribute("video_name", "");
        } else {
            x.setAttribute("video_name", title.innerText);
        }
        x.setAttribute("style", "font-size: small; margin: 80px; ");
        x.innerHTML = x.getAttribute("video_name") + "|" + x.getAttribute("data_url") + "|" + x.getAttribute("key_url");
        document.body.insertBefore(x, document.body.firstChild);
    }

    XMLHttpRequest.prototype.open = function(method,url,asncFlag,user,password) {
        var distribute = document.getElementsByClassName('distribute')[0];
        if (distribute != undefined) {
            distribute.setAttribute("style", "visibility:hidden;");
        }
        if (url.indexOf("ts") != -1 || url.indexOf("key") != -1) {
            var x = document.getElementsByClassName('url_result')[0];
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
                    "<span style='color:red;'>" + x.getAttribute("key_url") + "</span>";
            }
            console.log(url);
        }
        oriXOpen.call(this,method,url,asncFlag,user,password);
    };
}

var url_result = document.getElementsByClassName('url_result')[0];
if (url_result == undefined){
    hook();
}

})();
