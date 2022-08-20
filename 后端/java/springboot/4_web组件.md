# web组件

## 1. 拦截器

能够连接对Controller的请求

拦截器在框架中就有，我们还可以实现自定义拦截器，实现请求的预先处理。



实现自定义拦截器：

1. 创建类实现springmvc框架的HandlerInterceptor

   ```java
   public interface HandlerInterceptor {
       default boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
           return true;
       }
   
       default void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, @Nullable ModelAndView modelAndView) throws Exception {
       }
   
       default void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, @Nullable Exception ex) throws Exception {
       }
   }
   ```

2. 在SpringMVC中声明拦截器

   ```xml
   <!--    进行拦截器的注册-->
       <mvc:interceptors>
           <mvc:interceptor>
   <!--            映射拦截的请求-->
               <mvc:mapping path="/**"/>
   <!--            配置放行的请求-->
               <mvc:exclude-mapping path="/login"/>
               <mvc:exclude-mapping path="/showLogin"/>
   <!--            配置具体的实现类-->
               <bean class="org.example.interceptor.LoginInterceptor"/>
           </mvc:interceptor>
       </mvc:interceptors>
   ```

   也可以注解通过java类来实现

   ```java
   @Configuration
   public class MyConfigure implements WebMvcConfigurer {
       @Override
       public void addInterceptors(InterceptorRegistry registry) {
   //      创建拦截器
           HandlerInterceptor interceptor = new LoginInterceptor();
           String[] path = {"/user/**"};
           String[] excludePath = {"/user/login"};
           registry.addInterceptor(interceptor).
                   addPathPatterns(path).
                   excludePathPatterns(excludePath);
   
       }
   }
   ```


## Servlet

使用Servlet对象

使用步骤：

1. 创建Servlet类，基础HttpServlet
2. 注册Servlet，让框架能找到Servlet

 创建Servlet类

```java
public class MyServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("text/html;charset=utf-8");
        PrintWriter out = resp.getWriter();
        out.println("执行的是Servlet对象");
        out.flush();
        out.close();

    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doPost(req, resp);
    }
}
```

注册servlet

```java
@Configuration
public class WebAppConfig {
    @Bean
    public ServletRegistrationBean servletRegistrationBean() {
        /*
        * public ServletRegistrationBean(T servlet, String... urlMappings)
        * public ServletRegistrationBean(T servlet, boolean alwaysMapUrl, String... urlMappings)
         * */
        ServletRegistrationBean bean = new ServletRegistrationBean(new MyServlet(), "/myServlet");
        return bean;
    }
}
```

> @Bean的作用
>
> https://blog.csdn.net/hellozhxy/article/details/120367594

也可以只用空构造器之后进行属性的添加

```java
bean.setServlet(new MyServlet());
bean.addUrlMappings("/login","/test");
```

## Filter

过滤器，可以处理请求参数，属性常用于中文编码

1. 创建FIlter
2. 进行注册

```java
public class MyFilter implements Filter {
    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        System.out.println("执行MyFilter");
        filterChain.doFilter(servletRequest,servletResponse);
    }
}

```

```java
@Configuration
public class WebAppConfig {

    @Bean
    public FilterRegistrationBean filterRegistrationBean() {
//        public FilterRegistrationBean(T filter, ServletRegistrationBean<?>... servletRegistrationBeans)
        FilterRegistrationBean bean = new FilterRegistrationBean();
        bean.setFilter(new MyFilter());
        bean.addUrlPatterns("/user/*");
        return bean;
    }
}

```

## 字符集过滤器

CharacterEncodingFilter：解决post乱码问题

在springMVC中在web.xml注册过滤器，配置其属性

在springboot中

```java
    @Bean
    public FilterRegistrationBean filterRegistrationBean() {
//        public FilterRegistrationBean(T filter, ServletRegistrationBean<?>... servletRegistrationBeans)
        FilterRegistrationBean reg = new FilterRegistrationBean();
        CharacterEncodingFilter filter = new CharacterEncodingFilter();
        filter.setEncoding("utf-8");
        filter.setForceEncoding(true);
        reg.setFilter(filter);
        reg.addUrlPatterns("/*");
        return reg;

    }
```

还需要修改application中的

```properties
server.servlet.encoding.enabled=false
```

关闭配置好的过滤器，使用自定义的

****

当然也可以直接使用系统配置的

```yaml
server:
  servlet:
    encoding:
      force: true
      charset: utf-8
      enabled: true
```

