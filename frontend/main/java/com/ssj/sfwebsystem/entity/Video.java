package com.ssj.sfwebsystem.entity;

import com.fasterxml.jackson.annotation.JsonFormat;

import java.util.Date;

public class Video {
    private Long videoId;           // 视频id
    private String videoPath;       // 视频路径
    private String coverImgPath;    // 封面路径
    private String videoName;       // 视频名称
    private String videoFeaturePath;// 视频存储特征的路径
    private Double frameCount;      // 视频的帧数
    private String frameListPath;   // 视频帧索引列表的路径
    private Date uploadTime;        // 上传时间
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
    private Date shootStartTime;    // 视频拍摄开始时间
    private Double duration;       // 视频时长
    private String uploaderId;      // 上传员工的id
    private Integer msgStatus;      // 视频信息状态，0表示信息完整，1表示信息残缺

    public Video() {
    }

    public Video(Long videoId, String videoPath, String coverImgPath, String videoName, String videoFeaturePath, Double frameCount, String frameListPath, Date uploadTime, Date shootStartTime, Double duration, String uploaderId, Integer msgStatus) {
        this.videoId = videoId;
        this.videoPath = videoPath;
        this.coverImgPath = coverImgPath;
        this.videoName = videoName;
        this.videoFeaturePath = videoFeaturePath;
        this.frameCount = frameCount;
        this.frameListPath = frameListPath;
        this.uploadTime = uploadTime;
        this.shootStartTime = shootStartTime;
        this.duration = duration;
        this.uploaderId = uploaderId;
        this.msgStatus = msgStatus;
    }

    public Long getVideoId() {
        return videoId;
    }

    public void setVideoId(Long videoId) {
        this.videoId = videoId;
    }

    public String getVideoPath() {
        return videoPath;
    }

    public void setVideoPath(String videoPath) {
        this.videoPath = videoPath;
    }

    public String getCoverImgPath() {
        return coverImgPath;
    }

    public void setCoverImgPath(String coverImgPath) {
        this.coverImgPath = coverImgPath;
    }

    public String getVideoName() {
        return videoName;
    }

    public void setVideoName(String videoName) {
        this.videoName = videoName;
    }

    public String getVideoFeaturePath() {
        return videoFeaturePath;
    }

    public void setVideoFeaturePath(String videoFeaturePath) {
        this.videoFeaturePath = videoFeaturePath;
    }

    public Double getFrameCount() {
        return frameCount;
    }

    public void setFrameCount(Double frameCount) {
        this.frameCount = frameCount;
    }

    public String getFrameListPath() {
        return frameListPath;
    }

    public void setFrameListPath(String frameListPath) {
        this.frameListPath = frameListPath;
    }

    public Date getUploadTime() {
        return uploadTime;
    }

    public void setUploadTime(Date uploadTime) {
        this.uploadTime = uploadTime;
    }

    public Date getShootStartTime() {
        return shootStartTime;
    }

    public void setShootStartTime(Date shootStartTime) {
        this.shootStartTime = shootStartTime;
    }

    public Double getDuration() {
        return duration;
    }

    public void setDuration(Double duration) {
        this.duration = duration;
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
        return "Video{" +
                "videoId=" + videoId +
                ", videoPath='" + videoPath + '\'' +
                ", coverImgPath='" + coverImgPath + '\'' +
                ", videoName='" + videoName + '\'' +
                ", videoFeaturePath='" + videoFeaturePath + '\'' +
                ", frameCount=" + frameCount +
                ", frameListPath='" + frameListPath + '\'' +
                ", uploadTime=" + uploadTime +
                ", shootStartTime=" + shootStartTime +
                ", duration=" + duration +
                ", uploaderId='" + uploaderId + '\'' +
                ", msgStatus=" + msgStatus +
                '}';
    }
}
