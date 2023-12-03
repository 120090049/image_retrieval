package com.ssj.sfwebsystem.dao;

import com.ssj.sfwebsystem.entity.Video;
import com.ssj.sfwebsystem.util.PageQueryUtil;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface VideoRetrievalMapper {
    // 插入视频部分信息
    int insertSelective(Video video);

    // 根据信息状态修改视频信息
    int updateByMsgStatus(Video video);

    // 根据主键删除视频
    int deleteByPrimaryKey(Long videoId);

    // 批量删除
    int deleteBatch(Long[] ids);

    // 查找所有视频信息分页
    List<Video> selectAllVideosMessage(PageQueryUtil pageUtil);

    // 查找所有视频信息，不分页
    List<Video> selectAllByMsgStatus();

    // 根据id检索视频
    Video selectByVideoId(Long id);

//    int deleteById(Long[] ids);
    Video selectByVideoName(@Param("videoName") String videoName);

    List<Video> selectIncompleteVideos(PageQueryUtil queryUtil);

    Video selectByVideoIdIncomplete(Long id);

    int updateById(Video video);

    int getTotalCount();

    List<Video> selectVideosForAll(PageQueryUtil queryUtil);
}
