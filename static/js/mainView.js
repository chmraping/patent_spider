/**
 * 专利显示页的js代码
 * Created by abnerzheng on 15/4/21.
 */

angular.module('ui.bootstrap.demo', ['ui.bootstrap', 'ng.httpLoader']); //依赖注入，前端用了angular+bootstrap UI
angular.module('ui.bootstrap.demo').config(['httpMethodInterceptorProvider',
        function (httpMethodInterceptorProvider) {
            httpMethodInterceptorProvider.whitelistDomain('get_record_detail');
            httpMethodInterceptorProvider.whitelistDomain('get_company');
        }]
).controller('AccordionDemoCtrl', function ($scope, $http) {
        //一些初始化条件
        $scope.oneAtATime = true;
        $scope.companyName = "华为"; //公司名称
        //$scope.companyCode = "336666"; //股票代码，这里还未用到
        $scope.names = [];

        //模糊查询公司
        $scope.change = function () {
            //console.log($scope.query);
            $http.get('/fuzzy_query?query=' + $scope.query).success(function (msg) {
                //console.log(msg);
                if (msg.query === $scope.query) {
                    if(msg.name.length>100){
                        $scope.names=msg.name.splice(0,100);
                        return;
                    }
                    $scope.names = msg.name;
                }
            });
        };

        //选择公司
        $scope.select = function ($event) { //$event 为angular的事件传输，angular负责处理兼容性，而不需要写e = e||window.event
            var e = $event.target;
            text = $(e).text();
            //console.log(text);

            $scope.query = ""; //清空输入框
            $scope.companyName = text;
            $scope.names = [];
            changeCompany(); //切换公司
        };
        $scope.prev = function ($event) {
            //日期条前一次响应事件
            if (parseInt($("#7dayUl").css("left"), 10) < 0) {
                $("#7dayUl").css("left", "+=86");
            }
            if (parseInt($("#7dayUl").css("left"), 10) >= 0) {
                $($event.target.parentElement).addClass("dis-gray");
            } else {
                $($event.target.parentElement).removeClass("dis-gray");
            }
            if (parseInt($("#7dayUl").css("left"), 10) <= $scope.timelineLength) {
                $("#7dayNext").addClass("dis-gray");
            } else {
                $("#7dayNext").removeClass("dis-gray");
            }
        };

        $scope.appe = function ($event) {
            //日期条后一次响应事件
            if (parseInt($("#7dayUl").css("left"), 10) > $scope.timelineLength) {
                $("#7dayUl").css("left", "-=86");
            }
            if (parseInt($("#7dayUl").css("left"), 10) <= $scope.timelineLength) {
                $($event.target.parentElement).addClass("dis-gray");
            } else {
                $($event.target.parentElement).removeClass("dis-gray");
            }
            if (parseInt($("#7dayUl").css("left"), 10) >= 0) {
                $("#7dayPrev").addClass("dis-gray");
            } else {
                $("#7dayPrev").removeClass("dis-gray");
            }

        };


        //是否显示搜索结果的框
        $scope.searchShow = function () {
            return $scope.names.length !== 0;
        };

        //显示摘要以及主权项的按钮响应函数
        $scope.toggler = function ($event, divID) {
            if ($($event.target).hasClass("glyphicon-plus")) {
                $event.target.className = "glyphicon glyphicon-minus";
            } else {
                $event.target.className = "glyphicon glyphicon-plus";
            }

            $("#" + divID).toggle(); //内容框toggle
        };

        //专利信息变量的初始化
        $scope.bigCurrentPage = 1; //目前分页所在页码
        $scope.bigTotalItems = 0; //总条目数
        $scope.record_id = 0; //当前选择日期条


        //
        $scope.setPage = function (pageNo) {
            $scope.currentPage = pageNo; //选择页码
        };

        // 换页
        $scope.pageChanged = function () {
            $http.post('/get_record_detail/' + $scope.record_id, {page: $scope.bigCurrentPage}).success(function (msg) {
                console.log(msg);
                $scope.patents = msg.patents;
            })
        };
        $scope.maxSize = 5; //页码条个数最大为5个

        //切换公司
        var changeCompany = function () {
            $scope.timestamps = [];
            $scope.bigTotalItems = 0;
            $scope.patents = [];
            $http.get('get_company/' + $scope.companyName).success(function (msg) {

                if (msg.length === 0) {
                    alert("无此公司数据");
                    return;
                }
                $scope.record_id = msg[msg.length - 1].id; //设置为最近的爬虫结果
                $scope.timestamps = msg;
                if ($scope.timestamps.length > 7) {
                    $scope.timelineLength = -1 * ($scope.timestamps.length - 7) * 86;
                    $scope.lendd = $scope.timelineLength + "px";
                } else {
                    $scope.timelineLength = 0;
                    $scope.lendd = $scope.timelineLength + "px";
                }


                $scope.timestampChange(undefined, $scope.record_id);//切换
                $(".timeline").last().addClass("on"); //加上选中得效果
            })
        };
        changeCompany();
        getRecordDetail = function (id) {
            $http.get('/get_record_detail/' + id).success(function (msg) {
                console.log(msg);
                $scope.bigTotalItems = msg.patentCount;
                $scope.patents = msg.patents;
            })
        }
        $scope.timestampChange = function ($event, id) {
            $(".timeline").removeClass("on");
            $scope.record_id = id;
            if ($event)
                $($event.target).addClass("on");
            getRecordDetail(id);
        }
        $scope.del_patent = function () {

            $http.get('/del_patent/'+$scope.companyName).success(function (msg){
                console.log(msg)
                if (msg == "SUCCESS") {
                    alert("清除数据成功")
                    $("#deleteModal").modal('hide')
                    changeCompany();

                }
            })
        }
    }).controller('HistoryController', function ($scope, $http) {
        //历史信息变量的初始化
        $scope.currentPage = 1; //目前分页所在页码
        $scope.totalItems = 0; //总条目数
        $scope.record_id = 0; //当前选择日期条
        $scope.maxSize = 5;
        $scope.histories = [];
       var getHistoryDetail = function () {
            $http.get('/get_history_detail/',{page:$scope.currentPage}).success(function (msg) {
                console.log(msg);
                $scope.totalItems = msg.historiesCount;
                $scope.histories = msg.histories;
            })
        };
        getHistoryDetail()

        $scope.setPage = function (pageNo) {
            $scope.currentPage = pageNo; //选择页码
        };

        // 换页
        $scope.historyPageChanged = function () {
            $http.post('/get_history_detail/', {page: $scope.currentPage}).success(function (msg) {
                console.log(msg);
                $scope.histories = msg.histories;
            })
        };
    });

