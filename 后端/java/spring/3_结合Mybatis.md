# 结合mybatis进行事务操作



主要解决的问题是将SqlSessionFactory对象交由Spring来管理，所以需要将对象生成器SqlSessionFactoryBean注册到Spring容器中，再诸如给Dao实现类完成整合。

方式：扫描的Mapper动态代理。

## 准备工作

建表

```sql
select * from users;

drop table users;

create table users(
    userid int primary key ,
    uname varchar(20),
    upass varchar(20)
);

create table accounts(
    aid int primary key ,
    aname varchar(20),
    acontent varchar(50)
);

```

Pom中的依赖

spring-aspects,spring-context,spring-tx(处理事务),mybatis-spring,druid(数据库连接池),sptring-jdbc

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>spring_example</artifactId>
    <version>1.0-SNAPSHOT</version>
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
    </properties>



    <!-- https://mvnrepository.com/artifact/junit/junit -->
    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.1</version>
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

SqlMapConfig.xml的模板和jdbc.properties

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <properties resource="jdbc.properties"/>
    <settings>
        <setting name="logImpl" value="STDOUT_LOGGING"/>
    </settings>
    <typeAliases>
        <package name="org.example.pojo"/>
    </typeAliases>
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"></transactionManager>
            <dataSource type="POOLED">
                <property name="driver" value="${jdbc.driverClassName}"/>
                <property name="url" value="${jdbc.url}"/>
                <property name="username" value="${jdbc.username}"/>
                <property name="password" value="${jdbc.password}"/>
            </dataSource>
        </environment>

    </environments>
    <mappers>
        <package name="org.example.mapper"/>
    </mappers>
</configuration>
```

applicationContext_mapper/service.xml

spring中可以取代一些mybatis中的配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context https://www.springframework.org/schema/context/spring-context.xsd">
<!--    读取属性文件jdbc.properties-->
    <context:property-placeholder location="jdbc.properties"/>
<!--    创建数据源-->
    <bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource">
        <property name="driverClassName" value="${jdbc.driverClassName}"/>
        <property name="url" value="${jdbc.url}"/>
        <property name="username" value="${jdbc.username}"/>
        <property name="password" value="${jdbc.password}"/>
    </bean>
<!--    设置SqlSessionFactoryBean-->
    <bean class="org.mybatis.spring.SqlSessionFactoryBean">
<!--        配置数据源 直接引用之前创建的dataSource-->
        <property name="dataSource" ref="dataSource"/>
<!--        MyBatis核心配置文件-->
        <property name="configLocation" value="SqlMapConfig.xml"/>
<!--        注册实体类别名-->
        <property name="typeAliasesPackage" value="org.example.pojo"/>
    </bean>
<!--    注册-->
    <bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
        <property name="basePackage" value="org.example.mapper"/>
    </bean>
</beans>
```

很多原本的设定可以不用了，只剩下settings

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
<!--    <typeAliases>-->
<!--        <package name="org.example.pojo"/>-->
<!--    </typeAliases>-->
<!--    <environments default="development">-->
<!--        <environment id="development">-->
<!--            <transactionManager type="JDBC"/>-->
<!--            <dataSource type="POOLED">-->
<!--                <property name="driver" value="${jdbc.driverClassName}"/>-->
<!--                <property name="url" value="${jdbc.url}"/>-->
<!--                <property name="username" value="${jdbc.username}"/>-->
<!--                <property name="password" value="${jdbc.password}"/>-->
<!--            </dataSource>-->
<!--        </environment>-->

<!--    </environments>-->
<!--    <mappers>-->
<!--        <package name="org.example.mapper"/>-->
<!--    </mappers>-->
</configuration>
```

applicationContext_service.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context https://www.springframework.org/schema/context/spring-context.xsd">
<!--    添加包扫描-->
    <context:component-scan base-package="org.example.service"/>
<!--    事务处理-->
</beans>
```

## 开始代码

- 实体类
- mapper层开发，同Mybatis

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="org.example.pojo.Users">
    <insert id="insert" parameterType="users">
        insert into users values (#{userid},#{uname},#{upass});
    </insert>
</mapper>
```

```java
public interface UsersMapper {
    int insert(Users users);
}
```

- service层开发

接口类

```java
public interface UserService {
    int insert(Users users);
}
```

Impl

- Impl之后会使用到所以需要进行代理
- 需要添加数据访问层的对象，因为有了spring框架的帮忙，我们就可以通过自动注入来完成之前好多代码干的事

```java
@Service
public class UserServiceImpl implements UserService {
//    注意点：需要让spring进行代理，需要添加数据访问层的对象
//    原本我们需要
//    SqlSession sqlSession;
//    SimpleDateFormat sf = new SimpleDateFormat("yyyy-MM-dd");
//
//    @Before
//    public void openSession() throws IOException {
//        InputStream in = Resources.getResourceAsStream("SqlMapConfig.xml");
//        SqlSessionFactory factory = new SqlSessionFactoryBuilder().build(in);
//        sqlSession = factory.openSession();
//    }
//
//    @After
//    public void clossSession() {
//        sqlSession.close();
//    }
//    这里我们直接autowired按照类型进行代理就好了
    @Autowired
    UsersMapper usersMapper;


    @Override
    public int insert(Users users) {
        return usersMapper.insert(users);
    }
}

```

Test

```java
    @Test
    public void TestInsert() {
        ApplicationContext ac = new ClassPathXmlApplicationContext("applicationContext.xml");
        Users users = new Users(1,"x","123456");
        UserService userService = (UserService) ac.getBean("userServiceImpl");
        int num = userService.insert(users);
        System.out.println(num);
    }
```

## Account类

基本步骤同上

service类稍微修改，之后会用

```java
@Override
public int save(Accounts accounts) {
    int num = 0;
    num = accountsMapper.save(accounts);
    System.out.println("增加"+num+"个用户");
    return num;
}
```

## 添加事务的控制

```java
@Test
public void TestSave() {
    ApplicationContext ac = new ClassPathXmlApplicationContext("applicationContext.xml");
    AccountsService accountsService = (AccountsService) ac.getBean("accountsServiceImpl");
    int num = accountsService.save(new Accounts(200, "李四", "安全"));
    System.out.println(num);
}
```

如果代码中有错误那么就事务的处理不应该可以直接成功

```xml
<!--    事务处理-->
<!--    1.添加事务管理器-->
    <bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
<!--        因为事务必须关联数据库处理，所以要配置数据源-->
        <property name="dataSource" ref="dataSource"/><!--就是之前那个数据源-->
    </bean>
<!--    2.添加注解驱动-->
<!--    就是上一步中的事务管理器-->
    <tx:annotation-driven transaction-manager="transactionManager"/>
```

这时候回滚还是没有作用

此时accountsService的类型是对应的实现类，很明显没有进行动态代理

```java
@Service
@Transactional(propagation = Propagation.REQUIRED)//设置事务管理器并设置传播特性
public class AccountsServiceImpl implements AccountsService {

    @Autowired
    AccountsMapper accountsMapper;


    @Override
    public int save(Accounts accounts) {
        int num = 0;
        num = accountsMapper.save(accounts);
        System.out.println("增加"+num+"个用户");
        return num;
    }
}

```

此时再Service层添加一个异常

```
<==    Updates: 1
Releasing transactional SqlSession [org.apache.ibatis.session.defaults.DefaultSqlSession@3af37506]
增加1个用户
Transaction synchronization deregistering SqlSession [org.apache.ibatis.session.defaults.DefaultSqlSession@3af37506]
Transaction synchronization closing SqlSession [org.apache.ibatis.session.defaults.DefaultSqlSession@3af37506]
```

spring会进行事务处理，取消本次事务，插入失败

此时accountsService是动态代理类型

### 设置不进行回滚

```java
@Service
@Transactional(propagation = Propagation.REQUIRED,noRollbackForClassName = "ArithmeticException")//设置事务管理器并设置传播特性
public class AccountsServiceImpl implements AccountsService {

    @Autowired
    AccountsMapper accountsMapper;


    @Override
    public int save(Accounts accounts) {
        int num = 0;
        num = accountsMapper.save(accounts);
        System.out.println("增加"+num+"个用户");
        System.out.println(1/0);
        return num;
    }
}
```

设置noRollbackForClassName/noRollbackFor，多个异常使用{"",""}

```java
noRollbackFor = ArithmeticException.class
```

### @Transactional详解

知道异常进行回滚

```java
rollbackForClassName = ""
```

```java
timeout = -1//永不超时
```

```java
@Transactional(propagation = Propagation.REQUIRED//设置事务管理器并设置传播特性
        ,noRollbackForClassName = "ArithmeticException",noRollbackFor = ArithmeticException.class
    ,rollbackForClassName = "",timeout = -1//永不超时，
        ,readOnly = true,//默认为false，如果是查询操作必须是True
        isolation = Isolation.DEFAULT//数据库隔离级别
)
```

