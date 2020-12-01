// ==UserScript==
// @name         video downloader
// @namespace    http://tampermonkey.net/
// @version      0.3
// @description  try to take over the world!
// @author       You
// @match        *://*.h5.xiaoeknow.com/*
// @grant        none
// ==/UserScript==

(function() {
    function do_test_my_video(){
        if (window.myVideo == undefined || window.myVideo == null || window.myVideo.offsetParent == undefined)
        {
            setTimeout(do_test_my_video, 1000);
            return;
        }
        //var custom_video_player_10001 = document.getElementsByClassName('custom_video_player_10001')[0];
        //var url2 = custom_video_player_10001.__vue__._data.props.url[0].url;
        var url = window.myVideo.offsetParent.__vue__._data.props.url[0].url;
        if (url == null)
        {
            setTimeout(do_test_my_video, 1000);
            return;
        }
        var x = document.getElementById('url_result');
        if (x.getAttribute("m3u8") == undefined)
        {
            console.log("================m3u8:" + url);
            x.setAttribute("m3u8", url);
            x.innerHTML = "<span style='color:blue;'>" + x.getAttribute("video_name") + "</span>|" +
                "<span style='color:green;'>" + x.getAttribute("m3u8") + "</span>||" +
                "<span style='color:blue;'>" + x.getAttribute("referer_url") + "</span>";
        }
    }
    function hook() {
        var detail_title = document.getElementsByClassName('detail-title')[0];
        if (detail_title == undefined)
        {
            setTimeout(hook, 1000);
            return;
        }
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
            x.setAttribute("data_url", "data_url获取中");
            x.setAttribute("key_url", "key_url获取中");
            var referer_url = location.protocol + "//" + location.host;
            x.setAttribute("referer_url", referer_url);
            x.setAttribute("video_name", detail_title.innerText);
            x.setAttribute("style", "font-size: small; width: 400px;word-break:break-all;");
            x.innerHTML = "<span style='color:blue;'>" + x.getAttribute("video_name") + "</span>|" +
                "<span style='color:green;'>" + x.getAttribute("data_url") + "</span>|" +
                "<span style='color:red;'>" + x.getAttribute("key_url") + "</span>|" +
                "<span style='color:blue;'>" + x.getAttribute("referer_url") + "</span>";
            y.appendChild(x);
        }

        var oriXOpen = XMLHttpRequest.prototype.open;
        if (oriXOpen == undefined)
        {
            x.setAttribute("data_url", "data_url");
            x.setAttribute("key_url", "key_url");
            x.innerHTML = "<span style='color:blue;'>" + x.getAttribute("video_name") + "</span>|" +
                "<span style='color:green;'>" + x.getAttribute("data_url") + "</span>|" +
                "<span style='color:red;'>" + x.getAttribute("key_url") + "</span>|" +
                "<span style='color:blue;'>" + x.getAttribute("referer_url") + "</span>";
            x.innerHTML = x.innerHTML + "<br><span style='color:IndianRed;'>无法自动获取URL。" +
                "请按F12，在network或者网络标签页中使用ts和key关键字过滤，手动获取data_url和key_url</span>";
        }
        else
        {
            console.log("do hook...");
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
    }

var url_result = document.getElementById('url_result');
if (url_result == undefined){
    hook();
    do_test_my_video();
}

})();
