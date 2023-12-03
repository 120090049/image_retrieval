package com.ssj.sfwebsystem.entity;

import java.util.Date;

// 工作时间表
public class WorkSchedule {
    private Long timeId;        // 工作时间表主键
    private Long empId;         // 员工表主键
    private String empWorkerId; // 员工工号
    private String empName;     // 员工姓名
    private String department;  // 员工部门
    private String group;       // 员工分组
    private Date startTime;     // 工作开始时间
    private Date endTime;       // 工作结束时间
    private String comment;     // 备注

    public WorkSchedule() {
    }

    public WorkSchedule(Long timeId, Long empId, String empWorkerId, String empName, String department, String group, Date startTime, Date endTime, String comment) {
        this.timeId = timeId;
        this.empId = empId;
        this.empWorkerId = empWorkerId;
        this.empName = empName;
        this.department = department;
        this.group = group;
        this.startTime = startTime;
        this.endTime = endTime;
        this.comment = comment;
    }

    public Long getTimeId() {
        return timeId;
    }

    public void setTimeId(Long timeId) {
        this.timeId = timeId;
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

    public Date getStartTime() {
        return startTime;
    }

    public void setStartTime(Date startTime) {
        this.startTime = startTime;
    }

    public Date getEndTime() {
        return endTime;
    }

    public void setEndTime(Date endTime) {
        this.endTime = endTime;
    }

    public String getComment() {
        return comment;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }

    @Override
    public String toString() {
        return "WorkSchedule{" +
                "timeId=" + timeId +
                ", empId=" + empId +
                ", empWorkerId='" + empWorkerId + '\'' +
                ", empName='" + empName + '\'' +
                ", department='" + department + '\'' +
                ", group='" + group + '\'' +
                ", startTime=" + startTime +
                ", endTime=" + endTime +
                ", comment='" + comment + '\'' +
                '}';
    }
}
