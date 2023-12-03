$(function () {
    $("#jqGrid").jqGrid({
        url: '/admin/imageList/list',
        datatype: "json",
        colModel: [
            {label: '装配', name: 'imagePath1', index: 'imagePath1', width: 200, formatter: coverImageFormatter, align: 'center'},
            {label: '场景', name: 'imagePath2', index: 'imagePath2', width: 200, formatter: coverImageFormatter, align: 'center'},
            {label: '图像', name: 'imagePath3', index: 'imagePath3', width: 200, formatter: coverImageFormatter, align: 'center'},
            {label: '预览', name: 'imagePath4', index: 'imagePath4', width: 200, formatter: coverImageFormatter, align: 'center'}
        ],
        height: "100%",
        rowNum: 12,
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
        if(cellvalue != null && cellvalue.length > 0){
            return "<img src='" + cellvalue + "' height=\"160px\" alt='coverImage'/>";
        }else{
            return "<img src='...' onerror='this.src=\"/admin/dist/img/172-180.png\"; this.onerror=\"null\"'>";
        }
    }
});
