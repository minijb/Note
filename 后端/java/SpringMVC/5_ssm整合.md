![image-20220812171411790](img/image-20220812171411790.png)

## 1.搭建环境

- 建表

  ```sql
  set names utf8mb4;
  set foreign_key_checks = 0 ;
  
  create database if not exists ssmuser default character set utf8;
  use ssmuser;
  
  drop table if exists user;
  
  create table user(
      user_id varchar(255) character set utf8 collate utf8_general_ci not null default '',
      card_type varchar(255) character set utf8 collate utf8_general_ci  null default NULL,
      card_no varchar(255) character set utf8 collate utf8_general_ci  null default NULL,
      user_name varchar(255) character set utf8 collate utf8_general_ci  null default NULL,
      user_sex varchar(255) character set utf8 collate utf8_general_ci  null default NULL,
      user_age varchar(255) character set utf8 collate utf8_general_ci  null default NULL,
      user_role varchar(255) character set utf8 collate utf8_general_ci  null default NULL,
      primary key (user_id) using btree
  )engine = InnoDB character set =utf8 collate =utf8_general_ci row_format =compact ;
  
  insert into user values ('15968162097363060','身份证','114264195202156467','张三','男','30','办事和相关人员');
  insert into user values ('15968162097369997','护照','A32532654','李四','男','20','不便分类的其他人员');
  ```

- 配置pom

  ```xml
  <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.example</groupId>
    <artifactId>ssm_con</artifactId>
    <packaging>war</packaging>
    <version>1.0-SNAPSHOT</version>
    <properties>
      <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
      <maven.compiler.source>11</maven.compiler.source>
      <maven.compiler.target>11</maven.compiler.target>
    </properties>
  
    <dependencies>
      <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.13.2</version>
        <scope>test</scope>
      </dependency>
      <!-- https://mvnrepository.com/artifact/org.mybatis/mybatis -->
      <dependency>
        <groupId>org.mybatis</groupId>
        <artifactId>mybatis</artifactId>
        <version>3.5.10</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/mysql/mysql-connector-java -->
      <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>8.0.30</version>
      </dependency>
      <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-context</artifactId>
        <version>5.3.22</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/org.springframework/spring-tx -->
      <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-tx</artifactId>
        <version>5.3.22</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/org.mybatis/mybatis-spring -->
      <dependency>
        <groupId>org.mybatis</groupId>
        <artifactId>mybatis-spring</artifactId>
        <version>2.0.7</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/com.alibaba/druid -->
      <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>druid</artifactId>
        <version>1.2.11</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/org.springframework/spring-jdbc -->
      <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-jdbc</artifactId>
        <version>5.3.22</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/org.springframework/spring-aop -->
      <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-aop</artifactId>
        <version>5.3.22</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/org.springframework/spring-aspects -->
      <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-aspects</artifactId>
        <version>5.3.22</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/javax.servlet/javax.servlet-api -->
      <dependency>
        <groupId>javax.servlet</groupId>
        <artifactId>javax.servlet-api</artifactId>
        <version>4.0.1</version>
        <scope>provided</scope>
      </dependency>
      <!-- https://mvnrepository.com/artifact/com.fasterxml.jackson.core/jackson-databind -->
      <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.13.3</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/org.springframework/spring-beans -->
      <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-beans</artifactId>
        <version>5.3.22</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/com.github.miemiedev/mybatis-paginator -->
      <dependency>
        <groupId>com.github.miemiedev</groupId>
        <artifactId>mybatis-paginator</artifactId>
        <version>1.2.17</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/org.springframework/spring-webmvc -->
      <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-webmvc</artifactId>
        <version>5.3.22</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/org.springframework/spring-jms -->
  <!--    邮件处理-->
      <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-jms</artifactId>
        <version>5.3.22</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/org.springframework/spring-context-support -->
      <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-context-support</artifactId>
        <version>5.3.22</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/org.springframework/spring-test -->
      <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-test</artifactId>
        <version>5.3.22</version>
        <scope>test</scope>
      </dependency>
      <!-- https://mvnrepository.com/artifact/com.github.pagehelper/pagehelper -->
      <dependency>
        <groupId>com.github.pagehelper</groupId>
        <artifactId>pagehelper</artifactId>
        <version>5.3.1</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/jstl/jstl -->
      <dependency>
        <groupId>jstl</groupId>
        <artifactId>jstl</artifactId>
        <version>1.2</version>
      </dependency>
      <!-- https://mvnrepository.com/artifact/javax.servlet/jsp-api -->
      <dependency>
        <groupId>javax.servlet</groupId>
        <artifactId>jsp-api</artifactId>
        <version>2.0</version>
        <scope>provided</scope>
      </dependency>
      <!-- https://mvnrepository.com/artifact/org.json/json -->
      <dependency>
        <groupId>org.json</groupId>
        <artifactId>json</artifactId>
        <version>20220320</version>
      </dependency>
  
    </dependencies>
  
    <build>
      <plugins>
        <plugin>
          <groupId>org.apache.maven.plugins</groupId>
          <artifactId>maven-compiler-plugin</artifactId>
          <version>3.1</version>
          <configuration>
            <source>11</source>
            <target>11</target>
          </configuration>
        </plugin>
      </plugins>
  
      <resources>
        <resource>
          <directory>src/main/java</directory>
          <includes>
            <include>**/*.xml</include>
            <include>**/*.properties</include>
          </includes>
        </resource>
        <resource>
          <directory>src/main/resources</directory>
          <includes>
            <include>**/*.xml</include>
            <include>**/*.properties</include>
          </includes>
        </resource>
      </resources>
    </build>
  </project>
  
  ```

- 配置mybatis和spring的核心配置文件

  注：因为要将配置文件放到tomcat上，所以需要在路径上加上classpath:

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <beans xmlns="http://www.springframework.org/schema/beans"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xmlns:context="http://www.springframework.org/schema/context"
         xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context https://www.springframework.org/schema/context/spring-context.xsd">
      <!--读取属性文件-->
      <context:property-placeholder location="classpath:jdbc.properties"/>
      <!--    配置数据源-->
      <bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource">
          <property name="driverClassName" value="${jdbc.driverClassName}"/>
          <property name="url" value="${jdbc.url}"/>
          <property name="username" value="${jdbc.username}"/>
          <property name="password" value="${jdbc.password}"/>
      </bean>
      <!--    配置SqlSessionFactoryBean-->
      <bean class="org.mybatis.spring.SqlSessionFactoryBean">
          <!--    配置数据源-->
          <property name="dataSource" ref="dataSource"/>
          <!--    配置SqlMapConfig.xml-->
          <property name="configLocation" value="classpath:SqlMapConfig.xml"/>
          <!--    注册实体类-->
          <property name="typeAliasesPackage" value="org.example.pojo"/>
      </bean>
      <!--    注册mapper.xml-->
      <bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
          <property name="basePackage" value="org.example.mapper"/>
      </bean>
  </beans>
  ```

  ```xml
  <?xml version="1.0" encoding="UTF-8" ?>
  <!DOCTYPE configuration
          PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
          "http://mybatis.org/dtd/mybatis-3-config.dtd">
  <configuration>
      <!--    <properties resource="jdbc.properties"/>-->
      <settings>
          <setting name="logImpl" value="STDOUT_LOGGING"/>
      </settings>
  </configuration>
  ```

- applicationContext_service.xml

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <beans xmlns="http://www.springframework.org/schema/beans"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xmlns:context="http://www.springframework.org/schema/context" xmlns:tx="http://www.springframework.org/schema/tx"
         xmlns:aop="http://www.springframework.org/schema/aop"
         xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context https://www.springframework.org/schema/context/spring-context.xsd http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx.xsd http://www.springframework.org/schema/aop https://www.springframework.org/schema/aop/spring-aop.xsd">
  <!--    包扫描-->
      <context:component-scan base-package="org.example.service.impl"/>
  <!--    配置事务管理器-->
      <bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
  <!--        配置数据源-->
          <property name="dataSource" ref="dataSource"/>
      </bean>
  <!--    配置事务的切面-->
      <tx:advice id="myAdvice" transaction-manager="transactionManager">
          <tx:attributes>
              <tx:method name="*select*" read-only="true"/>
              <tx:method name="*find*" read-only="true"/>
              <tx:method name="*search*" read-only="true"/>
              <tx:method name="*get*" read-only="true"/>
              <tx:method name="*insert*" propagation="REQUIRED"/>
              <tx:method name="*add*" propagation="REQUIRED"/>
              <tx:method name="*save*" propagation="REQUIRED"/>
              <tx:method name="*set*" propagation="REQUIRED"/>
              <tx:method name="*update*" propagation="REQUIRED"/>
              <tx:method name="*change*" propagation="REQUIRED"/>
              <tx:method name="*modify*" propagation="REQUIRED"/>
              <tx:method name="*delete*" propagation="REQUIRED"/>
              <tx:method name="*drop*" propagation="REQUIRED"/>
              <tx:method name="*remove*" propagation="REQUIRED"/>
              <tx:method name="*clear*" propagation="REQUIRED"/>
              <tx:method name="*" propagation="SUPPORTS"/>
          </tx:attributes>
      </tx:advice>
  <!--    配置切入点+绑定-->
      <aop:config>
          <aop:pointcut id="muCut" expression="execution(* org.example.service.impl.*.*(..))"/>
          <aop:advisor advice-ref="myAdvice" pointcut-ref="muCut"/>
      </aop:config>
  </beans>
  ```
  
- springmvc.xml

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <beans xmlns="http://www.springframework.org/schema/beans"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xmlns:context="http://www.springframework.org/schema/context"
         xmlns:mvc="http://www.springframework.org/schema/mvc"
         xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context https://www.springframework.org/schema/context/spring-context.xsd http://www.springframework.org/schema/mvc https://www.springframework.org/schema/mvc/spring-mvc.xsd">
  <!--    包扫描-->
      <context:component-scan base-package="org.example.controller"/>
  <!--    注解驱动-->
      <mvc:annotation-driven/>
  <!--    全为json-->
  </beans>
  ```

- 配置web.xml,不仅仅要注册springmvc还要注册spring

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
           version="4.0">
  <!--    中文编码-->
      <filter>
          <filter-name>encode</filter-name>
          <!--  private String encoding;
      private boolean forceRequestEncoding;
      private boolean forceResponseEncoding;-->
          <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
          <init-param>
              <param-name>encoding</param-name>
              <param-value>UTF-8</param-value>
          </init-param>
          <init-param>
              <param-name>forceRequestEncoding</param-name>
              <param-value>true</param-value>
          </init-param>
          <init-param>
              <param-name>forceResponseEncoding</param-name>
              <param-value>true</param-value>
          </init-param>
      </filter>
      <filter-mapping>
          <filter-name>encode</filter-name>
          <url-pattern>/*</url-pattern>
      </filter-mapping>
  <!--    注册springmvc框架-->
      <servlet>
          <servlet-name>springmvc</servlet-name>
          <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
          <init-param>
              <param-name>contextConfigLocation</param-name>
              <param-value>classpath:springmvc.xml</param-value>
          </init-param>
      </servlet>
      <servlet-mapping>
          <servlet-name>springmvc</servlet-name>
          <url-pattern>/</url-pattern>
      </servlet-mapping>
  <!--    注册spring框架,通过监听器来启动spring-->
  <!--    还需要进行配置-->
      <listener>
          <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
      </listener>
      <context-param>
          <param-name>contextConfigLocation</param-name>
          <param-value>classpath:applicationContext_*.xml</param-value>
      </context-param>
  
  </web-app>
  ```

## encoding

### 实体类

```java
package org.example.pojo;

public class User {
    private String userId;
    private String cardType;
    private String cardNo;
    private String userName;
    private String userSex;
    private String userAge;
    private String userRole;

    public User() {
    }

    public User(String userId, String cardType, String cardNo, String userName, String userSex, String userAge, String userRole) {
        this.userId = userId;
        this.cardType = cardType;
        this.cardNo = cardNo;
        this.userName = userName;
        this.userSex = userSex;
        this.userAge = userAge;
        this.userRole = userRole;
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getCardType() {
        return cardType;
    }

    public void setCardType(String cardType) {
        this.cardType = cardType;
    }

    public String getCardNo() {
        return cardNo;
    }

    public void setCardNo(String cardNo) {
        this.cardNo = cardNo;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public String getUserSex() {
        return userSex;
    }

    public void setUserSex(String userSex) {
        this.userSex = userSex;
    }

    public String getUserAge() {
        return userAge;
    }

    public void setUserAge(String userAge) {
        this.userAge = userAge;
    }

    public String getUserRole() {
        return userRole;
    }

    public void setUserRole(String userRole) {
        this.userRole = userRole;
    }

    @Override
    public String toString() {
        return "User{" +
                "userId='" + userId + '\'' +
                ", cardType='" + cardType + '\'' +
                ", cardNo='" + cardNo + '\'' +
                ", userName='" + userName + '\'' +
                ", userSex='" + userSex + '\'' +
                ", userAge='" + userAge + '\'' +
                ", userRole='" + userRole + '\'' +
                '}';
    }
}

```

### Mapper

```java
public interface UserMapper {
    List<User> selectUserPage(
            @Param("userName") String userName,
            @Param("userSex") String userSex,
            @Param("startRow") Integer startRow);

    int insert(User user);

    int delete(String userId);

    int getRowCount(
            @Param("userName") String userName,
            @Param("userSex") String userSex);
}

```

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="org.example.mapper.UserMapper">
    <resultMap id="userMap" type="user">
        <id property="userId" column="user_id"/>
        <result property="cardType" column="card_type"/>
        <result property="cardNo" column="card_no"/>
        <result property="userName" column="user_name"/>
        <result property="userSex" column="user_sex"/>
        <result property="userAge" column="user_age"/>
        <result property="userRole" column="user_role"/>
    </resultMap>

    <sql id="allColumns">
        user_id,card_type,card_no,user_name,user_sex,user_age,user_role
    </sql>

    <select id="selectUserPage" resultMap="userMap">
        select <include refid="allColumns"/> from user
        <where>
            <if test="userName != null and userName != ''">
                and user_name like concat('%',#{userName},'%')
            </if>
            <if test="userSex != null and userSex != ''">
                and user_sex = #{userSex}
            </if>
        </where>
        limit #{startRow},5;
    </select>
    
    <insert id="insert" parameterType="user">
        insert into user values (#{userId},#{cardType},#{cardNo},#{userName},#{userSex},#{userAge},#{userRole});
    </insert>

    <delete id="delete" parameterType="string">
        delete from user where user_id = #{userId};
    </delete>

    <select id="getRowCount" resultType="int">
        select count(*) from user
        <where>
            <if test="userName != null and userName != ''">
                and user_name like concat('%',#{userName},'%')
            </if>
            <if test="userSex != null and userSex != ''">
                and user_sex = #{userSex}
            </if>
        </where>
    </select>


</mapper>
```



### Service层

```java
public interface UserService {
    List<User> selectUserPage(String userName,String userSex,int startRow);

    int createUser(User user);

    int deleteUserById(String userId);

    int getRowCount(String userName,String userSex);
}
```

impl

```java
@Service
public class UserServiceImpl implements UserService
{
    @Autowired
    UserMapper userMapper;

    @Override
    public List<User> selectUserPage(String userName, String userSex, int startRow) {
        return userMapper.selectUserPage(userName,userSex,startRow);
    }

    @Override
    public int createUser(User user) {
        return userMapper.createUser(user);
    }

    @Override
    public int deleteUserById(String userId) {
        return userMapper.deleteUserById(userId);
    }

    @Override
    public int getRowCount(String userName, String userSex) {
        return userMapper.getRowCount(userName,userSex);
    }
}

```

## 测试！！！

使用spring-test进行测试

```java
@RunWith(SpringJUnit4ClassRunner.class)//启动spring容器
@ContextConfiguration(locations = {"classpath:applicationContext_mapper.xml","classpath:applicationContext_service.xml"})
public class MyTest {
    @Autowired
    UserService userService;

    @Test
    public void testSelectUser() {
        List<User> list = userService.selectUserPage(null,"女",0);
        list.forEach(user -> System.out.println(user));
    }

    @Test
    public void testDelete() {
        int num = userService.deleteUserById("15968162097369904");
        System.out.println(num);
    }

    @Test
    public void testGetRowCount() {
        int num = userService.getRowCount(null,null);
        System.out.println(num);
    }

    @Test
    public void testCreateUser() {
        User user = new User("15968552097369903","军官证","100203123","萧山","男","30","军人");
        int num = userService.createUser(user);
        System.out.println(num);
    }
}
```

## 控制器开发

```java
@Controller
@RequestMapping("/user")
public class UserController {

    private static final int PAGE_SIZE = 5;

    @Autowired
    UserService userService;

    @RequestMapping("/selectUserPage")
    @ResponseBody
    public List<User> selectUserPage(String userName, String userSex, Integer page) {
//      根据页码计算起始行
        int startRow = 0;
        if (page != null) {
            startRow = (page - 1) * PAGE_SIZE;
        }
        return userService.selectUserPage(userName, userSex, startRow);
    }

    @RequestMapping("/getRowCount")
    @ResponseBody
    public int getRowCount(String userName,String userSex){
        return userService.getRowCount(userName,userSex);
    }

    @RequestMapping("/deleteUserById")
    @ResponseBody
    public int deleteUserById(String userId) {
        return userService.deleteUserById(userId);
    }


    @RequestMapping("/createUser")
    @ResponseBody
    public int createUser(User user){
        String userId = System.currentTimeMillis()+"";
        user.setUserId(userId);
        return userService.createUser(user);
    }
}
```

### 改造控制器，出吃跨域访问+端口修改

在控制器类上加上@CrossOrigin

