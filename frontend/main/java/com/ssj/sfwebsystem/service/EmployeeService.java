package com.ssj.sfwebsystem.service;


import com.ssj.sfwebsystem.entity.Employee;

// 跟用户及员工相关的service
public interface EmployeeService {
    // 注册用户信息
    int registerEmployee(Employee employee);

    // 用户登录信息
    Employee login(String userName, String password);

    // 根据工号查询员工信息
    Employee selectByEmpWorkerId(String empWorkerId);

    int updatePassword(Employee currentUser);
}
