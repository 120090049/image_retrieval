package com.ssj.sfwebsystem.dao;


import com.ssj.sfwebsystem.entity.Employee;
import org.apache.ibatis.annotations.Param;

public interface EmployeeMapper {
    // 新增员工
    int insert(Employee employee);

    // 根据主键查找员工
    Employee selectById(Long empId);

    // 根据工号查找员工
    Employee selectByWorkId(@Param("workId") String workId);

    // 修改员工信息，根据主键
    int updateEmployee(Employee newEmployee);

    // 根据主键删除员工信息
    int deleteById(Long empId);

    Employee login(@Param("userName") String userName, @Param("passwordMd5") String passwordMd5);
}
