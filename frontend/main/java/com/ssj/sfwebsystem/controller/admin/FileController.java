package com.ssj.sfwebsystem.controller.admin;

import com.ssj.sfwebsystem.config.Constants;
import com.ssj.sfwebsystem.config.UserInfoThreadHolder;
import com.ssj.sfwebsystem.entity.FileEntity;
import com.ssj.sfwebsystem.entity.Image;
import com.ssj.sfwebsystem.service.FileEntityService;
import com.ssj.sfwebsystem.util.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import java.io.File;
import java.io.IOException;
import java.text.ParseException;
import java.util.*;

@Slf4j
@Controller
@RequestMapping("/admin")
public class FileController {
    @Autowired
    private FileEntityService fileEntityService;

    private static final Set<String> IMAGE_TYPE = new HashSet<>();
    static {
        IMAGE_TYPE.add("webp");IMAGE_TYPE.add("bmp");IMAGE_TYPE.add("pcx");
        IMAGE_TYPE.add("tif");IMAGE_TYPE.add("gif");IMAGE_TYPE.add("jpeg");
        IMAGE_TYPE.add("tga");IMAGE_TYPE.add("exif");IMAGE_TYPE.add("fpx");
        IMAGE_TYPE.add("svg");IMAGE_TYPE.add("psd");IMAGE_TYPE.add("cdr");
        IMAGE_TYPE.add("pcd");IMAGE_TYPE.add("dxf");IMAGE_TYPE.add("png");
        IMAGE_TYPE.add("hdri");IMAGE_TYPE.add("raw");IMAGE_TYPE.add("ico");
        IMAGE_TYPE.add("jpg");
    }

    /**
     * 跳转到文件上传页面
     * @param request request request请求对象
     * @return 跳转到文件上传页面
     */
    @GetMapping("/fileUpload")
    public String list(HttpServletRequest request){
        request.setAttribute("path", "fileUpload");
        return "admin/fileUpload";
    }

    /**
     * 跳转到所有人都能查看的文件列表页面
     * @param request request request请求对象
     * @return 跳转到文件查看页面
     */
    @GetMapping("/fileList")
    public String listForAll(HttpServletRequest request){
        request.setAttribute("path", "fileList");
        return "admin/fileList";
    }

    // 分页查询文件信息
    @GetMapping("/fileSearch/list")
    @ResponseBody
    public Result list(@RequestParam Map<String, Object> params){
        if(StringUtils.isEmpty(params.get("page")) || StringUtils.isEmpty(params.get("limit"))){
            if(params.get("page") == null) log.info("page为空");
            if(params.get("limit") == null) log.info("limit为空");
            return ResultGenerator.genFailResult("参数异常！");
        }
        // 过滤掉值为空的键值对
        if(params.containsKey("fileName")&&"".equals(params.get("fileName"))){
            params.remove("fileName");
        }
        if(params.containsKey("uploadId")&&"".equals(params.get("uploadId"))){
            params.remove("uploadId");
        }
        if(params.containsKey("startTime")&&"".equals(params.get("startTime"))){
            params.remove("startTime");
        }
        if(params.containsKey("endTime")&&"".equals(params.get("endTime"))){
            params.remove("endTime");
        }
        PageQueryUtil pageQueryUtil = new PageQueryUtil(params);
        return ResultGenerator.genSuccessResult(fileEntityService.getFilePage(pageQueryUtil));
    }

    // 打开指定id的文件
    @GetMapping("/files/open/{fileId}")
    public String openFile(HttpServletRequest request, @PathVariable("fileId") Long fileId){
        FileEntity fileEntity = fileEntityService.getFileById(fileId);
        if(fileEntity == null){
            return "error/error_400";
        }
        // 存储ip信息和文件的真实地址
        request.setAttribute("ip", GetIPValue.getIPValue());
        String separator = File.separator;
        String regex = "\\\\";
        if("/".equals(separator)){
            regex = "/";
        }
        String[] split = fileEntity.getFilePath().split(regex);
        request.setAttribute("realPath", split[split.length-1]);
        if("pdf".equals(fileEntity.getFileType())){
            request.setAttribute("fileType", "pdf");
        }else if(IMAGE_TYPE.contains(fileEntity.getFileType())){
            request.setAttribute("fileType", "jpg");
        }
        return "admin/fileOnlineReview";
    }

    /**
     * 跳转到文件检索页面
     * @param request request request请求对象
     * @return 跳转到文件检索页面
     */
    @GetMapping("/fileSearch")
    public String search(HttpServletRequest request){
        request.setAttribute("path", "fileSearch");
        return "admin/fileSearch";
    }

    /**
     * 获取文件详情
     * @param id 文件主键id
     * @return
     */
    @GetMapping("/file/info/{id}")
    @ResponseBody
    public Result info(@PathVariable("id") Long id) {
        FileEntity fileEntity = fileEntityService.selectById(id);
        return ResultGenerator.genSuccessResult(fileEntity);
    }

    // 文件信息修改
    @RequestMapping(value = "/file/update", method = RequestMethod.POST)
    @ResponseBody
    public Result update(@RequestParam("fileId") Long fileId,
                         @RequestParam(name = "fileNameForUpdate") String fileName) {
        if(!isManager()){
            return ResultGenerator.genFailResult("只有管理员有修改信息的权限哦！"); // 不是管理员不能修改信息
        }
        FileEntity fileEntity = fileEntityService.selectById(fileId);
        if (fileEntity == null) {
            return ResultGenerator.genFailResult("无数据");
        }
        if(fileName != null && fileName.length() > 0){
            fileEntity.setFileName(fileName);
            return ResultGenerator.genSuccessResult(fileEntityService.updateFileMessage(fileEntity));
        }
        return ResultGenerator.genFailResult("请刷新从新修改！");
    }

    // 文件上传接口
    @PostMapping("/upload/fileUpload")
    @ResponseBody
    public LayUIResponse fileUpload(@RequestParam("file") MultipartFile[] multipartFiles){
        if(multipartFiles == null || multipartFiles.length == 0){
            log.error("图像检索的图片文件为空");
            return new LayUIResponse(1, "文件数量不对");
        }
        //System.out.println(multipartFiles.length);
        File imageDataBaseDir = new File(Constants.FILE_UPLOAD_PATH); // 文件存储的文件夹
        if(!imageDataBaseDir.isDirectory()){
            imageDataBaseDir.mkdirs();// 文件目录不存在就创建一个
        }
        // 逐个文件保存
        List<String> failSavedNames = new ArrayList<>();
        for (MultipartFile file : multipartFiles) {
            boolean save = saveOneFile(file);
            if(!save){
                failSavedNames.add(file.getOriginalFilename());
            }
        }
        return new LayUIResponse(0, "文件保存结果", failSavedNames);
    }

    // 以事务的形式保存文件并将信息存储数据库
    @Transactional
    protected boolean saveOneFile(MultipartFile file){
        String originalFilename = file.getOriginalFilename(); // 上传时文件的名字
        try{
            // 1.将文件保存到服务器
            File fileObjOnServer = new File(Constants.FILE_UPLOAD_PATH, NameUniqueUtil.getUniqueName(originalFilename));
            log.info("图片上传的真实路径："+fileObjOnServer.getAbsolutePath());
            String size = file.getSize()+""; // 单位是：字节
            file.transferTo(fileObjOnServer); // 将上传的文件保存到该位置
            // 2.将文件的信息存储到数据库
            FileEntity fileEntity = new FileEntity();
            fileEntity.setFileName(originalFilename);
            fileEntity.setFilePath(fileObjOnServer.getAbsolutePath());
            fileEntity.setUploaderWorkId(UserInfoThreadHolder.getCurrentUser().getEmpWorkerId());
            String[] split = originalFilename.split("\\.");
            fileEntity.setFileType(split[split.length-1].toLowerCase());
            fileEntity.setFileSize(size);
            fileEntity.setComment("文件上传");
            return fileEntityService.saveFile(fileEntity)==1;
        }catch (IOException e){
            e.printStackTrace();
            return false;
        }
    }

    /**
     * 批量删除文件
     * @param ids 前端传过来的文件id数组
     * @return 删除成功返回成功的结果，删除失败或没有id返回失败的结果
     */
    @PostMapping("/files/delete")
    @ResponseBody
    public Result delete(@RequestBody Long[] ids){
        if(ids.length < 1){
            return ResultGenerator.genFailResult("参数异常！");
        }
        if(fileEntityService.deleteBatch(ids)){
            return ResultGenerator.genSuccessResult();
        }else{
            return ResultGenerator.genFailResult("删除失败");
        }
    }

    private boolean isManager(){
        Byte empType = UserInfoThreadHolder.getCurrentUser().getEmpType();
        return empType == (byte)0 || empType == (byte)1;
    }
}
