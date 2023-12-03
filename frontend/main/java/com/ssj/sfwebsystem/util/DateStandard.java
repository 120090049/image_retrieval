package com.ssj.sfwebsystem.util;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * 日期标准化
 * 可以date转String
 * 也可string转date，支持各种类型
 */
public class DateStandard {
    /**
     * 输入字符串的日期
     * @param date 格式限制：yyyy:MM:dd hh:mm:ss
     * @return 返回date的日期
     */
    public static Date stringToDate1(String date) throws ParseException {
        if("now".equals(date) || date.length()==0) return new Date(0L);
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy:MM:dd hh:mm:ss");
        return sdf.parse(date);
    }

    /**
     * 输入字符串的日期
     * @param date 格式限制：yyyy-MM-dd hh:mm:ss
     * @return 返回date的日期
     */
    public static Date stringToDate2(String date) throws ParseException {
        if("now".equals(date) || date.length()==0) return new Date(0L);
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        return sdf.parse(date);
    }

    /**
     * date 转 yyyy-MM-dd HH:mm:ss字符串格式
     * @param shootStartTime date日期
     * @return 字符串日期
     */
    public static String dateToString(Date shootStartTime) {
        return new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(shootStartTime);
    }
}
