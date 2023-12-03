package com.ssj.sfwebsystem.service;

import com.ssj.sfwebsystem.entity.Image;
import com.ssj.sfwebsystem.util.PageQueryUtil;
import com.ssj.sfwebsystem.util.PageResult;

import java.util.List;

public interface ImageRetrievalService {
    // 图像检索的信息展示
    List<Image> imageRetrievalMessage(String[] imagesName);

    // 批量选择性新增图片信息
    boolean[] insertBatch(List<Image> images);

    int insertImage(Image image);

    // 批量更新不完整图片的信息
    boolean[] updateBatchIncomplete(List<Image> images);

    // 分页查询信息不完整的图片信息
    PageResult getCurrentIncompleteMessage(PageQueryUtil queryUtil);

    // 根据图片id查找图片信息
    Image selectImageById(Long id);

    Boolean updateById(Image image);

    // 返回当前所有图片数量
    int getTotalImages();

    PageResult getCurrentImageList(PageQueryUtil queryUtil);

    boolean deleteBatch(Long[] ids);

    PageResult getCurrentImageListForModifyAndDelete(PageQueryUtil queryUtil);
}
