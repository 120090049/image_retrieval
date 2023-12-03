package com.ssj.sfwebsystem.service.impl;

import com.alibaba.fastjson.JSONObject;
import com.ssj.sfwebsystem.config.Constants;
import com.ssj.sfwebsystem.config.UserInfoThreadHolder;
import com.ssj.sfwebsystem.controller.vo.ImageListVO;
import com.ssj.sfwebsystem.dao.ImageRetrievalMapper;
import com.ssj.sfwebsystem.entity.Image;
import com.ssj.sfwebsystem.service.ImageRetrievalService;
import com.ssj.sfwebsystem.socket.PythonSocket;
import com.ssj.sfwebsystem.util.PageQueryUtil;
import com.ssj.sfwebsystem.util.PageResult;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Service
@Slf4j
public class ImageRetrievalServiceImpl implements ImageRetrievalService {
    @Autowired
    private ImageRetrievalMapper imageRetrievalMapper;

    /**
     * 根据图像检索返回的图片名称批量查出所有图片的相关信息
     * @param imagesName 图片名称数组
     * @return 图片信息的数组
     */
    @Override
    public List<Image> imageRetrievalMessage(String[] imagesName) {
        List<Image> res = new ArrayList<>();
        String prefixName = Constants.FILE_UPLOAD_DIC;
        for (String name : imagesName) {
            Image image = imageRetrievalMapper.selectImageByImageName(prefixName+name);
            if(image!=null){
                res.add(image);
            }
        }
        return res;
    }

    /**
     * 新增图片信息，只需要填那些必须要填的信息，其他的可以不填，后面再补
     * @param images 图片信息数组
     * @return 哪些图片信息存储成功与失败
     */
    @Override
    public boolean[] insertBatch(List<Image> images) {
        int count = images.size();
        boolean[] res = new boolean[count];
        for (int i = 0; i < count; i++) {
            int num = imageRetrievalMapper.insertSelective(images.get(i));
            res[i] = num == 1;
        }
        return res;
    }

    @Override
    public int insertImage(Image image) {
        return imageRetrievalMapper.insertSelective(image);
    }

    /**
     * 把之前新增的不完整的图片信息补充完整
     * @param images 图片信息数组
     * @return 返回
     */
    @Override
    public boolean[] updateBatchIncomplete(List<Image> images) {
        int count = images.size();
        boolean[] res = new boolean[count];
        for (int i = 0; i < count; i++) {
            int num = imageRetrievalMapper.updateByMsgStatus(images.get(i));
            res[i] = num == 1;
        }
        return res;
    }

    @Override
    public PageResult getCurrentIncompleteMessage(PageQueryUtil queryUtil) {
        // 添加上传者的工号
        queryUtil.put("uploaderId", UserInfoThreadHolder.getCurrentUser().getEmpWorkerId());
        // 拍摄时间为0的那些
        queryUtil.put("shootTime", new Date(0L));
        List<Image> images = imageRetrievalMapper.selectIncompleteImages(queryUtil);
        for (Image image : images) {
            String[] split = image.getImagePath().split("/");
            image.setImagePath("/static/showImg/"+split[split.length-1]);
        }
        int total = images.size();
        return new PageResult(images, total, queryUtil.getLimit(), queryUtil.getPage());
    }

    @Override
    public Image selectImageById(Long id) {
        return imageRetrievalMapper.selectImageById(id);
    }

    @Override
    public Boolean updateById(Image image) {
        return imageRetrievalMapper.updateById(image)==1;
    }

    @Override
    public int getTotalImages() {
        return imageRetrievalMapper.getTotalCount();
    }

    @Override
    public PageResult getCurrentImageList(PageQueryUtil queryUtil) {
        List<Image> images = imageRetrievalMapper.selectImageList(queryUtil);
        for (Image image : images) {
            String[] split = image.getImagePath().split("/");
            image.setImagePath("/static/showImg/"+split[split.length-1]);
        }
        List<ImageListVO> res = new ArrayList<>();
        int index = 0;
        for (int i = 0; i < (images.size() + 3) / 4; i++) {
            ImageListVO imageListVO = new ImageListVO();
            if(index < images.size()){
                imageListVO.setImagePath1(images.get(index).getImagePath());
                index++;
            }
            if(index < images.size()){
                imageListVO.setImagePath2(images.get(index).getImagePath());
                index++;
            }
            if(index < images.size()){
                imageListVO.setImagePath3(images.get(index).getImagePath());
                index++;
            }
            if(index < images.size()){
                imageListVO.setImagePath4(images.get(index).getImagePath());
                index++;
            }
            res.add(imageListVO);
        }
        int total = imageRetrievalMapper.getTotalCount();
        return new PageResult(res, total, queryUtil.getLimit(), queryUtil.getPage());
    }

    @Override
    public PageResult getCurrentImageListForModifyAndDelete(PageQueryUtil queryUtil) {
        List<Image> images = imageRetrievalMapper.selectImageList(queryUtil);
        for (Image image : images) {
            String[] split = image.getImagePath().split("/");
            image.setImagePath("/static/showImg/"+split[split.length-1]);
        }
        int total = imageRetrievalMapper.getTotalCount();
        return new PageResult(images, total, queryUtil.getLimit(), queryUtil.getPage());
    }

    @Override
    @Transactional
    public boolean deleteBatch(Long[] ids) {
        if(ids.length < 1){
            return false;
        }
        // 删除图像数据
        int num = imageRetrievalMapper.deleteBatch(ids);
        // 删除对应的特征
        PythonSocket pythonSocket = new PythonSocket();
        for (Long id : ids) {
//            log.info(String.valueOf(id));
            // 找到该id前面有几个图像，也就是该id在数据库表中排第几
            int index = imageRetrievalMapper.selectCountById(id); // 特征列表索引是从0开始的
//            log.info(String.valueOf(index));
            JSONObject jsonObject = pythonSocket.remoteCall(new String[]{"deleteImage", String.valueOf(index), ""});
            String content = jsonObject.getString("content");
            log.info(content);
        }
        return num > 0;
    }
}
