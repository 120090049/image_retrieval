package com.ssj.sfwebsystem.controller.common;

import com.google.code.kaptcha.impl.DefaultKaptcha;
import com.google.code.kaptcha.util.Config;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;

import java.util.Properties;

@Component
public class KaptchaConfig {
    @Bean
    public DefaultKaptcha getDefaultKaptcha(){
        DefaultKaptcha defaultKaptcha = new DefaultKaptcha();
        Properties properties = new Properties();
        properties.put("kaptcha.border", "no");//没有边框
        properties.put("kaptcha.textproducer.font.color", "black");//黑色字体
        properties.put("kaptcha.image.width", "150");//宽
        properties.put("kaptcha.image.height", "40");//高
        properties.put("kaptcha.textproducer.font.size", "30");//字体大小
        properties.put("kaptcha.session.key", "verifyCode");//在session中存储的key叫什么
        properties.put("kaptcha.textproducer.char.space", "5");//长度为5个字符
        Config config = new Config(properties);
        defaultKaptcha.setConfig(config);
        return defaultKaptcha;
    }
}
