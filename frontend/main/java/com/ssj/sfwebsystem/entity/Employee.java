package com.ssj.sfwebsystem.entity;

import java.util.Date;

// 员工表
public class Employee {
    private Long empId;         // 员工表主键
    private String empWorkerId; // 员工工号
    private String empName;     // 员工姓名
    private String department;  // 部门
    private String group;       // 分组
    private Date joinTime;      // 入职时间
    private Byte empType;       // 员工类型，0超级管理员，1管理员，2普通员工
    private String password;    // 密码

    public Employee() {
    }

    public Employee(Long empId, String empWorkerId, String empName, String department, String group, Date joinTime, Byte empType, String password) {
        this.empId = empId;
        this.empWorkerId = empWorkerId;
        this.empName = empName;
        this.department = department;
        this.group = group;
        this.joinTime = joinTime;
        this.empType = empType;
        this.password = password;
    }

    public Long getEmpId() {
        return empId;
    }

    public void setEmpId(Long empId) {
        this.empId = empId;
    }

    public String getEmpWorkerId() {
        return empWorkerId;
    }

    public void setEmpWorkerId(String empWorkerId) {
        this.empWorkerId = empWorkerId;
    }

    public String getEmpName() {
        return empName;
    }

    public void setEmpName(String empName) {
        this.empName = empName;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public String getGroup() {
        return group;
    }

    public void setGroup(String group) {
        this.group = group;
    }

    public Date getJoinTime() {
        return joinTime;
    }

    public void setJoinTime(Date joinTime) {
        this.joinTime = joinTime;
    }

    public Byte getEmpType() {
        return empType;
    }

    public void setEmpType(Byte empType) {
        this.empType = empType;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    @Override
    public String toString() {
        return "Employee{" +
                "empId=" + empId +
                ", empWorkerId='" + empWorkerId + '\'' +
                ", empName='" + empName + '\'' +
                ", department='" + department + '\'' +
                ", group='" + group + '\'' +
                ", joinTime=" + joinTime +
                ", empType=" + empType +
                ", password='" + password + '\'' +
                '}';
    }
}
