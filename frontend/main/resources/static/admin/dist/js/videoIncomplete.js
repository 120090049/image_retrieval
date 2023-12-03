$(function () {
    $("#jqGrid").jqGrid({
        url: '/admin/videoIncomplete/list',
        datatype: "json",
        colModel: [
            {label: 'id', name: 'videoId', index: 'videoId', width: 50, key: true, hidden: true},
            {label: '视频名称', name: 'videoName', index: 'videoName', width: 120},
            {label: '时长(秒)', name: 'duration', index: 'duration', width: 120},
            {label: '拍摄时间', name: 'shootStartTime', index: 'shootStartTime', width: 120}
        ],
        height: 560,
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

    // function coverImageFormatter(cellvalue) {
    //     return "<img src='" + cellvalue + "' height=\"20%\" width=\"20%\" alt='coverImage'/>";
    // }
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
    var shootStartTime = $("#shootStartTime").val();
    // console.log(shootTime);
    if (isNull(shootStartTime)) {
        $('#edit-error-msg').css("display", "block");
        $('#edit-error-msg').html("开始拍摄时间不能为空！");
        return;
    }
    var params = $("#linkForm").serialize();
    url = '/admin/video/update';

    $.ajax({
        type: 'POST',//方法类型
        url: url,
        data: params,
        success: function (result) {
            if (result.resultCode == 200 && result.data) {
                $('#linkModal').modal('hide');
                swal("保存成功", {
                    icon: "success",
                });
                reload();
            }
            else {
                $('#linkModal').modal('hide');
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

// 修改时间信息
function shootTimeEditVideo() {
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
    $('.modal-title').html('修改时间');
    $('#linkModal').modal('show');
    $("#videoId").val(id);
}

function reset() {
    $("#videoName").val('');
    $("#shootStartTime").val('');
    $('#edit-error-msg').css("display", "none");
}
