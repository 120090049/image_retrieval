package com.ssj.sfwebsystem.dao;


import com.ssj.sfwebsystem.entity.FileEntity;
import com.ssj.sfwebsystem.util.PageQueryUtil;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface FileEntityMapper {
    // 新增文件信息
    int insert(FileEntity fileEntity);

    // 修改文件信息根据主键
    int updateById(FileEntity fileEntity);

    // 查找所有文件信息
    List<FileEntity> selectAll(PageQueryUtil pageUtil);

    // 删除文件信息
    int deleteById(Long fileId);

    // 判断是否删除
    FileEntity selectByIdIfDelete(Long fileId);

    int getTotalFiles(PageQueryUtil pageQueryUtil);

    FileEntity selectById(@Param("fileId") Long fileId);

    // 批量删除
    int deleteBatch(Long[] ids);

    int getTotalCount();
}
