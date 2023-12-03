$(function () {
    $("#jqGrid").jqGrid({
        url: '/admin/videoList/list',
        datatype: "json",
        colModel: [
            {label: 'id', name: 'fileId', index: 'fileId', width: 50, key: true, hidden: true},
            {label: '文件名称', name: 'fileName', index: 'fileName', width: 120, },
            {label: '文件大小(kb)', name: 'fileSize', index: 'fileSize', width: 120},
            {label: '上传时间', name: 'createTime', index: 'createTime', width: 80}
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

function lookUpFile() {
    var id = getSelectedRow();
    if (id == null) {
        return;
    }
    // 发送请求
    $.get("/admin/file/lookUp/" + id, function () {
        console.log("页面跳转");
    });
}
