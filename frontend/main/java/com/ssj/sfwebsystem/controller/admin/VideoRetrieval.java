package com.ssj.sfwebsystem.controller.admin;

import com.alibaba.fastjson.JSONObject;
import com.ssj.sfwebsystem.config.Constants;
import com.ssj.sfwebsystem.config.UserInfoThreadHolder;
import com.ssj.sfwebsystem.entity.Video;
import com.ssj.sfwebsystem.service.VideoRetrievalService;
import com.ssj.sfwebsystem.socket.JavaUsePython;
import com.ssj.sfwebsystem.util.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import java.io.File;
import java.io.IOException;
import java.text.ParseException;
import java.util.Date;
import java.util.List;
import java.util.Map;

@Slf4j
@Controller
@RequestMapping("/admin")
public class VideoRetrieval {
    @Autowired
    private VideoRetrievalService videoRetrievalService;

    // 跳转到视频上传的页面
    @GetMapping("/uploadVideo")
    public String toVideoUpload(HttpServletRequest request){
        request.setAttribute("path", "uploadVideo");
        return "admin/videoUpload";
    }

    @GetMapping("/videoModifyAndDelete")
    public String toVideoModifyAndDelete(HttpServletRequest request){
        request.setAttribute("path", "videoModifyAndDelete");
        return "admin/videoModifyAndDelete";
    }

    /**
     * 跳转到查看视频列表页面，所有人都能查看
     * @return 页面跳转
     */
    @GetMapping("/videoList")
    public String videoList(){
        return "admin/videoList";
    }

    // 所有用户都可以查看的视频信息
    @ResponseBody
    @GetMapping("/videoList/list")
    public Result videoList(@RequestParam Map<String, Object> params){
        if(StringUtils.isEmpty(params.get("page")) || StringUtils.isEmpty(params.get("limit"))){
            return ResultGenerator.genFailResult("参数异常！");
        }
        PageQueryUtil queryUtil = new PageQueryUtil(params);
        return ResultGenerator.genSuccessResult(videoRetrievalService.getVideoListForAll(queryUtil));
    }

    // 跳转到视频补全信息页面
    @GetMapping("/videoIncomplete")
    public String videoIncomplete(HttpServletRequest request){
        request.setAttribute("path", "videoIncomplete");
        return "admin/videoIncomplete";
    }

    // 跳转到视频播放页面
    @GetMapping("/videoBroadcast")
    public String toBroadcast(HttpServletRequest request, @RequestParam("id") Long id){
        request.setAttribute("path", "videoBroadcast");
        Video video = videoRetrievalService.selectByPrimaryKey(id);
        String[] split = video.getVideoPath().split("\\\\");
        String videoPath = "/static/showVideo/" + split[split.length-1];
        request.setAttribute("videoName", video.getVideoName().split("\\.")[0]);
        request.setAttribute("videoPath", videoPath);
        return "admin/videoBroadcast";
    }

    // 跳转到视频检索页面
    @GetMapping("/videoRetrieval")
    public String list(HttpServletRequest request){
        List<Video> allVideos = videoRetrievalService.getAllVideos();
//        System.out.println(allVideos);
        request.setAttribute("allVideos", allVideos);
        request.setAttribute("path", "videoRetrieval");
        return "admin/videoRetrieval";
    }

    // 查找当前用户上传的视频中信息不完整的那些
    @ResponseBody
    @GetMapping("/videoIncomplete/list")
    public Result list(@RequestParam Map<String, Object> params){
        if(StringUtils.isEmpty(params.get("page")) || StringUtils.isEmpty(params.get("limit"))){
            return ResultGenerator.genFailResult("参数异常！");
        }
        PageQueryUtil queryUtil = new PageQueryUtil(params);
        return ResultGenerator.genSuccessResult(videoRetrievalService.getCurrentIncompleteMessage(queryUtil));
    }

    // 视频详情
    @GetMapping("/video/info/{id}")
    @ResponseBody
    public Result info(@PathVariable("id") Long id){
//        System.out.println(id==null?-1:id); // 4
        Video video = videoRetrievalService.selectByPrimaryKey(id);
//        System.out.println(video==null?1:video);
        return ResultGenerator.genSuccessResult(video);
    }

    // 视频播放
    @GetMapping("/video/broadcast/{id}")
    public String broadcast(@PathVariable("id") Long id, HttpServletRequest request){
        //System.out.println(id==null?-1:id); // 4
        Video video = videoRetrievalService.selectByPrimaryKey(id);
        request.setAttribute("videoName", video.getVideoName());
        //System.out.println(video==null?1:video);
        String videoPath = video.getVideoPath();
        String[] split = videoPath.split("\\\\");
        request.setAttribute("videoPath", "/static/showVideo/" + split[split.length-1]);
        return "admin/videoBroadcast";
    }

    // 删除某一个视频
    @RequestMapping(value = "/video/delete", method = RequestMethod.POST)
    @ResponseBody
    public Result delete (@RequestBody Long id){
        if(!isManager()){
            return ResultGenerator.genFailResult("只有管理员有修改信息的权限哦！"); // 不是管理员不能修改信息
        }
        if(id == null){
            return ResultGenerator.genFailResult("参数异常！");
        }
        if(videoRetrievalService.deleteBatch(new Long[]{id})){
            return ResultGenerator.genSuccessResult();
        }else{
            return ResultGenerator.genFailResult("删除失败");
        }
    }

    // 视频信息修改，该方法用于更改信息不完整时的视频信息
    @RequestMapping(value = "/video/update", method = RequestMethod.POST)
    @ResponseBody
    public Result update(@RequestParam("videoId") Long videoId,
                         @RequestParam("shootStartTime") String shootStartTime){
        if(videoId == null){
            return ResultGenerator.genFailResult("请选择正确的视频序号！");
        }
        if(shootStartTime == null){
            return ResultGenerator.genFailResult("开始拍摄时间参数异常！");
        }
        Video video = videoRetrievalService.selectByIdIncomplete(videoId);
        if(video == null){
            return ResultGenerator.genFailResult("无数据");
        }
        // System.out.println(shootStartTime);//2022-11-01T11:05
        String tempTime = shootStartTime.replace('T', ' ')+":00";
        //System.out.println(tempTime);
        try {
            Date date = DateStandard.stringToDate2(tempTime);
            video.setShootStartTime(date);
            video.setMsgStatus(0);
            return ResultGenerator.genSuccessResult(videoRetrievalService.updateVideo(video));
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return ResultGenerator.genFailResult("请刷新从新修改！");
    }

    // 视频信息修改，该方法用于管理员对信息的修改
    @RequestMapping(value = "/video/updateForManger", method = RequestMethod.POST)
    @ResponseBody
    public Result updateForManger(@RequestParam("videoId") Long videoId,
                                  @RequestParam("shootStartTime") String shootStartTime,
                                  @RequestParam("videoName") String videoName){
        if(videoId == null){
            return ResultGenerator.genFailResult("请选择正确的视频序号！");
        }
        if(videoName == null){
            return ResultGenerator.genFailResult("视频名称不对，请重新输入！");
        }
        if(shootStartTime == null){
            return ResultGenerator.genFailResult("开始拍摄时间参数异常！");
        }
        Video video = videoRetrievalService.selectByPrimaryKey(videoId);
        if(video == null){
            return ResultGenerator.genFailResult("无数据");
        }
        // System.out.println(shootStartTime);//2022-11-01T11:05
        String tempTime = shootStartTime.replace('T', ' ')+":00";
        //System.out.println(tempTime);
        try {
            Date date = DateStandard.stringToDate2(tempTime);
            video.setShootStartTime(date);
            video.setVideoName(videoName);
            video.setMsgStatus(0);
            return ResultGenerator.genSuccessResult(videoRetrievalService.updateVideo(video));
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return ResultGenerator.genFailResult("请刷新从新修改！");
    }

    // 视频检索的功能
    @ResponseBody
    @PostMapping("/upload/videoRetrieval")
    public LayUIResponse videoRetrieval(@RequestParam("file") MultipartFile imageFile, @RequestParam("videoName") String videoName){
        if(imageFile == null){
            log.error("视频检索的图片文件为空");
            return new LayUIResponse(1, "图片文件为空");
        }
        if(videoName == null){
            log.error("视频检索的视频名称为空");
            return new LayUIResponse(1, "视频名称为空");
        }
        File imageDataBaseDir = new File(Constants.VIDEO_UPLOAD_TEMP_PATH); // 图片暂存文件夹
        if(!imageDataBaseDir.isDirectory()){
            imageDataBaseDir.mkdirs();// img的temp文件目录不存在就创建一个
        }
        try{
            String filename = imageFile.getOriginalFilename();
            if(filename!=null){
                // 服务器保存的文件对象
                File imageServer = new File(Constants.VIDEO_UPLOAD_TEMP_PATH, filename);
                log.info("图片上传的真实路径："+imageServer.getAbsolutePath());
                // 上传图片文件
                imageFile.transferTo(imageServer);
                String imagePath = Constants.VIDEO_UPLOAD_TEMP_PATH + filename;
                // log.info(imagePath);
                // 调用视频检索
                Video video = videoRetrievalService.selectByVideoName(videoName);
                String resTime = JavaUsePython.videoRetrieval(imagePath, video);
//                 log.info("检索图片的信息："+imagesMessage);
                // 查询视频拍摄时间
                String shootStartTime = DateStandard.dateToString(video.getShootStartTime());

                // 视频的路径
                String[] arr = video.getVideoPath().replaceAll("\\\\", "/").split("/");
                String videoPath = arr[arr.length-1];
                String ip = GetIPValue.getIPValue();
//                System.out.println(ip);
//                System.out.println(resTime);
                return new LayUIResponse(0, ip, resTime+"="+shootStartTime+"="+videoPath);
            }
        }catch (IOException e){
            e.printStackTrace();
        }
        return new LayUIResponse(1, "上传失败");
    }

    // 上传到检索视频数据库的视频
    @ResponseBody
    @PostMapping("/upload/uploadToVideoDB")
    public synchronized LayUIResponse uploadToVRDB(@RequestParam("file") MultipartFile video, @RequestParam(name = "photoTime") String photoTime){
        if(photoTime == null){
            log.error("提取图片的拍摄时间出现异常");
            return new LayUIResponse(1, "提取图片的拍摄时间出现异常，请刷新一下重新上传。");
        }
        if(video == null){
            log.error("上传的图片文件为空");
            return new LayUIResponse(1, "图片文件为空，请刷新重试。");
        }
        if(video.getSize() > 100*1024*1024L){
            log.info("上传文件超过100M了");
            return new LayUIResponse(1, "请上传小于100M的视频。");
        }


        // 2. 将视频保存，特征保存
        boolean success = saveVideoAndFeature(video, photoTime);
        if(success){
            // 2.1保存成功，更新“已保存字符串”
            return new LayUIResponse(0, "保存成功");
        }else{
            // 2.2保存失败，不需要更新啥
            return new LayUIResponse(1, "保存失败", "保存失败");
        }
    }

    private boolean saveVideoAndFeature(MultipartFile video, String neededTime) {
        // 把字符串的时间转成date
        Date shootTime = new Date(0L);
        try {
            shootTime = DateStandard.stringToDate1(neededTime);
        } catch (ParseException e) {
            log.error("字符串的格式不是yyyy:MM:dd hh:mm:ss");
        }
        // 先确保存储视频的文件夹存在
        File videoDataBaseDir = new File(Constants.VIDEO_PATH); // 视频文件夹
        if(!videoDataBaseDir.isDirectory()){
            videoDataBaseDir.mkdirs();// video的文件目录不存在就创建一个
        }
        try{
            String originalName = video.getOriginalFilename();//视频本来的名字
            if(originalName!=null){
                // 1.把视频存到服务器文件夹
                String uniqueName = NameUniqueUtil.getUniqueName(originalName);
                File videoServer = new File(Constants.VIDEO_PATH, uniqueName);
                log.info("视频上传的真实路径："+ videoServer.getAbsolutePath());
                // 执行上传
                video.transferTo(videoServer);
                // 2.提取特征并保存
                String videoPath = videoServer.getAbsolutePath();
                // 生成特征路径
                String videoFeaturePath = Constants.VIDEO_FEATURE_PATH + uniqueName.split("\\.")[0]+".npy";
                JSONObject res = JavaUsePython.videoUpload(videoPath, videoFeaturePath, uniqueName);// 返回jsonObject
                // 3.视频信息存储数据库
                if("success".equals(res.getString("success"))){
                    Video videoEntity = new Video();
                    videoEntity.setVideoPath(videoPath);
                    videoEntity.setCoverImgPath(""); // 可以不要的
                    videoEntity.setVideoName(originalName);
                    videoEntity.setShootStartTime(shootTime); // 拍摄开始时间
                    String[] nums = res.getString("duration").split("\\.");
                    videoEntity.setDuration(Double.parseDouble(nums[0]+"."+nums[1].substring(0,2)));
                    videoEntity.setUploaderId(UserInfoThreadHolder.getCurrentUser().getEmpWorkerId());
                    videoEntity.setVideoFeaturePath(videoFeaturePath);
                    videoEntity.setFrameCount(Double.parseDouble(res.getString("frameCount")));
                    videoEntity.setFrameListPath(res.getString("frameListPath"));
                    if(shootTime.equals(new Date(0L))){
                        videoEntity.setMsgStatus(1); // 信息不完整，不提供查询功能
                    }else{
                        videoEntity.setMsgStatus(0);
                    }
                    int i = videoRetrievalService.insertVideo(videoEntity);
                    return i > 0;
                }
            }
        }catch (IOException e){
            log.error("文件保存到服务器出错，烦请重新上传。");
        }
        return false;
    }

    private boolean isManager(){
        Byte empType = UserInfoThreadHolder.getCurrentUser().getEmpType();
        return empType == (byte)0 || empType == (byte)1;
    }
}
