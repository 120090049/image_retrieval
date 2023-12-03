package com.ssj.sfwebsystem.controller.vo;

import com.fasterxml.jackson.annotation.JsonFormat;

import java.util.Date;

public class VideoListVO {
    private Long videoId;           // 视频id
    private String videoPath;       // 视频路径
    private String videoName;       // 视频名称
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
    private Date shootStartTime;    // 视频拍摄开始时间
    private Double duration;       // 视频时长

    public VideoListVO() {
    }

    public VideoListVO(Long videoId, String videoPath, String videoName, Date shootStartTime, Double duration) {
        this.videoId = videoId;
        this.videoPath = videoPath;
        this.videoName = videoName;
        this.shootStartTime = shootStartTime;
        this.duration = duration;
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

    public String getVideoName() {
        return videoName;
    }

    public void setVideoName(String videoName) {
        this.videoName = videoName;
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
}
