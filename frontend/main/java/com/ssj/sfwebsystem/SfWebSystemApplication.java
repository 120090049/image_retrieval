package com.ssj.sfwebsystem;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;

@SpringBootApplication
@MapperScan("com.ssj.sfwebsystem.dao") // 持久层扫描的包路径
public class SfWebSystemApplication {
    public static void main(String[] args) {
        SpringApplication.run(SfWebSystemApplication.class, args);
    }
}
