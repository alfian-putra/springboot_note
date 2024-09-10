# Annotations
 [Home](README.md)


## Framework Annotations

__@Configuration__ : Used to indicate that a class declares one or more @Bean methods. These classes are processed by the Spring container to generate bean definitions and service requests for those beans at runtime.

__@Bean__ : Indicates that a method produces a bean to be managed by the Spring container. This is one of the most used and important spring annotation. @Bean annotation also can be used with parameters like name, initMethod and destroyMethod.

__@PreDestroy__ and __@PostConstruct__ are alternative way for bean initMethod and destroyMethod. It can be used when the bean class is defined by us. For example;

__@ComponentScan__ : Configures component scanning directives for use with @Configuration classes. Here we can specify the base packages to scan for spring components.

__@Component__ : Indicates that an annotated class is a “component”. Such classes are considered as candidates for auto-detection when using annotation-based configuration and classpath scanning.

__@PropertySource__ : provides a simple declarative mechanism for adding a property source to Spring’s Environment. There is a similar annotation for adding an array of property source files i.e @PropertySources.

__@Service__ : Indicates that an annotated class is a “Service”. This annotation serves as a specialization of @Component, allowing for implementation classes to be autodetected through classpath scanning.

__@Repository__ : Indicates that an annotated class is a “Repository”. This annotation serves as a specialization of @Component and advisable to use with DAO classes.

__@Autowired__ : Spring @Autowired annotation is used for automatic injection of beans. Spring @Qualifier annotation is used in conjunction with Autowired to avoid confusion when we have two of more bean configured for same type.

## MVC Annotations


__@Controller__

__@RequestMapping__

__@PathVariable__

__@RequestParam__

__@ModelAttribute__

__@RequestBody__ and __@ResponseBody__

__@RequestHeader__ and __@ResponseHeader__

## Spring Transaction Management Annotations

__@EnableWebSecurity__ is used with @Configuration class to have the Spring Security configuration defined

## Spring Boot Annotations

__@SpringBootApplication__

__@EnableAutoConfiguration__


source : [link](https://www.digitalocean.com/community/tutorials/spring-annotations)