# Spring IoC Container
 [Home](README.md)

Spring IoC (Inversion of Control) is the mechanism to achieve loose-coupling between Objects dependencies. To achieve loose coupling and dynamic binding of the objects at runtime, objects dependencies are injected by other assembler objects. Spring IoC container is the program that injects dependencies into an object and make it ready for our use. We have already looked how we can use Spring Dependency Injection to implement IoC in our applications. Spring IoC container classes are part of org.springframework.beans and org.springframework.context packages. Spring IoC container provides us different ways to decouple the object dependencies. BeanFactory is the root interface of Spring IoC container.

# Spring Bean

Spring Bean is nothing special, any object in the Spring framework that we initialize through Spring container is called Spring Bean. Any normal Java POJO class can be a Spring Bean if it’s configured to be initialized via container by providing configuration metadata information.

# Spring Bean Scope

__singleton__ - Only one instance of the bean will be created for each container. This is the default scope for the spring beans. While using this scope, make sure bean doesn’t have shared instance variables otherwise it might lead to data inconsistency issues.

__prototype__ - A new instance will be created every time the bean is requested.

__request__ - This is same as prototype scope, however it’s meant to be used for web applications. A new instance of the bean will be created for each HTTP request.

__session__ - A new bean will be created for each HTTP session by the container.

__global-session__ - This is used to create global session beans for Portlet applications.

# Spring Bean Configuration

__Annotation Based Configuration__ - By using @Service or @Component annotations. Scope details can be provided with @Scope annotation.

__XML Based Configuration__ - By creating Spring Configuration XML file to configure the beans. If you are using Spring MVC framework, the xml based configuration can be loaded automatically by writing some boiler plate code in web.xml file.

__Java Based Configuration__ - Starting from Spring 3.0, we can configure Spring beans using java programs. Some important annotations used for java based configuration are @Configuration, @ComponentScan and @Bean.

# Using @Configuration 

So we are going to create the spring beans using the @Bean annotation. But how? Where to write these methods? As we have discussed at the beginning that “@Configuration annotation indicates that the class has @Bean definition methods”, so let’s explain this statement and create our beans inside the CollegeConfig.java file using the @Bean annotation. So we can write something like this inside our CollegeConfig.java file. Please refer to the comments for a better understanding. 

```java
// Java Program to Illustrate Configuration Class 

package BeanAnnotation;

// Importing required classes 
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class CollegeConfig {

    // Using Bean annotation to create
    // College class Bean
    @Bean
    // Here the method name is the
    // bean id/bean name
    public College collegeBean() {
    
        // Return the College object
        return new College();
    }

}
```

Source : [link](https://www.digitalocean.com/community/tutorials/spring-ioc-bean-example-tutorial)