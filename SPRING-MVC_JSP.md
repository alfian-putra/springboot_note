# Jakarta Server Page
 [Home](README.md)

In Java, JSP stands for Jakarta Server Pages( (JSP; formerly JavaServer Pages)). It is a server-side technology that is used for creating web applications. It is used to create dynamic web content. __JSP consists of both HTML tags and JSP tags. In this, JSP tags are used to insert JAVA code into HTML pages.__ It is an advanced version of Servlet Technology i.e. a web-based technology that helps us to create dynamic and platform-independent web pages. In this, Java code can be inserted in HTML/ XML pages or both. JSP is first converted into a servlet by the JSP container before processing the client’s request. JSP has various features like JSP Expressions, JSP tags, JSP Expression Language, etc.

## Dependency

```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-thymeleaf</artifactId>
        </dependency>
        <dependency>
            <groupId>org.apache.tomcat.embed</groupId>
            <artifactId>tomcat-embed-jasper</artifactId>
        </dependency>
        <!-- JSTL for JSP -->
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>jstl</artifactId>
```

## Controller

```java
package net.javaguides.springboot.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class HelloController {

    @GetMapping({
        "/",
        "/hello"
    })
    public String hello(@RequestParam(value = "name", defaultValue = "World",
        required = true) String name, Model model) {
        model.addAttribute("name", name);
        return "hello";
    }
}
```


## JSP ViewResolver Configuration in application.properties file
```ini
spring.mvc.view.prefix=/WEB-INF/jsp/
spring.mvc.view.suffix=.jsp
```

## Create JSP page
Let's create a simple JSP page under webapp/WEB-INF/jsp folder structure. If webapp folder not exists then create webapp/WEB-INF/jsp folder structure and then create JSP pages under it.

```xml
<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="ISO-8859-1">
<title>Insert title here</title>
</head>
<body>
     <h2 align="center"> Hello ${name}!</h2>
</body>
</html>
```



Source :

[What is JSP ?](https://www.geeksforgeeks.org/introduction-to-jsp/)

[Implementation](https://medium.com/@dsforgood/configuring-jsp-in-spring-boot-application-81ea7336a082)