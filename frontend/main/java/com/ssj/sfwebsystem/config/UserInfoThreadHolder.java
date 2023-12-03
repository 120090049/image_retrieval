package com.ssj.sfwebsystem.config;

import com.ssj.sfwebsystem.entity.Employee;

public class UserInfoThreadHolder {
    // 保存用户对象的threadLocal
    private static final ThreadLocal<Employee> userThreadLocal = new ThreadLocal<>();

    // 添加用户信息
    public static void addCurrentUser(Employee user){
        userThreadLocal.set(user);
    }

    // 获取用户信息
    public static Employee getCurrentUser(){
        return userThreadLocal.get();
    }

    // 防止内存泄露
    public static void remove(){
        userThreadLocal.remove();
    }
}
