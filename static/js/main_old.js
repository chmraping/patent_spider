/**
 * Created by 璐 on 2015/4/13.
 */

;
$(document).ready(function () {
    //load countries using Ajax Call

    var data = [];
    var dtrans = {1: "name", 2: "content"};
    var pqSearch = {
        txt: "",
        rowIndices: [],
        curIndx: null,
        colIndx: 0,
        sortIndx: null,
        sortDir: null,
        results: null,
        prevResult: function () {
            var colIndx = this.colIndx,
                rowIndices = this.rowIndices;
            if (rowIndices.length == 0) {
                this.curIndx = null;
            } else if (this.curIndx == null || this.curIndx == 0) {
                this.curIndx = rowIndices.length - 1;
            } else {
                this.curIndx--;
            }
            this.updateSelection(colIndx);
        },
        nextResult: function () {
            //debugger;
            var rowIndices = this.rowIndices;
            if (rowIndices.length == 0) {
                this.curIndx = null;
            } else if (this.curIndx == null) {
                this.curIndx = 0;
            } else if (this.curIndx < rowIndices.length - 1) {
                this.curIndx++;
            } else {
                this.curIndx = 0;
            }
            this.updateSelection();
        },
        updateSelection: function () {
            var colIndx = this.colIndx,
                curIndx = this.curIndx,
                rowIndices = this.rowIndices;
            if (rowIndices.length > 0) {
                //results.html("Selected " + (curIndx + 1) + " , "+ rowIndx[curIndx] +" of " + rowIndx.length + " matche(s).");
                this.results.html("您选择" + rowIndices.length + "个匹配项中的第" + (curIndx + 1)+"个" );
            } else {
                this.results.html("未有匹配项");
            }
            $grid.pqGrid("setSelection", null);
            //$grid.pqGrid("option", "customData", { foundRowIndices: rowIndices, txt: this.txt, searchColIndx: colIndx });
            //$grid.pqGrid("refreshColumn", { colIndx: colIndx });
            $grid.pqGrid("setSelection", {
                rowIndx: rowIndices[curIndx],
                colIndx: colIndx
            });
        },
        search: function () {
            var txt = $("input.pq-search-txt").val().toUpperCase(),
                colIndx = $("select#pq-crud-select-column").val(),
                DM = $grid.pqGrid("option", "dataModel"),
                sortIndx = DM.sortIndx,
                sortDir = DM.sortDir;
            if (txt == this.txt && colIndx == this.colIndx && sortIndx == this.sortIndx && sortDir == this.sortDir) {
                return;
            }
            this.rowIndices = [], this.curIndx = null;
            this.sortIndx = sortIndx;
            this.sortDir = sortDir;
            if (colIndx != this.colIndx) {
                //clean the prev column.
                //$grid.pqGrid("option", "customData", { foundRowIndices: [], txt: "", searchColIndx: colIndx });
                $grid.pqGrid("option", "customData", null);
                $grid.pqGrid("refreshColumn", {
                    colIndx: this.colIndx
                });
                this.colIndx = colIndx;
            }
            //debugger;

            if (txt != null && txt.length > 0) {
                txt = txt.toUpperCase();
                //this.colIndx = $("select#pq-crud-select-column").val();

                var data = DM.data;
                //debugger;
                for (var i = 0; i < data.length; i++) {
                    var row = data[i];
                    var cell = row[dtrans[this.colIndx]].toUpperCase();
                    if (cell.indexOf(txt) != -1) {
                        this.rowIndices.push(i);
                    }
                }
            }
            $grid.pqGrid("option", "customData", {
                foundRowIndices: this.rowIndices,
                txt: txt,
                searchColIndx: colIndx
            });
            $grid.pqGrid("refreshColumn", {
                colIndx: colIndx
            });
            this.txt = txt;
        },
        render: function (ui) {
            var rowIndxPage = ui.rowIndxPage,
                rowIndx = ui.rowIndx,
            //data = ui.dataModel.data,
                rowData = ui.rowData,
                dataIndx = ui.dataIndx,
                colIndx = ui.colIndx,
                val = rowData[dataIndx];
            //debugger;
            if (ui.customData) {

                var rowIndices = ui.customData.foundRowIndices,
                    searchColIndx = ui.customData.searchColIndx,
                    txt = ui.customData.txt,
                    txtUpper = txt.toUpperCase(),
                    valUpper = val.toUpperCase();
                if ($.inArray(rowIndx, rowIndices) != -1 && colIndx == searchColIndx) {
                    var indx = valUpper.indexOf(txtUpper);
                    if (indx >= 0) {
                        var txt1 = val.substring(0, indx);
                        var txt2 = val.substring(indx, indx + txt.length);
                        var txt3 = val.substring(indx + txt.length);
                        return txt1 + "<span style='background:yellow;color:#333;'>" + txt2 + "</span>" + txt3;
                    } else {
                        return val;
                    }
                }
            }
            return val;
        }
    };
    $.ajax({
        url: "/get_expression", success: function (response) {
            data = JSON.parse(response);
            var obj = {
                width: 960,
                height: 600,
                title: "专利信息检索表达式管理",
                editModel: {clickToEdit: 2},
                selectionModel: {mode: 'single'}
            };
            obj.colModel = [{
                title: "序号",
                width: 100,
                dataType: "integer",
                dataIndx: "id",
                hidden: false,
                editable: false
            },
                {title: "名称", width: 200, dataType: "string", dataIndx: "name", editable: false},
                {
                    title: "表达式",
                    width: 900,
                    height: 100,
                    dataType: "string",
                    align: "left",
                    dataIndx: "content",
                    editable: false
                }
            ];
            obj.dataModel = {
                data: data,
                location: "local",
                sorting: "local",
                paging: "local",
                curPage: 1,
                rPP: 10,
                sortIndx: "name",
                sortDir: "up",
                rPPOptions: [1, 10, 20, 30, 40, 50, 100, 500, 1000]
            };
            $.extend(obj.colModel[1], {
                width: 200,
                render: function (ui) {
                    return pqSearch.render(ui);
                }
            });
            $.extend(obj.colModel[2], {
                width: 600,
                render: function (ui) {
                    return pqSearch.render(ui);
                }
            });

            $("#grid_array").on("pqgridrender", function (evt, obj) {
                var $toolbar = $("<div class='pq-grid-toolbar pq-grid-toolbar-crud'></div>").appendTo($(".pq-grid-top", this));

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
                var $toolbar = $("<div class='pq-grid-toolbar pq-grid-toolbar-search'></div>").appendTo($(".pq-grid-top", this));

                $("<span>搜索</span>").appendTo($toolbar);

                $("<input type='text' class='pq-search-txt'/>").appendTo($toolbar).keyup(function (evt) {
                    pqSearch.search();
                    if (evt.keyCode == 38) {
                        pqSearch.prevResult();
                    } else {
                        pqSearch.nextResult();
                    }
                });

                $("<select id='pq-crud-select-column'>\
                <option value='1'>名称</option>\
                <option value='2'>表达式</option>\
                </select>").appendTo($toolbar).change(function () {
                    pqSearch.search();
                    pqSearch.nextResult();
                });
                $("<span class='pq-separator'></span>").appendTo($toolbar);

                $("<button title='Previous Result'></button>")
                    .appendTo($toolbar)
                    .button({
                        icons: {
                            primary: "ui-icon-circle-triangle-w"
                        },
                        text: false
                    }).bind("click", function (evt) {
                        pqSearch.prevResult();
                    });
                $("<button title='Next Result'></button>")
                    .appendTo($toolbar)
                    .button({
                        icons: {
                            primary: "ui-icon-circle-triangle-e"
                        },
                        text: false
                    }).bind("click", function (evt) {
                        pqSearch.nextResult();
                    });
                $("<span class='pq-separator'></span>").appendTo($toolbar);

                pqSearch.results = $("<span class='pq-search-results'>未有匹配项</span>").appendTo($toolbar);
            });
            $grid = $("#grid_array").pqGrid(obj);

            $("#popup-dialog-crud").dialog({
                width: 400,
                modal: true,
                open: function () {
                    $(".ui-dialog").position({
                        of: "#grid_crud"
                    });
                },
                autoOpen: false
            });
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
                                    if(res.state === "SUCCESS"){
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
                        res = JSON.parse(res);
                        if (res.state === "SUCCESS") {
                            alert("删除成功");
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

                    //if (rowIndx != null && colIndx == null) {
                    return rowIndx;
                } else {
                    alert("请先选择一行");
                    return null;
                }
            }
        }
    });


})
