/**
 * Created by Administrator on 2017/7/15.
 */

var BANNER_TIME = 20000;

var img_container = document.querySelectorAll(".img-container");
var con_div_array = document.querySelectorAll(".controller .con");
var current_banner = 0;

var timer;

/* 启动app */
start_app();


function start_app() {
    /* 启动定时器 */
    timer = setInterval(trans_banner, BANNER_TIME);
    control_click();
}

function control_click() {
    for (var i = 0; i < con_div_array.length; i++) {
        (function (i) {
            var con_div = con_div_array[i];
            con_div.onclick = function () {
                clearInterval(timer);
                trans_banner(i);
                timer = setInterval(trans_banner, BANNER_TIME);
            };
        })(i);
    }
}

/* Banner 轮转动画 */
function trans_banner(click_index) {
    var next_banner;

    if (click_index === undefined) {
        next_banner = current_banner + 1 < img_container.length ? current_banner + 1 : 0;
    }else{
        next_banner = click_index;
    }

    if (current_banner === next_banner) {
        return;
    }

    for (var i = 0; i < img_container.length; i++) {
        var a_div = img_container[i];
        var con_div = con_div_array[i];
        if (i === current_banner) {
            a_div.style.opacity = 0;
            con_div.className = "con";
        }else if (i === next_banner) {
            a_div.style.opacity = 1;
            con_div.className = "con active";
        }
    }
    current_banner = next_banner;
}