package com.ssj.sfwebsystem.controller.admin;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/admin")
public class HelloDemo {
    // 跳转到Hello页面
    @GetMapping("/hello")
    public String hello(){
        return "admin/hello";
    }
}
