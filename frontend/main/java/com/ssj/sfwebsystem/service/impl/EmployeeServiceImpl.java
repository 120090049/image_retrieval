package com.ssj.sfwebsystem.service.impl;

import com.ssj.sfwebsystem.dao.EmployeeMapper;
import com.ssj.sfwebsystem.entity.Employee;
import com.ssj.sfwebsystem.service.EmployeeService;
import com.ssj.sfwebsystem.util.MD5Util;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class EmployeeServiceImpl implements EmployeeService {
    @Autowired
    private EmployeeMapper employeeMapper;

    // 注册
    @Override
    public int registerEmployee(Employee employee) {
        // 对注册时设置的密码进行MD5加密
        employee.setPassword(MD5Util.MD5EnCode(employee.getPassword(), "UTF-8"));
        return employeeMapper.insert(employee);
    }

    // 登录
    @Override
    public Employee login(String userName, String password) {
        String passwordMd5 = MD5Util.MD5EnCode(password, "UTF-8");
        return employeeMapper.login(userName, passwordMd5);// 可能为空
    }

    @Override
    public Employee selectByEmpWorkerId(String empWorkerId) {
        return employeeMapper.selectByWorkId(empWorkerId);
    }

    // 修改密码
    public int updatePassword(Employee employee){
        return employeeMapper.updateEmployee(employee);
    }
}
