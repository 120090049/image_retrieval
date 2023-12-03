package com.ssj.sfwebsystem.service.impl;

import com.ssj.sfwebsystem.config.UserInfoThreadHolder;
import com.ssj.sfwebsystem.controller.vo.VideoListVO;
import com.ssj.sfwebsystem.dao.VideoRetrievalMapper;
import com.ssj.sfwebsystem.entity.Video;
import com.ssj.sfwebsystem.service.VideoRetrievalService;
import com.ssj.sfwebsystem.util.PageQueryUtil;
import com.ssj.sfwebsystem.util.PageResult;
import org.apache.commons.io.FileUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Service
public class VideoRetrievalServiceImpl implements VideoRetrievalService {
    @Autowired
    private VideoRetrievalMapper videoRetrievalMapper;

    @Override
    public List<Video> getAllVideos() {
        return videoRetrievalMapper.selectAllByMsgStatus();
    }

    @Override
    public List<Video> getAllVideosPage(PageQueryUtil pageUtil) {
        return videoRetrievalMapper.selectAllVideosMessage(pageUtil);
    }

    @Override
    public int insertVideo(Video video) {
        return videoRetrievalMapper.insertSelective(video);
    }

    @Override
    public Video selectByPrimaryKey(Long id) {
        return videoRetrievalMapper.selectByVideoId(id);
    }

    @Override
    public int deleteBatchById(Long[] ids) {
        return videoRetrievalMapper.deleteBatch(ids);
    }

    @Override
    public Video selectByVideoName(String videoName) {
        return videoRetrievalMapper.selectByVideoName(videoName);
    }

    @Override
    public PageResult getCurrentIncompleteMessage(PageQueryUtil queryUtil) {
        // 添加上传者的工号
        queryUtil.put("uploaderId", UserInfoThreadHolder.getCurrentUser().getEmpWorkerId());
        // 拍摄时间为0的那些
        queryUtil.put("shootTime", new Date(0L));
        List<Video> videos = videoRetrievalMapper.selectIncompleteVideos(queryUtil);
        int total = videos.size();
        return new PageResult(videos, total, queryUtil.getLimit(), queryUtil.getPage());
    }

    @Override
    public Video selectByIdIncomplete(Long id) {
        return videoRetrievalMapper.selectByVideoIdIncomplete(id);
    }

    @Override
    public Boolean updateVideo(Video video) {
        return videoRetrievalMapper.updateById(video)==1;
    }

    @Override
    public int getTotalVideos() {
        return videoRetrievalMapper.getTotalCount();
    }

    @Override
    public PageResult getVideoListForAll(PageQueryUtil queryUtil) {
        List<Video> videos = videoRetrievalMapper.selectVideosForAll(queryUtil);
        List<VideoListVO> res = new ArrayList<>();
        for (Video video : videos) {
            VideoListVO videoListVO = new VideoListVO();
            videoListVO.setVideoId(video.getVideoId());
            videoListVO.setVideoName(video.getVideoName());
            videoListVO.setVideoPath(video.getVideoPath());
            videoListVO.setDuration(video.getDuration());
            videoListVO.setShootStartTime(video.getShootStartTime());
            res.add(videoListVO);
        }
        int total = videos.size();
        return new PageResult(res, total, queryUtil.getLimit(), queryUtil.getPage());
    }

    @Override
    public PageResult getCurrentVideoList(PageQueryUtil queryUtil) {
        List<Video> videos = videoRetrievalMapper.selectVideosForAll(queryUtil);
        List<VideoListVO> res = new ArrayList<>();
        for (Video video : videos) {
            VideoListVO videoListVO = new VideoListVO();
            videoListVO.setVideoId(video.getVideoId());
            videoListVO.setVideoName(video.getVideoName());
            videoListVO.setVideoPath(video.getVideoPath());
            videoListVO.setDuration(video.getDuration());
            videoListVO.setShootStartTime(video.getShootStartTime());
            res.add(videoListVO);
        }
        int total = videos.size();
        return new PageResult(res, total, queryUtil.getLimit(), queryUtil.getPage());
    }

    @Override
    public boolean deleteBatch(Long[] longs) {
        // 1.把视频、视频特征、帧序列都删掉、封面
        for (Long id : longs) {
            Video video = videoRetrievalMapper.selectByVideoId(id);
            if(video != null){
                File videoPath = new File(video.getVideoPath());
                File videoFeaturePath = new File(video.getVideoFeaturePath());
                File frameListPath = new File(video.getFrameListPath());
                File coverImgPath = new File(video.getCoverImgPath());
                try {
                    if(videoPath.exists()) FileUtils.delete(videoPath);
                    if(videoFeaturePath.exists()) FileUtils.delete(videoFeaturePath);
                    if(frameListPath.exists()) FileUtils.delete(frameListPath);
                    if(coverImgPath.exists()) FileUtils.delete(coverImgPath);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        // 2.将视频的状态改成2
        return videoRetrievalMapper.deleteBatch(longs) > 0;
    }
}
