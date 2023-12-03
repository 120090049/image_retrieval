package com.ssj.sfwebsystem.util;

import java.text.SimpleDateFormat;
import java.util.Date;

// 给服务器上的文件名起唯一名字的工具
public class NameUniqueUtil {
    private static final SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMddHHmmss");
    private static volatile long seed = 0L;
    // 输入一个带后缀的名字，返回带上时间的名字
    public synchronized static String getUniqueName(String name){
        if(name == null || name.length() == 0){
            throw new RuntimeException("名字为空或长度为0");
        }
        String[] strs = name.split("\\.");
        if(strs == null || strs.length!=2){
            throw new RuntimeException("请保证文件命名规范，有且仅有一个点用来分割名称和后缀");
        }
        Date now = new Date();
        String format = sdf.format(now);
        StringBuilder res = new StringBuilder();
        res.append(format);
        res.append(seed++);
        if(seed==Long.MAX_VALUE) seed=0L; // 复位
        res.append(".");
        res.append(strs[1]);
        return res.toString();
    }

    // 没有名字的生成随机名字
    public synchronized static String getUniqueName(){
        Date now = new Date();
        String format = sdf.format(now);
        StringBuilder res = new StringBuilder();
        res.append(format);
        res.append(seed++);
        if(seed==Long.MAX_VALUE) seed=0L; // 复位
        res.append(".");
        res.append("jpg");
        return res.toString();
    }
}
