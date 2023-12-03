package com.ssj.sfwebsystem.service.impl;

import com.ssj.sfwebsystem.dao.FileEntityMapper;
import com.ssj.sfwebsystem.entity.FileEntity;
import com.ssj.sfwebsystem.service.FileEntityService;
import com.ssj.sfwebsystem.util.PageQueryUtil;
import com.ssj.sfwebsystem.util.PageResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.File;
import java.util.List;

@Service
public class FileEntityServiceImpl implements FileEntityService {
    @Autowired
    private FileEntityMapper fileEntityMapper;
    @Override
    public int saveFile(FileEntity fileEntity) {
        return fileEntityMapper.insert(fileEntity);
    }

    @Override
    public PageResult getFilePage(PageQueryUtil pageQueryUtil) {
        List<FileEntity> fileList = fileEntityMapper.selectAll(pageQueryUtil);
        for (FileEntity entity : fileList) {
            entity.setFileSize(entity.getFileSize()+" 字节");
        }
        int total = fileEntityMapper.getTotalFiles(pageQueryUtil);
        return new PageResult(fileList, total, pageQueryUtil.getLimit(), pageQueryUtil.getPage());
    }

    @Override
    public FileEntity getFileById(Long fileId) {
        return fileEntityMapper.selectById(fileId);
    }

    /**
     * 批量删除
     * @param ids
     * @return
     */
    @Override
    public boolean deleteBatch(Long[] ids) {
        int num = fileEntityMapper.deleteBatch(ids);
        for (Long id : ids) {
            FileEntity fileEntity = fileEntityMapper.selectByIdIfDelete(id);
            if(fileEntity!=null){
                File fileDelete = new File(fileEntity.getFilePath());
                if(fileDelete.exists()) // 文件存在就删除
                    fileDelete.delete();
            }
        }
        return num > 0;
    }

    @Override
    public int getTotalFiles() {
        return fileEntityMapper.getTotalCount();
    }

    // 根据主键获取文件详细信息
    @Override
    public FileEntity selectById(Long id) {
        FileEntity fileEntity = fileEntityMapper.selectById(id);
        return fileEntity;
    }

    @Override
    public Boolean updateFileMessage(FileEntity fileEntity) {
        return fileEntityMapper.updateById(fileEntity) > 0;
    }
}
