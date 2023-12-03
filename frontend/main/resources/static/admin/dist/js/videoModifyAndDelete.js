$(function () {
    $("#jqGrid").jqGrid({
        url: '/admin/videoList/list',
        datatype: "json",
        colModel: [
            {label: 'id', name: 'videoId', index: 'videoId', width: 50, key: true, hidden: true},
            {label: '视频名称', name: 'videoName', index: 'videoName', width: 200},
            {label: '时长(s)', name: 'duration', index: 'duration', width: 80},
            {label: '拍摄时间', name: 'shootStartTime', index: 'shootStartTime', width: 200}
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
    var videoId = $("#videoId").val();
    var shootTime = $("#shootStartTime").val();
    var videoName = $("#videoName").val();
    if (isNull(shootTime)) {
        $('#edit-error-msg').css("display", "block");
        $('#edit-error-msg').html("拍摄时间不能为空！");
        return;
    }
    if (isNull(videoName)) {
        $('#edit-error-msg').css("display", "block");
        $('#edit-error-msg').html("视频名称不能为空！");
        return;
    }
    var params = $("#categoryForm").serialize();
    url = '/admin/video/updateForManger';

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

function videoEdit() {
    var id = getSelectedRow();
    if (id == null) {
        return;
    }
    reset();
    //请求数据
    $.get("/admin/video/info/" + id, function (r) {
        if (r.resultCode == 200 && r.data != null) {
            //填充数据至modal
            $("#videoName").val(r.data.videoName);
            $("#shootStartTime").val(r.data.shootStartTime);
        }
    });

    $('.modal-title').html('视频编辑');
    $('#categoryModal').modal('show');
    $("#videoId").val(id);
}

function deleteVideo() {
    var id = getSelectedRow();
    if (id == null) {
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
                    url: "/admin/video/delete",
                    contentType: "application/json",
                    data: JSON.stringify(id),
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
    $("#categoryName").val('');
    $("#categoryIcon option:first").prop("selected", 'selected');
}