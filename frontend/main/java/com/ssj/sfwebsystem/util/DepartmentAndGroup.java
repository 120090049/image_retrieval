package com.ssj.sfwebsystem.util;

import java.util.HashSet;
import java.util.Set;

// 验证部门与分组是否合法
public class DepartmentAndGroup {
    private static final Set<String> DEPARTMENTANDGROUP = new HashSet<>();
    static {
        DEPARTMENTANDGROUP.add("飞行管理部.分布班组");
        DEPARTMENTANDGROUP.add("飞行管理部.机关班组");
        DEPARTMENTANDGROUP.add("飞行管理部.食堂班组");
        DEPARTMENTANDGROUP.add("信息技术管理部.软件班组");
        DEPARTMENTANDGROUP.add("信息技术管理部.运维班组");
        DEPARTMENTANDGROUP.add("信息技术管理部.行政班组");
        DEPARTMENTANDGROUP.add("维修工程部.维霄班组");
        DEPARTMENTANDGROUP.add("维修工程部.驱鸟班组");
        DEPARTMENTANDGROUP.add("维修工程部.荷花班组");
        DEPARTMENTANDGROUP.add("安全质量监察部.云翼班组");
        DEPARTMENTANDGROUP.add("安全质量监察部.风景线班组");
        DEPARTMENTANDGROUP.add("安全质量监察部.亮剑班组");
        DEPARTMENTANDGROUP.add("运行标准部.黑鹰特战班组");
        DEPARTMENTANDGROUP.add("运行标准部.楷杰班组");
        DEPARTMENTANDGROUP.add("运行标准部.欣悦班组");
        DEPARTMENTANDGROUP.add("运行控制部.指南针班组");
        DEPARTMENTANDGROUP.add("运行控制部.小百灵班组");
        DEPARTMENTANDGROUP.add("运行控制部.龙耀班组");
        DEPARTMENTANDGROUP.add("综合部.飞燕班组");
        DEPARTMENTANDGROUP.add("综合部.磐石班组");
        DEPARTMENTANDGROUP.add("综合部.风盾班组");
    }

    public static boolean isValid(String msg){
        return DEPARTMENTANDGROUP.contains(msg);
    }
}
