$(function () {
    var pqFilter = {
        search: function () {
            var txt = $("input.pq-filter-txt").val().toUpperCase(),
                colIndx = $("select#pq-filter-select-column").val(),
                DM = $grid.pqGrid("option", "dataModel");
            DM.filterIndx = colIndx;
            DM.filterValue = txt;
            $grid.pqGrid("refreshDataAndView");
        }, render: function (ui) {
            var DM = ui.dataModel, rowData = ui.rowData, dataIndx = ui.dataIndx,
                val = rowData[dataIndx], txt = DM.filterValue;
            if (txt != null) {
                txtUpper = txt.toUpperCase(), valUpper = val;
            }
            if (dataIndx == DM.filterIndx) {
                var indx = valUpper.indexOf(txtUpper);
                if (indx >= 0) {
                    var txt1 = val.substring(0, indx);
                    var txt2 = val.substring(indx, indx + txt.length);
                    var txt3 = val.substring(indx + txt.length);
                    return txt1 + "<span style='background:yellow;color:#333;'>" + txt2 + "</span>" + txt3;
                }
            }
            return val;
        }
    }

    var colModel = [{
        title: "序号",
        width: 100,
        dataType: "integer",
        dataIndx: "id",
        hidden: false,
        editable: false,
        render: function (ui) {
            return pqFilter.render(ui);
        }
    },
        {
            title: "名称",
            width: 200,
            dataType: "string",
            dataIndx: "name",
            editable: false,
            render: function (ui) {
                return pqFilter.render(ui);
            }
        },
        {
            title: "表达式",
            width: 900,
            height: 100,
            dataType: "string",
            align: "left",
            dataIndx: "content",
            editable: false,
            render: function (ui) {
                return pqFilter.render(ui);
            }
        }
    ];
    var dataModel = {
        location: "remote",
        sorting: "remote",
        paging: "remote",
        dataType: "JSON",
        method: "GET",
        curPage: 1,
        rPP: 10,
        rPPOptions: [1, 10, 20, 30, 40, 50, 100, 500, 1000],
        fields: ['id', 'name'],
        getUrl: function () {
            var queryString = "cur_page=" + this.curPage + "&records_per_page=" + this.rPP;

            if (this.filterIndx != null && this.fields[this.filterIndx]) {

                queryString += "&filterBy=" + this.fields[this.filterIndx] + "&filterValue=" + this.filterValue;
            }
            var obj = {
                url: "/get_expression",
                data: queryString
            };
            return obj;
        },
        getData: function (dataJSON) {
            //var data
            console.log(dataJSON)
            return {curPage: dataJSON.curPage, totalRecords: dataJSON.totalRecords, data: dataJSON.data};
        }

    };
    var obj = {
        dataModel: dataModel,
        colModel: colModel,
        width: 960,
        height: 600,
        title: "专利信息检索表达式管理",
        editModel: {clickToEdit: 2},
        selectionModel: {mode: 'single'}
    };

    obj.render = function (evt, obj) {
        var $toolbar = $("<div class='pq-grid-toolbar pq-grid-toolbar-search'></div>").appendTo($(".pq-grid-top", this));
        $("<span>Filter</span>").appendTo($toolbar);
        $("<input type='text' class='pq-filter-txt'/>").appendTo($toolbar).keyup(function (evt) {
            if (evt.keyCode == 13) {
                pqFilter.search();
            }
        });
        $("<select id='pq-filter-select-column'>\
            <option value='0'>序号</option>\
            <option value='1'>名称</option>\
            </select>").appendTo($toolbar).change(function () {
            pqFilter.search();
        });
        $("<span class='pq-separator'></span>").appendTo($toolbar);

                //var $toolbar = $("<div class='pq-grid-toolbar pq-grid-toolbar-crud'></div>").appendTo($(".pq-grid-top", this));

        $("<span>新增</span>").appendTo($toolbar).button({
            icons: {
                primary: "ui-icon-circle-plus"
            }
        }).click(function (evt) {
            addRow();
        });
        $("<span>修改</span>").appendTo($toolbar).button({
            icons: {
                primary: "ui-icon-pencil"
            }
        }).click(function (evt) {
            editRow();
        });
        $("<span>删除</span>").appendTo($toolbar).button({
            icons: {
                primary: "ui-icon-circle-minus"
            }
        }).click(function () {
            deleteRow();
        });
        $toolbar.disableSelection();
    };


    var $grid = $("#grid_array").pqGrid(obj);


    /*
     --------------------------------------------------------------------------------------------------------------------
     */
    function editRow() {
        var rowIndx = getRowIndx();
        if (rowIndx != null) {
            var DM = $grid.pqGrid("option", "dataModel");
            var data = DM.data;
            var row = data[rowIndx];
            var $frm = $("form#crud-form");
            $frm.find("input[name='name']").val(row['name']);
            $frm.find("textarea").val(row['content']);

            $("#popup-dialog-crud").dialog({
                title: "修改表达式 (" + (rowIndx + 1) + ")",
                buttons: {
                    更新: function () {
                        //save the record in DM.data.
                        var that = this;
                        row['name'] = $frm.find("input[name='name']").val();
                        row['content'] = $frm.find("textarea").val();
                        //$grid.pqGrid("refreshDataAndView").pqGrid('setSelection',{ rowIndx:rowIndx});
                        $grid.pqGrid("refreshRow", {
                            rowIndx: rowIndx
                        }).pqGrid('setSelection', {
                            rowIndx: rowIndx
                        });
                        $.post('/update_expression', row, function (res) {
                            res = JSON.parse(res);
                            if (res.state === "SUCCESS") {
                                alert("更新成功");
                            }
                            $(that).dialog("close");
                        });
                    },
                    取消: function () {
                        $(this).dialog("close");
                    }
                }
            }).dialog("open");
        }
    }

//append Row
    function addRow() {
        //debugger;
        var DM = $grid.pqGrid("option", "dataModel");
        var data = DM.data;

        var $frm = $("form#crud-form");
        $frm.find("input").val("");
        $frm.find("textarea").val("");
        $("#popup-dialog-crud").dialog({
            title: "添加一条表达式",
            buttons: {
                增加: function () {
                    var that = this;
                    var row = $.extend({}, data[2]);
                    //        save the record in DM.data.
                    var name = $frm.find("input[name='name']").val();
                    row.name = name;
                    var content = $frm.find("textarea").val();
                    row.content = content;
                    $.post('/add_expression', {name: name, content: content}, function (res) {
                        res = JSON.parse(res);
                        if (res.state === "SUCCESS") {
                            alert("添加成功");
                            row.id = res.id;
                            data.push(row);
                            $grid.pqGrid("refreshDataAndView");
                            $(that).dialog("close");
                        }
                    })

                },
                Cancel: function () {
                    $(this).dialog("close");
                }
            }
        });
        $("#popup-dialog-crud").dialog("open");
    }

//delete Row.
    function deleteRow() {
        var rowIndx = getRowIndx();

        if (rowIndx != null) {
            var DM = $grid.pqGrid("option", "dataModel");
            row = DM.data[rowIndx];
            DM.data.splice(rowIndx, 1);
            $grid.pqGrid("refreshDataAndView");
            $grid.pqGrid("setSelection", {
                rowIndx: rowIndx
            });
            $.post('/del_expression', {id: row['id']}, function (res) {
               // res = JSON.parse(res);
                console.log(res)
                if (res == "SUCCESS") {
                    alert("删除成功");
                    $grid.pqGrid("refreshDataAndView");
                }
            })
        }
    }

    function getRowIndx() {
        //var $grid = $("#grid_render_cells");

        //var obj = $grid.pqGrid("getSelection");
        //debugger;
        var arr = $grid.pqGrid("selection", {
            type: 'row',
            method: 'getSelection'
        });
        if (arr && arr.length > 0) {
            var rowIndx = arr[0].rowIndx;
             var DM = $grid.pqGrid("option", "dataModel");
            rowIndx -=  (DM.curPage-1)*DM.rPP
            //console.log(rowIndx)
            //if (rowIndx != null && colIndx == null) {
            return rowIndx;
        } else {
            alert("请先选择一行");
            return null;
        }
    }


});