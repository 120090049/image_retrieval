package com.ssj.sfwebsystem.dao;

import com.ssj.sfwebsystem.entity.Image;
import com.ssj.sfwebsystem.util.PageQueryUtil;

import java.util.List;

public interface ImageRetrievalMapper {
    // 批量插入图片部分信息
    int insertSelective(Image image);

    // 通过图片名称查询所有图片信息
    Image selectImageByImageName(String imageName);

    // 根据信息状态修改图片信息
    int updateByMsgStatus(Image image);

    // 根据主键删除图片
    int deleteByPrimaryKey(Long imageId);

    // 批量删除
    int deleteBatch(Long[] ids);

    // 查找不完整的图片信息
    List<Image> selectIncompleteImages(PageQueryUtil pageUtil);

    Image selectImageById(Long imageId);

    int updateById(Image image);

    // 统计当前所有图片数量
    int getTotalCount();

    List<Image> selectImageList(PageQueryUtil queryUtil);

    int selectCountById(Long id);
}
