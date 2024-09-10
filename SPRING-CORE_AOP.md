# Aspect-Oriented Programming (AOP)
 [Home](README.md)

Aspect-Oriented Programming (AOP) is a programming paradigm that enables the modularization of cross-cutting concerns in software applications. Cross-cutting concerns are aspects of your application that affect multiple parts of the codebase. These can include logging, security, transactions, and error handling. AOP allows you to separate these concerns from the core application logic, making your code more maintainable and less cluttered.

## Creating Aspects

In Spring, you can create aspects by defining a class annotated with @Aspect. This class should contain advice methods. For example:

```java
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;

@Aspect
public class LoggingAspect {

    @Before("execution(* com.example.demo.*.*(..))")
    public void logBefore() {
        System.out.println("Before method execution");
    }
}
```

In this example, the LoggingAspect class contains a @Before advice that logs a message before the execution of any method in the com.example.demo package.

## Writing Advices

Spring supports different types of advice:

__@Before__ : Runs before the join point.

__@After__ : Runs after the join point.

__@Around__ : Wraps around the join point, allowing you to modify its behavior.

```java
@Around("execution(* com.example.service.*.*(..)) && args(arg1, arg2)")
public Object customAroundAdvice(ProceedingJoinPoint joinPoint, Object arg1, Object arg2) {
    // Custom around advice logic
    return joinPoint.proceed();
}
```
__@AfterThrowing__ : Runs if an exception is thrown at the join point.
The @Before advice in our example logs a message before a method is executed. Here’s a brief explanation of advice types:

Source : [link](https://naveen-metta.medium.com/deep-dive-into-aspect-oriented-programming-aop-in-spring-and-spring-boot-afcb29141cbd)