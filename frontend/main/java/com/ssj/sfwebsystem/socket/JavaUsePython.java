package com.ssj.sfwebsystem.socket;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.ssj.sfwebsystem.entity.Video;

public class JavaUsePython {
    public static String imageUpload(String imagePath, String uniqueName){ // 图像上传调用
        PythonSocket pythonSocket = new PythonSocket();
        String content = "";
        String function = "uploadImage";
        JSONObject jsonObject = pythonSocket.remoteCall(new String[]{function, imagePath, uniqueName, content});
        return jsonObject.getString("content");
    }

    public static String imageRetrieval(String imagePath, String nums) { // 图像检索调用
        PythonSocket pythonSocket = new PythonSocket();
        String content = "";
        String function = "imageRetrieval";
        if(imagePath.contains("\\")){
            imagePath.replaceAll("\\\\", "/");
        }
        JSONObject jsonObject = pythonSocket.remoteCall(new String[]{function, imagePath, nums, content});
        JSONArray array = jsonObject.getJSONArray("content");
        StringBuilder res = new StringBuilder();
        for (Object o : array) {
            res.append((String) o + " ");
        }
        return res.toString();
    }

    public static String foreignObject(String imagePath) { // 多余物检测功能
        PythonSocket pythonSocket = new PythonSocket();
        String content = "";
        String function = "foreignObject";
        JSONObject jsonObject = pythonSocket.remoteCall(new String[]{function, imagePath, content});
        return jsonObject.getString("content");
    }

    public static String videoRetrieval(String imagePath, Video video) { // 视频检索调用
        PythonSocket pythonSocket = new PythonSocket();
        String resTime = "";
        String function = "videoRetrieval";
        String videoFeaturePath = video.getVideoFeaturePath();
        String frameCount = String.valueOf(video.getFrameCount());
        String frameListPath = video.getFrameListPath();
        String duration = String.valueOf(video.getDuration());
        JSONObject jsonObject = pythonSocket.remoteCall(new String[]{function, imagePath, videoFeaturePath, frameCount, frameListPath, duration, resTime});
        return jsonObject.getString("resTime");
    }

    public static JSONObject videoUpload(String videoPath, String videoFeaturePath, String uniqueName){ // 视频上传调用
        // 需要两个参数：1.视频的路径，2.视频保存的特征路径
        // 调用python接口
        PythonSocket pythonSocket = new PythonSocket();
        String function = "uploadVideo";
        String success = "";
        String frameCount = "0";
        String frameListPath = "";
        String duration = "";
        return pythonSocket.remoteCall(new String[]{function, videoPath, videoFeaturePath, success,frameCount,frameListPath,duration, uniqueName});
    }
}
