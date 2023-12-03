$(function () {
    $("#jqGrid").jqGrid({
        url: '/admin/imageList/modifyAndDelete',
        datatype: "json",
        colModel: [
            {label: 'id', name: 'imageId', index: 'imageId', width: 50, key: true, hidden: true},
            {label: '图像名称', name: 'imageName', index: 'imageName', width: 200},
            {label: '图像预览', name: 'imagePath', index: 'imagePath', width: 240, formatter: coverImageFormatter},
            {label: '拍摄时间', name: 'shootTime', index: 'shootTime', width: 200}
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
        return "<img src='" + cellvalue + "' height=\"40%\" width=\"40%\"/>";
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
    var params = $("#categoryForm").serialize();
    url = '/admin/image/update';

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

function categoryEdit() {
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

    $('.modal-title').html('图像编辑');
    $('#categoryModal').modal('show');
    $("#imageId").val(id);
}

function deleteCagegory() {
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
                    url: "/admin/image/delete",
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