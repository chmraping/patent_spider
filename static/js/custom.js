/**
 * Created by damon_lin on 15/4/28.
 */
$(document).ready(function () {
    //$("#set_btn").click(function () {
    //    $("#myModalLabel").text("设置")
    //})
    var today = new Date()
    var todayToStr = "" + today.getFullYear() +
        (today.getMonth() < 9 ? "0" + (today.getMonth() + 1) : today.getMonth() + 1) +
        (today.getDate() < 10 ? "0" + today.getDate() : today.getDate() )

    $("#end_day").val(todayToStr)

    $("#start_btn").click(function (e) {
        var validate = function (data) {
            var validatePattern = /^(\d{4})(\d{2})(\d{2})$/
            var result = data.match(validatePattern)
            if (result)
                result = result.map(function (e) {
                    return parseInt(e)
                })
            return result!==null && result[1] < 2200 && result[2] < 13 && result[3] < 32

        }
        e = e || window.event;
        e.preventDefault();
        data = {
            "start_day": $("#start_day").val(),
            "end_day": $("#end_day").val(),
            "start_id": $("#start_id").val(),
            "end_id": $("#end_id").val()
        }
        for(e in data){
            if(data[e] ==="") {
                alert("请输入完整信息")
                return
            }

        }
        if ( parseInt(data["start_day"]) < parseInt(data["end_day"])) { // 非空且结束时间比开始时间迟
            //初步的时间判断
            //正则表达式进行判断，以增强检验
            if (validate(data["start_day"]) && validate(data["end_day"])) {
                //通过检查
                $(this).text("正在抓取");
                $.ajax({
                    data: data,
                    type: 'post',
                    url: '/spider',
                    success: function (e) {
                        alert(e)
                        $("#start_btn").text("手动抓取")
                    }
                })
                return 1;
            }
        }

        alert("时间输入有误")


    })
    $("#reset_btn").click(function (e) {
        e = e || window.event;
        e.preventDefault();
        $.ajax({
            type: 'post',
            url: '/reset',
            success: function (e) {
                $("#manual_btn").text("手动抓取 ")
                $("#start_btn").text(" 确定")
                alert(e)
            }
        })
    })
    $("#save_btn").click(function (e) {
        e = e || window.event;
        e.preventDefault();
        data = $("#input_delay").val()
        var reg = /^[1-9]\d*$/;
        if (!reg.test(data)) {
            $("#myModalLabel").text("请输入合法数值！")
            return
        }
        $("#myModalLabel").text("正在请求...")
        $.ajax({
            type: 'post',
            url: '/set_setting',
            data: {"delay": data},
            success: function (e) {
                //$("#myModalLabel").text("成功开启监控")
                $.ajax({
                    type: 'post',
                    url: '/watch',
                    success: function (e) {
                        console.log(e)
                        if (e == 'ok') {
                            $("#myModalLabel").text("成功开启监控")
                        }
                        else {
                            $("#myModalLabel").text(e)
                        }

                    }
                })
            }
        })
    })
    $("#close_btn").click(function (e) {
        e = e || window.event;
        e.preventDefault();
        $("#myModalLabel").text("正在请求...")
        $.ajax({
            type: 'post',
            url: '/stop',
            success: function (e) {
                console.log(e)
                if (e == 'ok') {
                    $("#myModalLabel").text("成功关闭监控")
                }
                else {
                    $("#myModalLabel").text(e)
                }
            }
        })
    })
    $("#save_logout_btn").click(function (e) {
        e = e || window.event;
        e.preventDefault();
        $.getJSON('/unAuth', function (msg) {
            if (msg.STATE === "SUCCESS") {
                alert("退出登陆成功");
            }
            window.location.href = "accounts/login";
        })
    })



    var get_log = function () {
        $("#logModalLabel").text("正在请求...")
        $("#log_body").html(" ")
        $.ajax({
            type: 'post',
            url: '/log',
            success: function (e) {
                $("#log_body").html(e);
                $("#logModalLabel").text("日志纪录");
                $("#log_body").scrollTop($("#log_body")[0].scrollHeight + 100);
            }
        })
    }
    $("#log_btn").click(function (e) {
        e = e || window.event;
        e.preventDefault();
        get_log()
    })
    $("#refresh_btn").click(function (e) {
        e = e || window.event;
        e.preventDefault();
        get_log()
    })

})
