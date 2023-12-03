package com.ssj.sfwebsystem.interceptor;

import com.ssj.sfwebsystem.config.UserInfoThreadHolder;
import com.ssj.sfwebsystem.entity.Employee;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * 后台系统身份验证拦截器
 */
@Component
public class AdminLoginInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String requestServletPath = request.getServletPath();
        if(requestServletPath.startsWith("/admin") && null == request.getSession().getAttribute("employee")){
            request.getSession().setAttribute("errorMessage", "请重新登录");
            response.sendRedirect(request.getContextPath() + "/admin/login");
            return false;
        }else{
            // 验证通过
            request.getSession().removeAttribute("errorMessage");
            Employee employee = (Employee)request.getSession().getAttribute("employee");
            UserInfoThreadHolder.addCurrentUser(employee);
            return true;
        }
//        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        UserInfoThreadHolder.remove();
    }
}
