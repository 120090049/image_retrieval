$(function () {
    $("#jqGrid").jqGrid({
        url: '/admin/videoList/list',
        datatype: "json",
        colModel: [
            {label: 'id', name: 'videoId', index: 'videoId', width: 50, key: true, hidden: true},
            {label: '视频地址', name: 'videoPath', index: 'videoPath', hidden: true},
            {label: '视频名称', name: 'videoName', index: 'videoName', width: 120, },
            {label: '拍摄时间', name: 'shootStartTime', index: 'shootStartTime', width: 120},
            {label: '时长(秒)', name: 'duration', index: 'duration', width: 80}
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

function lookUpVideo() {
    var id = getSelectedRow();
    if(id != null){
        location.href = "/admin/videoBroadcast?id=" + id;
    }
}
