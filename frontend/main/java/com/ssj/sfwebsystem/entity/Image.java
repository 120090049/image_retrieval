package com.ssj.sfwebsystem.entity;

import com.fasterxml.jackson.annotation.JsonFormat;

import java.util.Date;

public class Image {
    private Long imageId;           // 图片id
    private String imagePath;       // 图片路径
    private String imageName;       // 图片名称
    private Date uploadTime;        // 上传时间
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
    private Date shootTime;         // 拍摄时间
    private String workerId;        // 拍摄时工作员工的id
    private String uploaderId;      // 上传图片的员工id
    private Integer msgStatus;      // 图片信息状态，0表示信息完整，1表示信息残缺，2表示已删除的信息

    public Image() {
    }

    public Image(Long imageId, String imagePath, String imageName, Date uploadTime, Date shootTime, String workerId, String uploaderId, Integer msgStatus) {
        this.imageId = imageId;
        this.imagePath = imagePath;
        this.imageName = imageName;
        this.uploadTime = uploadTime;
        this.shootTime = shootTime;
        this.workerId = workerId;
        this.uploaderId = uploaderId;
        this.msgStatus = msgStatus;
    }

    public Long getImageId() {
        return imageId;
    }

    public void setImageId(Long imageId) {
        this.imageId = imageId;
    }

    public String getImagePath() {
        return imagePath;
    }

    public void setImagePath(String imagePath) {
        this.imagePath = imagePath;
    }

    public String getImageName() {
        return imageName;
    }

    public void setImageName(String imageName) {
        this.imageName = imageName;
    }

    public Date getUploadTime() {
        return uploadTime;
    }

    public void setUploadTime(Date uploadTime) {
        this.uploadTime = uploadTime;
    }

    public Date getShootTime() {
        return shootTime;
    }

    public void setShootTime(Date shootTime) {
        this.shootTime = shootTime;
    }

    public String getWorkerId() {
        return workerId;
    }

    public void setWorkerId(String workerId) {
        this.workerId = workerId;
    }

    public String getUploaderId() {
        return uploaderId;
    }

    public void setUploaderId(String uploaderId) {
        this.uploaderId = uploaderId;
    }

    public Integer getMsgStatus() {
        return msgStatus;
    }

    public void setMsgStatus(Integer msgStatus) {
        this.msgStatus = msgStatus;
    }

    @Override
    public String toString() {
        return "Image{" +
                "imageId=" + imageId +
                ", imagePath='" + imagePath + '\'' +
                ", imageName='" + imageName + '\'' +
                ", uploadTime=" + uploadTime +
                ", shootTime=" + shootTime +
                ", workerId='" + workerId + '\'' +
                ", uploaderId='" + uploaderId + '\'' +
                ", msgStatus=" + msgStatus +
                '}';
    }
}
