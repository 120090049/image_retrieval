package com.ssj.sfwebsystem.controller.admin;

import com.alibaba.fastjson.JSONObject;
import com.ssj.sfwebsystem.config.UserInfoThreadHolder;
import com.ssj.sfwebsystem.entity.Employee;
import com.ssj.sfwebsystem.service.EmployeeService;
import com.ssj.sfwebsystem.service.FileEntityService;
import com.ssj.sfwebsystem.service.ImageRetrievalService;
import com.ssj.sfwebsystem.service.VideoRetrievalService;
import com.ssj.sfwebsystem.util.DepartmentAndGroup;
import com.ssj.sfwebsystem.util.LayUIResponse;
import com.ssj.sfwebsystem.util.MD5Util;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.thymeleaf.util.StringUtils;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import java.util.Date;

@Slf4j
@Controller
@RequestMapping("/admin")
public class EmployeeController {
    @Autowired
    private EmployeeService employeeService;
    @Autowired
    private ImageRetrievalService imageRetrievalService;
    @Autowired
    private VideoRetrievalService videoRetrievalService;
    @Autowired
    private FileEntityService fileEntityService;

    // 跳转到登录页面
    @GetMapping("/login")
    public String login(){
        return "admin/login";
    }

    // 跳转到注册页面
    @GetMapping("/register")
    public String register(){
        return "admin/register";
    }

    // 跳转到修改密码页面
    @GetMapping("/updatePassword")
    public String updatePassword(HttpServletRequest request){
        request.setAttribute("path", "updatePassword");
        return "admin/updatePassword";
    }

    // 跳转到管理员修改密码页面
    @GetMapping("/updatePasswordForAdmin")
    public String updatePasswordForAdmin(HttpServletRequest request){
        request.setAttribute("path", "updatePasswordForAdmin");
        return "admin/updatePasswordForAdmin";
    }

    // 工号密码验证码验证登录
    @PostMapping("/login")
    public String login(@RequestParam("empWorkerId") String empWorkerId,
                        @RequestParam("password") String password,
                        @RequestParam("verifyCode") String verifyCode,
                        HttpSession session){
        if(StringUtils.isEmpty(empWorkerId) || StringUtils.isEmpty(password)){
            session.setAttribute("errorMsg", "工号或密码不能为空");
            return "admin/login";
        }
        if(StringUtils.isEmpty(verifyCode)){
            session.setAttribute("errorMsg", "验证码不能为空");
            return "admin/login";
        }
        // 检查验证码是否正确
        String kaptchaCode = session.getAttribute("verifyCode") + "";
        if(StringUtils.isEmpty(kaptchaCode) || !verifyCode.equals(kaptchaCode)){
            session.setAttribute("errorMsg", "验证码错误");
            return "admin/login";
        }
        Employee employee = employeeService.login(empWorkerId, password);
        if(employee != null){ // 有该用户
            session.setAttribute("employee", employee);
            // 设置session的最大过期时间
            session.setMaxInactiveInterval(60*60*24*7);
            // log.info("验证完毕，可登陆！");
            return "redirect:/admin/index";
        }else{
            session.setAttribute("errorMsg", "工号或密码错误");
            return "admin/login";
        }
    }

    // 跳转到博客后台管理系统首页。
    @GetMapping({"", "/", "/index", "/index.html"})
    public String index(HttpServletRequest request){
        request.setAttribute("path", "index");
        request.setAttribute("imageCount", imageRetrievalService.getTotalImages());
        request.setAttribute("videoCount", videoRetrievalService.getTotalVideos());
        request.setAttribute("fileCount", fileEntityService.getTotalFiles());
        return "admin/index";
    }

    // 普通员工修改密码
    @RequestMapping(value = "/updatePassword", method = RequestMethod.POST)
    public String updatePassword(@RequestParam("password") String password,
                                 @RequestParam("password2") String password2,
                                 HttpServletRequest request){
        if(password == null || password2 == null){
            request.setAttribute("res", "密码输入不能为空");
        }else if (password.length() < 6 || password.length() > 12 || password2.length() < 6 || password2.length() > 12){
            request.setAttribute("res", "密码输入长度需要在6-12位");
        }else if (!password.equals(password2)){
            request.setAttribute("res", "两次输入的密码必须一样");
        }else {
            // 此时修改密码
            Employee currentUser = UserInfoThreadHolder.getCurrentUser();
            currentUser.setPassword(MD5Util.MD5EnCode(password, "UTF-8"));
            int count = employeeService.updatePassword(currentUser);
            if(count > 0){
                request.setAttribute("res", "修改成功！");
            }else{
                request.setAttribute("res", "修改失败！");
            }
        }
        return "admin/updatePassword";
    }

    // 管理员修改密码
    @RequestMapping(value = "/updatePassword/admin", method = RequestMethod.POST)
    public String updatePasswordForAdmin(@RequestParam("password") String password,
                                         @RequestParam("empId") String empId,
                                         @RequestParam("password2") String password2,
                                         HttpServletRequest request){
        if(empId == null || empId.length() < 1){
            request.setAttribute("resAdmin", "请输入正确的工号！");
        } else if(password == null || password2 == null){
            request.setAttribute("resAdmin", "密码输入不能为空");
        }else if (password.length() < 6 || password.length() > 12 || password2.length() < 6 || password2.length() > 12){
            request.setAttribute("resAdmin", "密码输入长度需要在6-12位");
        }else if (!password.equals(password2)){
            request.setAttribute("resAdmin", "两次输出的密码必须一样");
        }else {
            // 此时修改密码
            Employee employee = employeeService.selectByEmpWorkerId(empId);
            if(employee == null){
                request.setAttribute("resAdmin", "查无此人！");
                return "admin/systemManagement";
            }
            employee.setPassword(MD5Util.MD5EnCode(password, "UTF-8"));
            int count = employeeService.updatePassword(employee);
            if(count > 0){
                request.setAttribute("resAdmin", "修改成功！");
            }else{
                request.setAttribute("resAdmin", "修改失败！");
            }
        }
        return "admin/updatePasswordForAdmin";
    }

    // 注册功能
    @PostMapping("/register/save")
    public String registerSave(@RequestParam("empWorkerId") String empWorkerId,
                               @RequestParam("empName") String empName,
                               @RequestParam("password") String password,
                               @RequestParam("password2") String password2,
                               @RequestParam("departmentAndGroup") String departmentAndGroup,
                               @RequestParam("verifyCode") String verifyCode,
                               HttpSession session){
        if(StringUtils.isEmpty(empWorkerId) || empWorkerId.length() < 1){
            session.setAttribute("errorMsg", "工号不能为空");
            return "admin/register";
        }
        if(StringUtils.isEmpty(empName) || empName.length() < 1){
            session.setAttribute("errorMsg", "姓名不能为空");
            return "admin/register";
        }
        if(StringUtils.isEmpty(password) || password.length() < 1){
            session.setAttribute("errorMsg", "密码不能为空");
            return "admin/register";
        }
        if(StringUtils.isEmpty(password2) || password2.length() < 1){
            session.setAttribute("errorMsg", "确认密码不能为空");
            return "admin/register";
        }
        if(!password.equals(password2)){
            session.setAttribute("errorMsg", "请确保两次输入的密码相同");
            return "admin/register";
        }
        if(StringUtils.isEmpty(departmentAndGroup) || "不能选这个".equals(departmentAndGroup) || !DepartmentAndGroup.isValid(departmentAndGroup)){
            session.setAttribute("errorMsg", "请选择正确的部门和分组");
            return "admin/register";
        }
        if(StringUtils.isEmpty(verifyCode)){
            session.setAttribute("errorMsg", "验证码不能为空");
            return "admin/register";
        }
        String kaptchaCode = session.getAttribute("verifyCode") + "";
        if(StringUtils.isEmpty(kaptchaCode) || !verifyCode.equals(kaptchaCode)){
            session.setAttribute("errorMsg", "验证码错误");
            return "admin/register";
        }
        Employee employee = employeeService.selectByEmpWorkerId(empWorkerId);
        if(employee != null){// 已经有该工号的员工信息了，无需再注册
            session.setAttribute("errorMsg", "该工号已注册，无需重复注册");
            return "redirect:/admin/login";
        }
        // 未注册过就注册一下
        Employee emp = new Employee();
        emp.setPassword(password);//密码存储加密形式
        emp.setEmpName(empName);
        emp.setEmpType((byte)2); // 不管谁先设置为普通用户
        emp.setEmpWorkerId(empWorkerId);
        emp.setJoinTime(new Date());
        String[] split = departmentAndGroup.split("\\.");
        emp.setDepartment(split[0]);
        emp.setGroup(split[1]);
        int num = employeeService.registerEmployee(emp);
        if(num < 1){
            session.setAttribute("errorMsg", "注册失败，请从新搞一下");
            return "admin/register";
        }
        session.setAttribute("successMsg", "注册成功请登录");
        return "redirect:/admin/login";
    }

    // 跳转到检测功能页面
    @GetMapping("/detectingTechnique")
    public String detectingTechnique(HttpServletRequest request){
        request.setAttribute("path", "detectingTechnique");
        return "admin/detectingTechnique";
    }
    // 跳转到信息修改页面
    @GetMapping("/modifyInformation")
    public String modifyInformation(HttpServletRequest request){
        request.setAttribute("path", "modifyInformation");
        Byte empType = UserInfoThreadHolder.getCurrentUser().getEmpType();
        if(empType == 0 || empType == 1)
            return "admin/modifyInformation";
        return "admin/index";
    }
    // 跳转到系统管理页面
    @GetMapping("/systemManagement")
    public String systemManagement(HttpServletRequest request){
        request.setAttribute("path", "systemManagement");
        return "admin/systemManagement";
    }

    /**
     * 退出登录
     * @param request
     * @return
     */
    @GetMapping("/logout")
    public String logout(HttpServletRequest request){
        request.getSession().removeAttribute("employee");
        request.getSession().removeAttribute("errorMsg");
        return "admin/login";
    }
}
