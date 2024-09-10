# Authentication
 [Home](README.md)

Spring Security provides comprehensive support for authentication. Authentication is how we verify the identity of who is trying to access a particular resource. A common way to authenticate users is by requiring the user to enter a username and password. Once authentication is performed we know the identity and can perform authorization.

Spring Security provides built-in support for authenticating users. This section is dedicated to generic authentication support that applies in both Servlet and WebFlux environments. Refer to the sections on authentication for Servlet and WebFlux for details on what is supported for each stack.

## DispatcherServlet

When we are not using Spring Security, the request is intercepted by the DispatcherServlet. The DispatcherServlet is the front controller which intercepts any HTTP Request and forwards it to the right controller. Spring Boot automatically configures the DispatcherServlet.

The DispatcherServlet creates a WebApplicationContext, which is a specialized IOC container that is used for web applications. The WebApplicationContext is configured by the DispatcherServlet based on the configuration files.

The IOC container creates an instance of the controller beans. The DispatcherServlet will use the IOC container to lookup the controller bean and to delegate requests to it.

## Authentication Using Spring 

When Spring Security is added to the Spring Boot Application, all the request is intercepted by the Spring Security mechanism before it reaches DispatcherServlet and controller.


Source :
[link 1](https://medium.com/@aprayush20/understanding-spring-security-authentication-flow-f9bb545bd77)