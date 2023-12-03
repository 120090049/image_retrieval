$(function () {
    $("#jqGrid").jqGrid({
        url: '/admin/fileSearch/list',
        datatype: "json",
        colModel: [
            {label: 'id', name: 'fileId', index: 'fileId', width: 50, key: true, hidden: true},
            {label: '文件名', name: 'fileName', index: 'fileName', width: 140},
            {label: '上传者工号', name: 'uploaderWorkId', index: 'uploaderWorkId', width: 60},
            {label: '文件大小', name: 'fileSize', index: 'fileSize', width: 60},
            {label: '添加时间', name: 'createTime', index: 'createTime', width: 90}
        ],
        height: "100%",
        rowNum: 10,
        rowList: [10, 20, 50],
        styleUI: 'Bootstrap',
        loadtext: '信息读取中...',
        rownumbers: false,
        rownumWidth: 20,
        autowidth: true,
        multiselect: true,
        pager: "#jqGridPager",
        jsonReader: {
            root: "data.list",
            page: "data.currPage",
            total: "data.totalPage",
            records: "data.totalCount"
        },
        prmNames: {
            page: "page",
            rows: "limit",
            order: "order",
        },
        gridComplete: function () {
            //隐藏grid底部滚动条
            $("#jqGrid").closest(".ui-jqgrid-bdiv").css({"overflow-x": "hidden"});
        }
    });

    $(window).resize(function () {
        $("#jqGrid").setGridWidth($(".card-body").width());
    });
});

/**
 * 搜索功能
 */
function search() {
    //标题关键字
    var fileName = $('#fileName').val();
    var uploadId = $('#uploaderId').val();
    var startTime = $('#test-startDate-1').val();
    var endTime = $('#test-endDate-1').val();
    if (!validLength(fileName, 100)) {
        swal("搜索字段长度过大!", {
            icon: "error",
        });
        return false;
    }
    if (!validLength(uploadId, 50)) {
        swal("搜索字段长度过大!", {
            icon: "error",
        });
        return false;
    }
    //数据封装
    var searchData = {fileName: fileName, uploadId: uploadId, startTime: startTime, endTime: endTime};
    //传入查询条件参数
    $("#jqGrid").jqGrid("setGridParam", {postData: searchData});
    //点击搜索按钮默认都从第一页开始
    $("#jqGrid").jqGrid("setGridParam", {page: 1});
    //提交post并刷新表格
    $("#jqGrid").jqGrid("setGridParam", {url: '/admin/fileSearch/list'}).trigger("reloadGrid");
}

/**
 * jqGrid重新加载
 */
function reload() {
    var page = $("#jqGrid").jqGrid('getGridParam', 'page');
    $("#jqGrid").jqGrid('setGridParam', {
        page: page
    }).trigger("reloadGrid");
}

//绑定modal上的保存按钮
$('#saveButton').click(function () {
    var fileId = $("#fileId").val();
    var fileName = $("#fileNameForUpdate").val();
    if (isNull(fileName)) {
        $('#edit-error-msg').css("display", "block");
        $('#edit-error-msg').html("文件名称不能为空！");
        return;
    }
    var params = $("#categoryForm").serialize();
    url = '/admin/file/update';

    $.ajax({
        type: 'POST',//方法类型
        url: url,
        data: params,
        success: function (result) {
            if (result.resultCode == 200 && result.data) {
                $('#categoryModal').modal('hide');
                swal("保存成功", {
                    icon: "success",
                });
                reload();
            }
            else {
                $('#categoryModal').modal('hide');
                swal("保存失败", {
                    icon: "error",
                });
            }
        },
        error: function () {
            swal("操作失败", {
                icon: "error",
            });
        }
    });
});

function openFile() {
    var id = getSelectedRow();
    if (id == null) {
        return;
    }
    window.open("/admin/files/open/" + id);
}
function fileEdit(){
    var id = getSelectedRow();
    if (id == null) {
        return;
    }
    reset();
    //请求数据
    $.get("/admin/file/info/" + id, function (r) {
        if (r.resultCode == 200 && r.data != null) {
            //填充数据至modal
            $("#fileNameForUpdate").val(r.data.fileName);
        }
    });

    $('.modal-title').html('文件编辑');
    $('#categoryModal').modal('show');
    $("#fileId").val(id);
}

function deleteFile() {
    var ids = getSelectedRows();
    if (ids == null) {
        return;
    }
    swal({
        title: "确认弹框",
        text: "确认要删除数据吗?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    }).then((flag) => {
            if (flag) {
                $.ajax({
                    type: "POST",
                    url: "/admin/files/delete",
                    contentType: "application/json",
                    data: JSON.stringify(ids),
                    success: function (r) {
                        if (r.resultCode == 200) {
                            swal("删除成功", {
                                icon: "success",
                            });
                            $("#jqGrid").trigger("reloadGrid");
                        } else {
                            swal(r.message, {
                                icon: "error",
                            });
                        }
                    }
                });
            }
        }
    );
}

function reset() {
    $("#fileNameForUpdate").val('');
    $("#categoryIcon option:first").prop("selected", 'selected');
}