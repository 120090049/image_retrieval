package com.ssj.sfwebsystem.dao;



import com.ssj.sfwebsystem.entity.WorkSchedule;
import com.ssj.sfwebsystem.util.PageQueryUtil;

import java.util.List;

public interface WorkerScheduleMapper {
    // 增加工作时间表
    int insert(WorkSchedule workSchedule);

    // 查找所有的工作时间表
    List<WorkSchedule> selectAll(PageQueryUtil pageUtil);
}
