package com.ssj.sfwebsystem.entity;

import com.fasterxml.jackson.annotation.JsonFormat;

import java.util.Date;

// 文件汇总表
public class FileEntity {
    private Long fileId;            // 文件表主键
    private String fileName;        // 文件名称
    private String filePath;        // 文件路径
    private String uploaderWorkId;  // 上传者工号
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
    private Date createTime;        // 上传时间
    private String fileType;        // 文件类型
    private String fileSize;        // 文件大小
    private String comment;         // 备注，delete表示删除状态

    public FileEntity() {
    }

    public FileEntity(Long fileId, String fileName, String filePath, String uploaderWorkId, Date createTime, String fileType, String fileSize, String comment) {
        this.fileId = fileId;
        this.fileName = fileName;
        this.filePath = filePath;
        this.uploaderWorkId = uploaderWorkId;
        this.createTime = createTime;
        this.fileType = fileType;
        this.fileSize = fileSize;
        this.comment = comment;
    }

    public Long getFileId() {
        return fileId;
    }

    public void setFileId(Long fileId) {
        this.fileId = fileId;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public String getFilePath() {
        return filePath;
    }

    public void setFilePath(String filePath) {
        this.filePath = filePath;
    }

    public String getUploaderWorkId() {
        return uploaderWorkId;
    }

    public void setUploaderWorkId(String uploaderWorkId) {
        this.uploaderWorkId = uploaderWorkId;
    }

    public Date getCreateTime() {
        return createTime;
    }

    public void setCreateTime(Date createTime) {
        this.createTime = createTime;
    }

    public String getFileType() {
        return fileType;
    }

    public void setFileType(String fileType) {
        this.fileType = fileType;
    }

    public String getFileSize() {
        return fileSize;
    }

    public void setFileSize(String fileSize) {
        this.fileSize = fileSize;
    }

    public String getComment() {
        return comment;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }

    @Override
    public String toString() {
        return "FileEntity{" +
                "fileId=" + fileId +
                ", fileName='" + fileName + '\'' +
                ", filePath='" + filePath + '\'' +
                ", uploaderWorkId='" + uploaderWorkId + '\'' +
                ", createTime=" + createTime +
                ", fileType='" + fileType + '\'' +
                ", fileSize='" + fileSize + '\'' +
                ", comment='" + comment + '\'' +
                '}';
    }
}
