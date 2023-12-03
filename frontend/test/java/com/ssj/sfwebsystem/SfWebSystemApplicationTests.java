package com.ssj.sfwebsystem;

import javafx.util.converter.LocalDateStringConverter;
import net.bytebuddy.asm.Advice;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import java.time.DayOfWeek;
import java.time.LocalDate;
import java.util.Date;

@SpringBootTest
class SfWebSystemApplicationTests {

    @Test
    void contextLoads() {
        Date date1 = new Date();
        System.out.println(date1);

        LocalDate now = LocalDate.now();
        System.out.println(now);

        LocalDate date = LocalDate.of(2020, 8, 21);
        int year = date.getYear(); // 获取年
        int monthValue = date.getMonthValue(); // 获取月
        int dayOfMonth = date.getDayOfMonth(); // 获取日
        LocalDate localDateNew = date.plusDays(1000L); // 做加法计算
        DayOfWeek dayOfWeek = date.getDayOfWeek(); // 获取是一周的第几天
        int value = dayOfWeek.getValue(); // 周一是1，周二是2，...，周日是7
    }

}
