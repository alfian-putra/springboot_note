## Eureka Server-Client Implementation on Spring Boot
 [Home](README.md)

__Service Registry__

Service discovery includes a Service Registry mechanism, which is a special service that stores the network locations of each service instance.

A service updates the service registry when instances are created or destroyed. When a client application queries the service registry, it gets a list of available instances and routes.

__Self Registration Pattern__

A service instance is responsible for registering itself with the service registry. On startup the service instance invokes the service registry's registration API to register its network location.

It is also convenient that services supply a health check, which is an endpoint that is invoked periodically to verify that the service instance is healthy and available to handle requests.

__Client-Side Discovery Pattern__

When a client wants to invoke a service, it queries the service registry to obtain a list of available instances.

Clients may use load-balancing algorithms to determine which service instance to use for each request (load-balanced requests).

## Service Registry, the Eureka Server

To include Eureka Server in our project, let’s add the cloud-starter-netflix-eureka-server dependency to the service-registry/pom.xml file.

```xml
<dependency>
    <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
    <groupId>org.springframework.cloud</groupId>
</dependency>
```

The example below shows a minimal Eureka Server application.

```java
@EnableEurekaServer
@SpringBootApplication
public class RegistryApplication {

    public static void main(String[] args) {
        SpringApplication.run(RegistryApplication.class, args);
    }
}
```

Next, we add the service registry configuration to service-registry/src/main/resources/application.yml.

```yaml
server.port: 8761

spring:
  cloud.config.enabled: false

# Standalone Eureka Server
eureka:
  instance:
    hostname: localhost
  client:
    register-with-eureka: false
    fetch-registry: false
    serviceUrl:
      defaultZone: http://${eureka.instance.hostname}:${server.port}/eureka/
```

We configure the Eureka Server in standalone mode by setting eureka.client.register-with-eureka=false and eureka.client.fetch-registry=false. This switches off the client side behavior so that it does not keep trying and failing to reach its peers.

Once you run the Eureka Server, you can open http://localhost:8761/ in your browser.

## Order Service, the Eureka Client

When a client registers with Eureka, it provides meta-data such as host, port, health indicator URL and other details.

To include the Eureka Client in our project, let’s add spring-cloud-starter-netflix-eureka-client and spring-boot-starter-actuator to order-service/pom.xml.

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

The example below shows a minimal Spring Boot application.

```java
@SpringBootApplication
public class OrdersApplication {

    public static void main(String[] args) {
        SpringApplication.run(OrdersApplication.class, args);
    }

    @Bean
    RouterFunction<ServerResponse> orders() {
        return route()
            .POST("/orders", request -> ServerResponse.accepted().build())
            .build();
    }
}
```

Here, we expose the /orders endpoint which always returns 202 Accepted as a response.

Next, we add the self-registration configuration to order-service/src/main/resources/application.yml.

```yaml
server.port: 8585

spring:
  application.name: order-service

eureka:
  server:
    host: localhost:8761
  client:
    serviceUrl:
      defaultZone: http://${eureka.server.host}/eureka
    register-with-eureka: true
    fetch-registry: false

# actuator
management:
  endpoints.web.exposure.include: health,info
  info.env.enabled: true
info:
  application.name: ${spring.application.name}
```

The default status page and status indicators of a Eureka instance are /info and /health respectively, which are the default locations of useful endpoints in a Spring Boot Actuator application.

## API Gateway, the Discovery Client

Once you have an application instance in the service registry, you can use the discovery client to look for service instances on the Eureka Server.

First, let’s add spring-cloud-starter-netflix-eureka-client and spring-boot-starter-webflux to api-gateway/pom.xml.

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
```

Next, we add the client-side discovery configuration to api-gateway/src/main/resources/application.yml.

```yaml
server.port: 9090

eureka:
  server:
    host: localhost:8761
  client:
    serviceUrl:
      defaultZone: http://${eureka.server.host}/eureka
    register-with-eureka: false
    fetch-registry: true
```

In the example below, we create a @Configuration class where we set up a load-balanced instance of WebClient.

```java
@Configuration
class WebClientConfiguration {

    @Bean
    @LoadBalanced
    WebClient webClient() {
        return WebClient.builder().build();
    }
}
```

We use the native com.netflix.discovery.EurekaClient as the service discovery client to get available service instances, as shown below.

```java
@RestController
public class OrdersServiceProxy {

    private final WebClient webClient;
    private final EurekaClient discoveryClient;

    public OrdersServiceProxy(WebClient webClient, EurekaClient discoveryClient) {
        this.webClient = webClient;
        this.discoveryClient = discoveryClient;
    }

    @PostMapping("v1/orders")
    public Mono<ResponseEntity<Void>> ordersV1(Order order) {
        
        // Implementation
        String baseUrl = 
            discoveryClient.getNextServerFromEureka("order-service", false)
                .getHomePageUrl();

        return webClient.post()
            .uri(baseUrl + "/orders")
            .body(Mono.just(order), Order.class)
            .retrieve()
            .toBodilessEntity();
    }
}
```

Source :

[Link](https://manerajona.medium.com/service-discovery-patterns-with-netflix-eureka-34d5b260aeda)