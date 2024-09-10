# OpenFeign
 [Home](README.md)

OpenFeign is an open-source project that was originally developed by Netflix and then moved to the open-source community. Feign is a declarative rest client that creates a dynamic implementation of the interface that’s declared as FeignClient. Writing web services with the help of FeignClient is very easier. __FeignClient is mostly used to consume REST API endpoints which are exposed by third-party or microservice.__

## Dependency

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

## Include Feign

```java
@SpringBootApplication
@EnableFeignClients
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

}
```

Create an Interface and annotate it with @FeignClient and declare your calling methods like below

```java
@FeignClient(name = "giveYourServiceName", url = "provideYourUrlHere", path = "provideYourContextPathHere")
public interface AddressClient {

    @GetMapping("/address/{id}")
    public ResponseEntity<AddressResponse> getAddressByEmployeeId(@PathVariable("id") int id);

}
```
---
```java


package com.gfg.employeaap.feignclient;
 
import com.gfg.employeaap.response.AddressResponse;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
 
@FeignClient(name = "address-service", url = "http://localhost:8081", path = "/address-service")
public interface AddressClient {
 
    @GetMapping("/address/{id}")
    public ResponseEntity<AddressResponse> getAddressByEmployeeId(@PathVariable("id") int id);
 
}
```

## Deep Dive

1. Here’s an example of how to create a Feign client interface to interact with a “Product Catalog” microservice:

    ```java
    @FeignClient(name = "product-catalog")
    public interface CatalogServiceClient {
    @GetMapping("/catalog/{productId}")
    ProductDTO getProduct(@PathVariable("productId") Long productId);

    @PostMapping("/catalog")
    ProductDTO createProduct(@RequestBody ProductDTO product);

    @PutMapping("/catalog/{productId}")
    ProductDTO updateProduct(@PathVariable("productId") Long productId, @RequestBody ProductDTO product);
    
    @DeleteMapping("/catalog/{productId}")
    void deleteProduct(@PathVariable("productId") Long productId);

    }
    ```

    __NOTE : In this example, CatalogServiceClient is a Feign client interface that resembles the API of the “product catalog” microservice. You can use these methods to interact with the user service without writing the HTTP request and response handling code.__

2. Annotation-Driven Development: OpenFeign uses annotations like @ GetMapping, @PostMapping, and @PathVariable to define HTTP endpoints. This approach is more concise and readable than manually building URLs and request bodies, reducing the chances of errors.

3. Automatic Serialization/Deserialization: Spring Cloud OpenFeign automatically handles the serialization of Java objects to JSON (or other formats) for request bodies and the deserialization of responses. With RestTemplate, you often need to handle this serialization/deserialization manually.

4. Integrates with Service Discovery: OpenFeign seamlessly integrates with service discovery and load balancing provided by tools like Eureka and Ribbon. It allows you to refer to services by their names rather than specific host and port, which is essential in a microservices architecture.
    ```java
    @FeignClient(name = "product-catalog")
    public interface CatalogServiceClient {
        // ...
    }
    ```
    When you make requests through CatalogServiceClient, Spring Cloud OpenFeign will automatically resolve the host and port of the “product-catalog” from the service discovery registry. This ensures load balancing and failover, distributing requests to available instances of the service

5. Fallback and Resilience: OpenFeign provides built-in support for defining fallback methods, allowing you to gracefully handle service failures. This enhances the resilience of your application, automatically using fallback logic when the target service is unavailable.

    ```java
    @FeignClient(name = "order-service", fallback = OrderServiceFallback.class)
    public interface OrderServiceClient {

        @GetMapping("/orders/{orderId}")
        OrderDTO getOrder(@PathVariable("orderId") Long orderId);
    }
    ```

    In this example, if the “Order Service” is unavailable or encounters an error, the OrderServiceFallback class will be used to handle the fallback logic. This could include returning a default response or logging the failure.

    ```java
    @Component
    public class OrderServiceFallback implements OrderServiceClient {

        @Override
        public OrderDTO getOrder(Long orderId) {
            // Fallback logic: Return a default response or handle the error gracefully.
            return new OrderDTO();
        }
    }
    ```

6. Request/Response Compression: OpenFeign supports request and response compression out-of-the-box, reducing network overhead and improving performance, which you would have to configure manually when using RestTemplate.

    ```ini
    feign.compression.request.enabled=true
    feign.compression.response.enabled=true
    ```

7. Consistency and Code Reusability: By creating a Feign client interface, you ensure that all service interactions are consistent, as they share the same API definition. This promotes code reusability and reduces the chances of inconsistencies in the way different parts of your application interact with the service.

8. Simplified Testing: Feign clients are easy to mock and use in unit tests, making it simpler to test your application’s interactions with external services.

9. Ecosystem Integration: OpenFeign is a part of the Spring Cloud ecosystem, making it a natural choice if you are already using Spring Boot and other Spring Cloud components in your application. It integrates seamlessly with other Spring features.

10. HTTP/2 Support : The Java HTTP Client supports both HTTP/1.1 and HTTP/2. By default the client will send requests using HTTP/2. Requests sent to servers that do not yet support HTTP/2 will automatically be downgraded to HTTP/1.1. Here’s a summary of the major improvements that HTTP/2 brings:

    - Header Compression. HTTP/2 uses HPACK compression, which reduces overhead.
    - Single Connection to the server, reduces the number of round trips needed to set up multiple TCP connections.
    - Multiplexing. Multiple requests are allowed at the same time, on the same connection.
    - Server Push. Additional future needed resources can be sent to a client.
Binary format. More compact.

    To use HTTP/2 with a Spring Feign client, you’ll need to configure Feign and your Spring application properly. HTTP/2 is a major update to the HTTP protocol, and it’s supported in Java starting from Java 9. Here are the steps to configure a Spring Feign client to use HTTP/2:

    1. Ensure Java Version: Make sure you are using a Java version that supports HTTP/2. Java 9 and later versions have built-in support for HTTP/2. If you are using an older version, you should consider upgrading to a supported version.
    2. Configure Feign Client: In your Spring application, you should configure the Feign client to use HTTP/2. You can do this by creating a Feign configuration class:

        ```java
        import feign.Client;
        import feign.http2client.Http2Client;
        import org.springframework.cloud.openfeign.FeignClientsConfiguration;
        import org.springframework.context.annotation.Bean;
        import org.springframework.context.annotation.Configuration;

        @Configuration
        public class FeignHttp2Config extends FeignClientsConfiguration {
            @Bean
            public Client feignClient() {
                return new Http2Client();
            }
        }
        ```
    3. Configure HTTP/2 for Tomcat: Spring Boot’s embedded Tomcat server also needs to be configured for HTTP/2 support. You can enable it by setting the following property in your application.properties or application.yml:

        ```ini
        server.http2.enabled=true
        ```

        While Spring Cloud OpenFeign offers these advantages, it’s essential to consider the specific requirements of your project and whether these benefits align with your use case. In some cases, using RestTemplate or manual HTTP calls might be more appropriate, but for many modern microservices-based applications, Spring Cloud OpenFeign simplifies and streamlines the process of interacting with other services.

Source :

[Link](https://www.geeksforgeeks.org/spring-cloud-openfeign-with-example-project/)

[Link](https://www.geeksforgeeks.org/spring-boot-microservices-communication-using-feignclient-with-example/)

[Link](https://medium.com/@timiolowookere/using-spring-cloud-openfeign-for-inter-service-communication-418ef79de3d0)