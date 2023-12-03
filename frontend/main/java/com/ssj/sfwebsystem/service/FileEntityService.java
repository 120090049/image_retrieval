package com.ssj.sfwebsystem.service;


import com.ssj.sfwebsystem.entity.FileEntity;
import com.ssj.sfwebsystem.util.PageQueryUtil;
import com.ssj.sfwebsystem.util.PageResult;

// 跟文件相关的service
public interface FileEntityService {
    // 保存一个文件
    int saveFile(FileEntity fileEntity);

    // 获取文件分页对象
    PageResult getFilePage(PageQueryUtil pageQueryUtil);

    // 根据文件id查找文件
    FileEntity getFileById(Long fileId);

    boolean deleteBatch(Long[] ids);

    int getTotalFiles();

    FileEntity selectById(Long id);

    Boolean updateFileMessage(FileEntity fileEntity);
}
