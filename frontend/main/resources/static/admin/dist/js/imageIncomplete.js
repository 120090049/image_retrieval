$(function () {
    $("#jqGrid").jqGrid({
        url: '/admin/imageIncomplete/list',
        datatype: "json",
        colModel: [
            {label: 'id', name: 'imageId', index: 'imageId', width: 50, key: true, hidden: true},
            {label: '图片名称', name: 'imageName', index: 'imageName', width: 120},
            {label: '预览图', name: 'imagePath', index: 'imagePath', width: 120, formatter: coverImageFormatter},
            {label: '拍摄时间', name: 'shootTime', index: 'shootTime', width: 120}
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

    function coverImageFormatter(cellvalue) {
        return "<img src='" + cellvalue + "' height=\"20%\" width=\"20%\" alt='coverImage'/>";
    }
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
    var imageId = $("#imageId").val();
    var shootTime = $("#shootTime").val();
    var imageName = $("#imageName").val();
    // console.log(shootTime);
    if (isNull(shootTime)) {
        $('#edit-error-msg').css("display", "block");
        $('#edit-error-msg').html("拍摄时间不能为空！");
        return;
    }
    if (isNull(imageName)) {
        $('#edit-error-msg').css("display", "block");
        $('#edit-error-msg').html("图像名称不能为空！");
        return;
    }
    var params = $("#linkForm").serialize();
    url = '/admin/image/update';

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
function shootTimeEdit() {
    var id = getSelectedRow();
    if (id == null) {
        return;
    }
    reset();
    //请求数据
    $.get("/admin/image/info/" + id, function (r) {
        if (r.resultCode == 200 && r.data != null) {
            //填充数据至modal
            $("#imageName").val(r.data.imageName);
            $("#shootTime").val(r.data.shootTime);
        }
    });
    $('.modal-title').html('修改时间');
    $('#linkModal').modal('show');
    $("#imageId").val(id);
}

function reset() {
    $("#imageName").val('');
    $("#shootTime").val('');
    $('#edit-error-msg').css("display", "none");
}
