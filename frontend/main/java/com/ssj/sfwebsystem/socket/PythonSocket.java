package com.ssj.sfwebsystem.socket;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

import java.io.*;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.logging.Logger;

public class PythonSocket {
    // 空构造
    public PythonSocket(){}

    public JSONObject remoteCall(String[] content){
        String host = "127.0.0.1";
        int port = 12345;
        Logger log = Logger.getLogger(this.getClass().getName());
        JSONObject jsonObject = new JSONObject();
        // 添加数据
        jsonObject.put("function", content[0]); // 功能
        if("imageRetrieval".equals(content[0])){
            // content中的内容：1.function功能，2.imgPath图片路径，3.n返回图片数量，4.content返回图像地址集合
            jsonObject.put("path", content[1]); // 图像检索路径
            jsonObject.put("n", content[2]); // 返回几张图像
            jsonObject.put("content", content[3]); // 返回图像的地址集合
        }else if("videoRetrieval".equals(content[0])){
            // function, imagePath, videoFeaturePath, frameCount, frameListPath, duration, resTime
            jsonObject.put("imgPath", content[1]);
            jsonObject.put("videoFeaturePath", content[2]);
            jsonObject.put("frameCount", content[3]);
            jsonObject.put("frameListPath", content[4]);
            jsonObject.put("duration", content[5]);
            jsonObject.put("resTime", content[6]);
        }else if("uploadImage".equals(content[0])) {
            jsonObject.put("imagePath", content[1]);
            jsonObject.put("uniqueName", content[2]);
            jsonObject.put("content", content[3]);
        }else if ("deleteImage".equals(content[0])){
            jsonObject.put("index", content[1]);
            jsonObject.put("content", content[2]);
        }else if("uploadVideo".equals(content[0])){
            //function, videoPath, videoFeaturePath, success,frameCount,frameListPath,duration
            jsonObject.put("videoPath", content[1]);
            jsonObject.put("featurePath", content[2]);
            jsonObject.put("success", content[3]);
            jsonObject.put("frameCount", content[4]);
            jsonObject.put("frameListPath", content[5]);
            jsonObject.put("duration", content[6]);
            jsonObject.put("uniqueName", content[7]);
        }else if("foreignObject".equals(content[0])){
            //function, foreignObjectImgPath, content
            jsonObject.put("foreignObjectImgPath", content[1]);
            jsonObject.put("content", content[2]);
        }
        // 转成json
        String str = jsonObject.toJSONString();
        //log.info("发送内容(JSONObject)：" + jsonObject);
        log.info("发送内容(String)：" + str);
        // 访问服务进程的套接字
        Socket socket = null;
        log.info("调用远程接口:host=>" + host + ",port=>" + port);
        try {
            // 初始化套接字，设置访问服务的主机和进程端口号，HOST是访问python进程的主机名称，可以是IP地址或者域名，PORT是python进程绑定的端口号
            socket = new Socket(host, port);
            // 获取输出流对象
            OutputStream os = socket.getOutputStream();
            PrintStream out = new PrintStream(os);
            // 发送内容
            out.print(str);
            // 告诉服务进程，内容发送完毕，可以开始处理
            out.print("over");
            // 获取服务进程的输入流
            InputStream is = socket.getInputStream();
            BufferedReader br = new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8));
            String tmp;
            StringBuilder sb = new StringBuilder();
            // 读取内容
            while ((tmp = br.readLine()) != null)
                sb.append(tmp).append('\n');
            // 解析结果
            // log.info("接收数据：" + sb);
            // 解析成数组
            // JSONArray res = JSON.parseArray(sb.toString());
            // 解析成对象
            return JSON.parseObject(sb.toString());
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (socket != null) {
                    socket.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
            log.info("远程接口调用结束");
        }
        return null;
    }
}
