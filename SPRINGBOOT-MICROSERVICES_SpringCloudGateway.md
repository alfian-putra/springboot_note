# Spring Cloud Gateway
 [Home](README.md)

## Routing Handler

Being focused on routing requests, the Spring Cloud Gateway forwards requests to a Gateway Handler Mapping, which determines what should be done with requests matching a specific route.

Let’s start with a quick example of how the Gateway Handler resolves route configurations by using RouteLocator:

```java
@Bean
public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
    return builder.routes()
      .route("r1", r -> r.host("**.baeldung.com")
        .and()
        .path("/baeldung")
        .uri("http://baeldung.com"))
      .route(r -> r.host("**.baeldung.com")
        .and()
        .path("/myOtherRouting")
        .filters(f -> f.prefixPath("/myPrefix"))
        .uri("http://othersite.com")
        .id("myOtherID"))
    .build();
}
```
Notice how we made use of the main building blocks of this API:

- __Route__ — the primary API of the gateway. It is defined by a given identification (ID), a destination (URI) and set of predicates and filters.
- __Predicate__ — a Java 8 Predicate — which is used for matching HTTP requests using headers, methods or parameters
- __Filter__ — a standard Spring WebFilter

## Dynamic Routing

Just like Zuul, Spring Cloud Gateway provides means for routing requests to different services.

The routing configuration can be created by using pure Java (RouteLocator, as shown in the example in Section 2) or by using properties configuration:

```yaml
spring:
  application:
    name: gateway-service  
  cloud:
    gateway:
      routes:
      - id: baeldung
        uri: baeldung.com
      - id: myOtherRouting
        uri: localhost:9999
```

## Routing Factories

Spring Cloud Gateway matches routes using the Spring WebFlux HandlerMapping infrastructure. It also includes many built-in Route Predicate Factories. All these predicates match different attributes of the HTTP request. Multiple Route Predicate Factories can be combined via the logical “and”.
freestar Route matching can be applied both programmatically and via configuration properties file using a different type of Route Predicate Factories.
Our article Spring Cloud Gateway Routing Predicate Factories explores routing factories in more detail.

## WebFilter Factories

Route filters make the modification of the incoming HTTP request or outgoing HTTP response possible.
Spring Cloud Gateway includes many built-in WebFilter Factories as well as the possibility to create custom filters.
Our article Spring Cloud Gateway WebFilter Factories explores WebFilter factories in more detail.

## Spring Cloud DiscoveryClient Support

Spring Cloud Gateway can be easily integrated with Service Discovery and Registry libraries, such as Eureka Server and Consul:

```java
@Configuration
@EnableDiscoveryClient
public class GatewayDiscoveryConfiguration {
 
    @Bean
    public DiscoveryClientRouteDefinitionLocator 
      discoveryClientRouteLocator(DiscoveryClient discoveryClient) {
 
        return new DiscoveryClientRouteDefinitionLocator(discoveryClient);
    }
}
```

## Monitoring

Spring Cloud Gateway makes use of the Actuator API, a well-known Spring Boot library that provides several out-of-the-box services for monitoring the application. Once the Actuator API is installed and configured, the gateway monitoring features can be visualized by accessing /gateway/ endpoint.

## Configuration 

And now we create a simple routing configuration in the application.yml file:

```yaml
spring:
  cloud:
    gateway:
      routes:
      - id: baeldung_route
        uri: http://baeldung.com
        predicates:
        - Path=/baeldung/
management:
  endpoints:
    web:
      exposure:
        include: "*'
```

And here’s the Gateway application code:

```java
@SpringBootApplication
public class GatewayApplication {
    public static void main(String[] args) {
        SpringApplication.run(GatewayApplication.class, args);
    }
}
```

After the application starts, we can access the url “http://localhost/actuator/gateway/routes/baeldung_route” to check all routing configuration created:

```json
{
    "id":"baeldung_route",
    "predicates":[{
        "name":"Path",
        "args":{"_genkey_0":"/baeldung"}
    }],
    "filters":[],
    "uri":"http://baeldung.com",
    "order":0
}
```

We see that the relative url “/baeldung” is configured as a route. So, hitting the url “http://localhost/baeldung”, we’ll be redirected to “http://baeldung.com”, as was configured in our example.

Source :
[Link](https://www.baeldung.com/spring-cloud-gateway)

