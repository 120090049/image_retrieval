package com.ssj.sfwebsystem.controller.admin;

import com.ssj.sfwebsystem.config.Constants;
import com.ssj.sfwebsystem.config.UserInfoThreadHolder;
import com.ssj.sfwebsystem.entity.Employee;
import com.ssj.sfwebsystem.entity.Image;
import com.ssj.sfwebsystem.service.ImageRetrievalService;
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
import java.text.SimpleDateFormat;
import java.util.*;

// 图像检索功能
@Controller
@Slf4j
@RequestMapping("/admin")
public class ImageRetrieval {
    @Autowired
    private ImageRetrievalService imageRetrievalService;

    /**
     * 跳转到图像检索页面
     * @param request request请求对象
     * @return 跳转到图像检索界面
     */
    @GetMapping("/imageRetrieval")
    public String list(HttpServletRequest request) {
        request.setAttribute("path", "imageRetrieval");
        return "admin/imageRetrieval";
    }

    /**
     * 跳转到场景图像库浏览页面，所有员工都可以查看
     * @return 跳转页面
     */
    @GetMapping("/imageList")
    public String imageList() {
        return "admin/imageList";
    }

    /**
     * 跳转到图像上传页面，只有管理员和超级管理员可以使用
     * @return 跳转页面
     */
    @GetMapping("/imageUpload")
    public String categoryPage(HttpServletRequest request) {
        if(!isManager()){
            return "redirect:/admin/index"; // 普通员工不可访问，直接跳到首页
        }
        request.setAttribute("path", "imageUpload");
        return "admin/imageUpload";
    }

    /**
     * 跳转到图像信息修改与删除页面
     * @param request request请求对象
     * @return 跳转页面
     */
    @GetMapping("/imageModifyAndDelete")
    public String imageModifyAndDelete(HttpServletRequest request) {
        if(!isManager()){
            return "redirect:/admin/index"; // 普通员工不可访问，直接跳到首页
        }
        request.setAttribute("path", "imageModifyAndDelete");
        return "admin/imageModifyAndDelete";
    }

    /**
     * 跳转到图像信息不完整列表，只有能上传信息的人才能补全信息，所以也只有管理员能进入
     * @param request request请求对象
     * @return 跳转页面
     */
    @GetMapping("/imageIncomplete")
    public String imageIncomplete(HttpServletRequest request) {
        if(!isManager()){
            return "redirect:/admin/index"; // 普通员工不可访问，直接跳到首页
        }
        request.setAttribute("path", "imageIncomplete");
        return "admin/imageIncomplete";
    }

    /**
     * 获取图片详情
     * @param id 图片主键id
     * @return
     */
    @GetMapping("/image/info/{id}")
    @ResponseBody
    public Result info(@PathVariable("id") Long id) {
        Image image = imageRetrievalService.selectImageById(id);
        return ResultGenerator.genSuccessResult(image);
    }

    // 图片信息修改
    @RequestMapping(value = "/image/update", method = RequestMethod.POST)
    @ResponseBody
    public Result update(@RequestParam("imageId") Long imageId,
                         @RequestParam(name = "imageName", required = false) String imageName,
                         @RequestParam("shootTime") String shootTime) {
        if(!isManager()){
            return ResultGenerator.genFailResult("只有管理员有修改信息的权限哦！"); // 不是管理员不能修改信息
        }
        Image image = imageRetrievalService.selectImageById(imageId);
        if (image == null) {
            return ResultGenerator.genFailResult("无数据");
        }
        if (shootTime == null) {
            return ResultGenerator.genFailResult("拍摄时间参数异常！");
        }
        if(imageName != null && imageName.length() > 0){
            image.setImageName(imageName);
            // log.info("进来了。。。" + imageName);
        }
        //System.out.println(shootTime);//2022-10-31T11:04
        String tempTime = shootTime.replace('T', ' ') + ":00";
        //System.out.println(tempTime);
        try {
            Date date = DateStandard.stringToDate2(tempTime);
            image.setShootTime(date);
            image.setMsgStatus(0);
            return ResultGenerator.genSuccessResult(imageRetrievalService.updateById(image));
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return ResultGenerator.genFailResult("请刷新从新修改！");
    }

    // 图片删除
    @ResponseBody
    @RequestMapping(value = "/image/delete", method = RequestMethod.POST)
    public Result delete(@RequestBody Long id){
        if(!isManager()){
            return ResultGenerator.genFailResult("只有管理员有修改信息的权限哦！"); // 不是管理员不能修改信息
        }
        if(id == null){
            return ResultGenerator.genFailResult("参数异常！");
        }
        if(imageRetrievalService.deleteBatch(new Long[]{id})){
            return ResultGenerator.genSuccessResult();
        }else{
            return ResultGenerator.genFailResult("删除失败");
        }
    }

    // 查找当前用户上传的图片中信息不完整的那些
    @ResponseBody
    @GetMapping("/imageIncomplete/list")
    public Result list(@RequestParam Map<String, Object> params) {
        if (StringUtils.isEmpty(params.get("page")) || StringUtils.isEmpty(params.get("limit"))) {
            return ResultGenerator.genFailResult("参数异常！");
        }
        PageQueryUtil queryUtil = new PageQueryUtil(params);
        return ResultGenerator.genSuccessResult(imageRetrievalService.getCurrentIncompleteMessage(queryUtil));
    }

    // 分页查找所有的图片展示
    @ResponseBody
    @GetMapping("/imageList/list")
    public Result imageList(@RequestParam Map<String, Object> params) {
        if (StringUtils.isEmpty(params.get("page")) || StringUtils.isEmpty(params.get("limit"))) {
            return ResultGenerator.genFailResult("参数异常！");
        }
        PageQueryUtil queryUtil = new PageQueryUtil(params);
        return ResultGenerator.genSuccessResult(imageRetrievalService.getCurrentImageList(queryUtil));
    }

    @ResponseBody
    @GetMapping("/imageList/modifyAndDelete")
    public Result imageListModifyAndDelete(@RequestParam Map<String, Object> params) {
        if(!isManager()){
            return ResultGenerator.genFailResult("只有管理员有修改信息的权限哦！"); // 不是管理员不能修改信息
        }
        if (StringUtils.isEmpty(params.get("page")) || StringUtils.isEmpty(params.get("limit"))) {
            return ResultGenerator.genFailResult("参数异常！");
        }
        PageQueryUtil queryUtil = new PageQueryUtil(params);
        return ResultGenerator.genSuccessResult(imageRetrievalService.getCurrentImageListForModifyAndDelete(queryUtil));
    }

    // 上传到检索图片数据库的图片
    @ResponseBody
    @PostMapping("/upload/uploadToImageDB")
    public synchronized LayUIResponse uploadToIRDB(@RequestParam("file") MultipartFile image, @RequestParam(name = "photoTime") String photoTime) {
        if(!isManager()){
            return new LayUIResponse(1, "权限问题", "只有管理员才能上传图片哦！");
        }
        if (photoTime == null) { // 拍摄时间参数不能为空
            log.error("提取图片的拍摄时间出现异常");
            return new LayUIResponse(1, "提取图片的拍摄时间出现异常，请刷新一下重新上传。");
        }
        if(photoTime.contains("!") || photoTime.contains("@")){ // 拍摄时间参数不能带^和=
            return new LayUIResponse(1, "文件名称不能包含^和=，请修改名称后重新上传");
        }
        if(doubleCheck(photoTime)){
            return new LayUIResponse(1, "本次上传的文件中有重名文件哦，请修改名称后重新上传");
        }
        if (image == null) { // 上传的图像文件参数不能为空
            log.error("上传的图片文件为空");
            return new LayUIResponse(1, "图片文件为空，请刷新重试。");
        }

        // 将图像名称和拍摄时间放在字典里
        Map<String, String> map = photoTimeToMap(photoTime);

        // 2. 将图片保存，特征保存
        boolean success = saveImageAndFeature(image, map);
        if (success) {
            // 2.1保存成功
            return new LayUIResponse(0, "保存成功");
        } else {
            // 2.2保存失败
            return new LayUIResponse(1, "保存失败", image.getOriginalFilename()+"保存失败");
        }
    }

    private Map<String, String> photoTimeToMap(String photoTime) {
        // photoTime: 2022_12_02_11_16_IMG_3911.JPG^2022:12:02 11:17:00=2022_12_02_11_17_IMG_3912.JPG^2022:12:02 11:17:11=
        Map<String, String> map = new HashMap<>();
        String[] split = photoTime.split("=");
        for (String s : split) {
            String[] strings = s.split("\\^");
            map.put(strings[0], strings[1]);
        }
        return map;
    }

    private boolean doubleCheck(String photoTime) {
        // photoTime: 2022_12_02_11_16_IMG_3911.JPG^2022:12:02 11:17:00=2022_12_02_11_17_IMG_3912.JPG^2022:12:02 11:17:11=
        Set<String> set = new HashSet<>();
        String[] split = photoTime.split("=");
        log.info(Arrays.toString(split)); // 打印一下看看
        for (String s : split) {
            if (set.contains(s.split("\\^")[0])){
                return true;
            }
            set.add(s.split("\\^")[0]);
        }
        return false;
    }

    // 保存图像并提取特征
    private boolean saveImageAndFeature(MultipartFile image, Map<String, String> map) {
        String neededTime = map.get(image.getOriginalFilename());
        // 把字符串的时间转成date
        Date shootTime = new Date(0L);
        try {
            shootTime = DateStandard.stringToDate1(neededTime);
        } catch (ParseException e) {
            log.error("字符串的格式不是yyyy:MM:dd hh:mm:ss");
        }
        // 先确保存储图片的文件夹存在
        File imageDataBaseDir = new File(Constants.FILE_UPLOAD_DIC); // 图片文件夹
        if (!imageDataBaseDir.isDirectory()) {
            imageDataBaseDir.mkdirs();// img的temp文件目录不存在就创建一个
        }
        try {
            String originalName = image.getOriginalFilename();//图片本来的名字
            if (originalName != null) {
                // 1.把照片存到服务器文件夹
                String uniqueName = NameUniqueUtil.getUniqueName(originalName);
                File imageServer = new File(Constants.FILE_UPLOAD_DIC, uniqueName);
                log.info("图片上传的真实路径：" + imageServer.getAbsolutePath());
                // 执行上传
                image.transferTo(imageServer);
                // 2.提取特征并保存
                String imagePath = imageServer.getAbsolutePath();
                String success = JavaUsePython.imageUpload(imagePath, uniqueName); // 返回success
                // 3.图片信息存储数据库
                if ("success".equals(success)) {
                    Image imageEntity = new Image();
                    imageEntity.setImageName(originalName);
                    imageEntity.setImagePath(Constants.FILE_UPLOAD_DIC + uniqueName);
                    imageEntity.setUploaderId(UserInfoThreadHolder.getCurrentUser().getEmpWorkerId());
                    imageEntity.setShootTime(shootTime);
                    // TODO 员工工号需要从工作时间表获得
                    imageEntity.setWorkerId("2022102000001");
                    if (shootTime.equals(new Date(0L))) {
                        imageEntity.setMsgStatus(1); // 信息不完整，不提供查询功能
                    } else {
                        imageEntity.setMsgStatus(0);
                    }
                    int i = imageRetrievalService.insertImage(imageEntity);
                    return i > 0;
                }
            }
        } catch (IOException e) {
            log.error("文件保存到服务器出错，烦请重新上传。");
        }
        return false;
    }

    // 场景（图像）检索
    @ResponseBody
    @PostMapping("/upload/imgRetrieval")
    public LayUIResponse iRUploadImg(@RequestParam("file") MultipartFile imageFile, @RequestParam("imgNum") Integer imgNum) {
//        long start = System.currentTimeMillis();
        if (imgNum == null || imgNum < 1) {
            log.error("图像检索的返回图像数量值为空");
            return new LayUIResponse(1, "返回图片数量的值为空了或小于等于0了");
        }
        if (imageFile == null) {
            log.error("图像检索的图片文件为空");
            return new LayUIResponse(1, "图片文件为空");
        }
        File imageDataBaseDir = new File(Constants.IMAGE_UPLOAD_TEMP_PATH); // 图片暂存文件夹
        if (!imageDataBaseDir.isDirectory()) {
            imageDataBaseDir.mkdirs();// img的temp文件目录不存在就创建一个
        }
        try {
            String filename = imageFile.getOriginalFilename();
            if (filename != null) {
                // 服务器保存的文件对象
                File imageServer = new File(Constants.IMAGE_UPLOAD_TEMP_PATH, filename);
                log.info("图片上传的真实路径：" + imageServer.getAbsolutePath());
                // 上传图片文件
                imageFile.transferTo(imageServer);
                String imagePath = Constants.IMAGE_UPLOAD_TEMP_PATH + filename;
                // log.info(imagePath);
                String imgsPath = JavaUsePython.imageRetrieval(imagePath, String.valueOf(imgNum));
                String imagesMessage = selectImageMassageByNames(imgsPath);
//                 log.info("检索图片的信息："+imagesMessage);
                String ip = GetIPValue.getIPValue();
//                System.out.println(ip);
//                long end = System.currentTimeMillis();
//                log.info("场景检索共计用时：" + (end - start));
                return new LayUIResponse(0, ip, imagesMessage);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return new LayUIResponse(1, "上传失败");
    }

    private String selectImageMassageByNames(String imagePath) {
        String[] paths = imagePath.split(" ");
        List<Image> images = imageRetrievalService.imageRetrievalMessage(paths);
        StringBuilder res = new StringBuilder();
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        for (Image image : images) {
            String[] splits = image.getImagePath().split("/");
            res.append(splits[splits.length - 1]); // 图片的路径
            res.append("!");
            res.append(sdf.format(image.getShootTime())); // 拍摄时间
            res.append("!");
            res.append(image.getWorkerId()); // 员工工号
            res.append("?");
        }
        res.deleteCharAt(res.length() - 1);
        return res.toString();
    }

    @GetMapping("/update/list")
    @ResponseBody
    public Result listIncompleteImageMessage(@RequestParam Map<String, Object> params) {
        if (StringUtils.isEmpty(params.get("page")) || StringUtils.isEmpty(params.get("limit"))) {
            return ResultGenerator.genFailResult("参数异常！");
        }
        PageQueryUtil queryUtil = new PageQueryUtil(params);
        return ResultGenerator.genSuccessResult(imageRetrievalService.getCurrentIncompleteMessage(queryUtil));
    }

    private boolean isManager(){
        Byte empType = UserInfoThreadHolder.getCurrentUser().getEmpType();
        return empType == (byte)0 || empType == (byte)1;
    }
}
