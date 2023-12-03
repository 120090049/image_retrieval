package com.ssj.sfwebsystem.service;



import com.ssj.sfwebsystem.entity.Video;
import com.ssj.sfwebsystem.util.PageQueryUtil;
import com.ssj.sfwebsystem.util.PageResult;

import java.util.List;

public interface VideoRetrievalService {
    // 查找出所有视频的信息
    List<Video> getAllVideos();

    List<Video> getAllVideosPage(PageQueryUtil pageUtil);

    // 新增视频数据
    int insertVideo(Video video);

    // 根据主键查找视频
    Video selectByPrimaryKey(Long id);

    // 根据id批量删除视频
    int deleteBatchById(Long[] ids);

    Video selectByVideoName(String videoName);

    // 分页查询信息不完整的图片信息
    PageResult getCurrentIncompleteMessage(PageQueryUtil queryUtil);

    Video selectByIdIncomplete(Long id);

    Boolean updateVideo(Video video);

    int getTotalVideos();

    PageResult getVideoListForAll(PageQueryUtil queryUtil);

    PageResult getCurrentVideoList(PageQueryUtil queryUtil);

    boolean deleteBatch(Long[] longs);
}
