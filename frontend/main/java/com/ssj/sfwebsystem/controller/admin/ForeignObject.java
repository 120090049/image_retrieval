package com.ssj.sfwebsystem.controller.admin;

import com.ssj.sfwebsystem.config.Constants;
import com.ssj.sfwebsystem.socket.JavaUsePython;
import com.ssj.sfwebsystem.util.LayUIResponse;
import com.ssj.sfwebsystem.util.NameUniqueUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.Base64;

@Controller
@Slf4j
@RequestMapping("/admin")
public class ForeignObject {

    /**
     * 跳转到多余物检测页面
     * @param request request request请求对象
     * @return 跳转到多余物检测界面
     */
    @GetMapping("/foreignObject")
    public String list(HttpServletRequest request){
        request.setAttribute("path", "foreignObject");
        return "admin/foreignObject";
    }

    @ResponseBody
    @PostMapping("/upload/foreignObject")
    public LayUIResponse foreignObject(@RequestParam("file")MultipartFile foreignObjectImg){
        if(foreignObjectImg == null){
            log.error("多余物检测的图片为空");
            return new LayUIResponse(1, "图片文件为空");
        }
        File imageDataBaseDir = new File(Constants.IMAGE_UPLOAD_TEMP_PATH); // 图片暂存文件夹
        if(!imageDataBaseDir.isDirectory()){
            imageDataBaseDir.mkdirs();// img的temp文件目录不存在就创建一个
        }
        try{
            String filename = foreignObjectImg.getOriginalFilename(); // 获取图片名称
            if(filename!=null){
                // 服务器保存的文件对象
                File imageServer = new File(Constants.IMAGE_UPLOAD_TEMP_PATH, filename);
                log.info("图片上传的真实路径："+imageServer.getAbsolutePath());
                // 上传图片文件
                foreignObjectImg.transferTo(imageServer);
                // 图片在服务器上的路径
                String imagePath = Constants.IMAGE_UPLOAD_TEMP_PATH + filename;
                // log.info(imagePath);
                String imgPath = JavaUsePython.foreignObject(imagePath);
                // imgPath的格式：是一个绝对路径
                return new LayUIResponse(0, "检测成功", filename+"_res.jpg");
            }
        }catch (IOException e){
            e.printStackTrace();
        }
        return new LayUIResponse(1, "上传失败");
    }

    @ResponseBody
    @PostMapping(value = "/upload/test", consumes = "text/plain")
    public String handleUpload(@RequestBody String base64) throws IOException {
        // 传给python做多余物检测
        if(base64 != null){
            // 解密
            try {
                String savePath = Constants.IMAGE_UPLOAD_TEMP_PATH;
                // 图片分类路径+图片名+图片后缀
                String imgClassPath = NameUniqueUtil.getUniqueName();
                // 去掉base64前缀 data:image/jpeg;base64,
                base64 = base64.substring(base64.indexOf(",", 1) + 1);
                // 解密，解密的结果是一个byte数组
                Base64.Decoder decoder = Base64.getDecoder();
                byte[] imgbytes = decoder.decode(base64);
                for (int i = 0; i < imgbytes.length; ++i) {
                    if (imgbytes[i] < 0) {
                        imgbytes[i] += 256;
                    }
                }

                // 保存图片
                OutputStream out = new FileOutputStream(savePath.concat(imgClassPath));
                out.write(imgbytes);
                out.flush();
                out.close();

                String imagePath = Constants.IMAGE_UPLOAD_TEMP_PATH + imgClassPath;
                return JavaUsePython.foreignObject(imagePath);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return "2";
    }
}
