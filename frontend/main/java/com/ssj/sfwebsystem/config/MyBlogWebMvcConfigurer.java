package com.ssj.sfwebsystem.config;

import com.ssj.sfwebsystem.interceptor.AdminLoginInterceptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * 1.需要一个公网ip地址，还有绑定域名
 */
@Configuration
public class MyBlogWebMvcConfigurer implements WebMvcConfigurer {
    @Autowired
    private AdminLoginInterceptor adminLoginInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 添加一个拦截器，拦截以 /admin 为前缀的url路径
        registry.addInterceptor(adminLoginInterceptor).addPathPatterns("/admin/**")
                .excludePathPatterns("/admin/login")
                .excludePathPatterns("/admin/register/**")
                .excludePathPatterns("/admin/dist/**")
                .excludePathPatterns("/admin/plugins/**")
                .excludePathPatterns("/static/**")
                .excludePathPatterns("/admin/showFile/**") // 文件 静态资源
                .excludePathPatterns("/admin/showImg/**");// 图片 静态资源

    }

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("static/showImg/**", "static/showVideo/**", "admin/showFile/**", "static/foreign/**")
                .addResourceLocations("file:" + Constants.FILE_UPLOAD_DIC, "file:"+Constants.VIDEO_PATH, "file:"+Constants.FILE_UPLOAD_PATH, "file:"+Constants.IMAGE_UPLOAD_TEMP_PATH);
    }
}
