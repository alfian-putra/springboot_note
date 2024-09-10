# MVC (Model View Controller)
 [Home](README.md)

The Spring Web MVC framework provides Model-View-Controller (MVC) architecture and ready components that can be used to develop flexible and loosely coupled web applications. The MVC pattern results in separating the different aspects of the application (input logic, business logic, and UI logic), while providing a loose coupling between these elements.



__The Model__ encapsulates the application data and in general they will consist of POJO.

__The View__ is responsible for rendering the model data and in general it generates HTML output that the client's browser can interpret.

__The Controller__ is responsible for processing user requests and building an appropriate model and passes it to the view for rendering.

## Create the controller class

```java
package com.javatpoint;  
import org.springframework.stereotype.Controller;  
import org.springframework.web.bind.annotation.RequestMapping;  
@Controller  
public class HelloController {  

    @RequestMapping("/")  
    public String display() {  
        return "index";  
    }     

    @RequestMapping("/rest")
    public String healthCheck() {
        return "OK";
    }
}  
```

Source :

[Spring MVC](https://www.javatpoint.com/spring-mvc-tutorial)
[Spring Controller](https://www.digitalocean.com/community/tutorials/spring-controller-spring-mvc-controller)