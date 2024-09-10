# Autoconfiguration
 [Home](README.md)

Spring Boot auto-configuration automatically configures the Spring application based on the jar dependencies that we have added. For example, if the H2 database Jar is present in the classpath and we have not configured any beans related to the database manually, the Spring Boot's auto-configuration feature automatically configures it in the project.

Auto-configuration works by examining the artifacts on your application’s classpath and triggering configuration templates (known as auto-configuration classes). These templates are conditionally applied based on the presence or absence of specific classes or beans in the classpath and the context. Spring Boot uses a series of @Conditional annotations to control the activation of auto-configurations. For example:

__@ConditionalOnClass__: Activates a configuration if specified classes are present in the classpath.

__@ConditionalOnMissingBean__: Ensures a configuration is applied only if a particular bean is not already defined.

__@ConditionalOnProperty__: Checks for specific environment properties before applying a configuration.





Source :

[Link (complete guide)](https://www.marcobehler.com/guides/spring-boot-autoconfiguration)
[Link](https://www.javatpoint.com/spring-boot-auto-configuration)