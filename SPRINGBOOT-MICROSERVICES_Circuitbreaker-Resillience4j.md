## Circuit Breaker (Resillience4j)
 [Home](README.md)

You may have already heard of circuit breakers we find in electronic items. What is the main purpose of it? __Simply, break the electric flow in an unexpected scenario__. Same as that, here also this micro service pattern has go the name due to the same nature it has.

This pattern comes into the picture while communicating between services. Let’s take a simple scenario. Let’s say we have two services: Service A and B. Service A is calling Service B(API call) to get some information needed. When Service A is calling to Service B, if Service B is down due to some infrastructure outage, what will happen? Service A is not getting a result and it will be hang by throwing an exception. Then another request comes and it also faces the same situation. Like this request threads will be blocked/hanged until Service B is coming up! As a result, the network resources will be exhausted with low performance and bad user experience. Cascading failures also can happen due to this.

In such scenarios, we can use this Circuit Breaker pattern to solve the problem. It is giving us a way to handle the situation without bothering the end user or application resources.

## Life Cycle of Pattern States 

There are 3 main states discussed in Circuit Breaker pattern. They are:

- CLOSED
When both services which are interacting are up and running, circuit breaker is CLOSED. Circuit breaker is counting the number of remote API calls continuously.

- OPEN
As soon as the percentage of failing remote API calls is exceeding the given threshold, circuit breaker changes its state to OPEN state. Calling micro service will fail immediately, and an exception will be returned. That means, the flow is interrupted.

- HALF OPEN
After staying at OPEN state for a given timeout period, breaker automatically turns its state into HALF OPEN state. In this state, only a LIMITED number of remote API calls are allowed to pass through. If the failing calls count is greater than this limited number, breaker turns again into OPEN state. Otherwise it is CLOSED.

## What is Resilience4j?

Resilience4j is a lightweight, easy-to-use fault tolerance library inspired by
Netflix Hystrix. It provides various features.

- Circuit Breaker — fault tolerance
- Rate Limiter — block too many requests
- Time Limiter — limit time while calling remote operations
- Retry Mechanism — automatic retry for failed operations
- Bulkhead — limit number of concurrent requests
- Cache — store results of costly remote operations

## Example Scenaryo

By implementing a circuit breaker pattern, you can mitigate the impact of such failures and introduce a fallback mechanism. Here’s how it works:

1. Normal Operation:
During normal operation, when the external API is up and running, the circuit breaker remains in a closed state, allowing requests to flow through seamlessly. Your application retrieves the list of countries from the external API and serves the data to the users.

2. Failure Detection:
If the external API experiences issues and starts responding with errors or becomes unresponsive, the circuit breaker detects this abnormal behavior by monitoring the failure rate or response times. Once the predefined threshold is exceeded, the circuit breaker trips, transitioning to an open state.

3. Fallback Mechanism:
When the circuit breaker is in the open state, instead of allowing requests to reach the failing external API, it redirects them to a fallback method or a pre-defined response. In the context of our example, the fallback method could be retrieving a cached version of the country list or providing a default list.

4. Automatic Recovery:
To periodically check if the external API has recovered, the circuit breaker allows a limited number of requests to pass through after a certain duration. If these requests are successful, indicating that the external API is functioning again, the circuit breaker transitions back to the closed state, resuming normal operations. However, if the requests continue to fail, the circuit breaker remains open to prevent further damage.

## Getting Started with Resillience4J

### Dependeny

```xml
<dependency>
   <groupId>io.github.resilience4j</groupId>
   <artifactId>resilience4j-spring-boot3</artifactId>
   <version>2.0.2</version>
 </dependency>
 <dependency>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-starter-aop</artifactId>
 </dependency>
 ```

 ### configurations in the applications.yml file.

```yaml
spring:
  application.name: CircuitBreakerDemo
  jackson.serialization.indent_output: true

management:
  endpoints.web.exposure.include:
    - '*'
  endpoint.health.show-details: always
  health.circuitbreakers.enabled: true

resilience4j.circuitbreaker:
  configs:
    default:
      registerHealthIndicator: true
      slidingWindowSize: 10
      minimumNumberOfCalls: 5
      permittedNumberOfCallsInHalfOpenState: 3
      automaticTransitionFromOpenToHalfOpenEnabled: true
      waitDurationInOpenState: 5s
      failureRateThreshold: 50
      eventConsumerBufferSize: 10
```

Given below is a simple explanation of parameters that we have configured.

- __resilience4j.circuitbreaker__: This specifies the configuration for the circuit breaker module of Resilience4j.
- __configs__: This defines the different circuit breaker configurations. In this case, there is a single configuration named "default".
- __registerHealthIndicator__: This parameter determines whether to register a health indicator for the circuit breaker. It allows monitoring the circuit breaker's health status.
- __slidingWindowSize__: This sets the size of the sliding window used by the circuit breaker to track the success and failure rates of calls.
- __minimumNumberOfCalls__: This specifies the minimum number of calls required within the sliding window before the circuit breaker can calculate the success or failure rate.
- __permittedNumberOfCallsInHalfOpenState__: This sets the maximum number of calls allowed when the circuit breaker is in the half-open state. If this limit is exceeded, the circuit breaker transitions back to the open state.
- __automaticTransitionFromOpenToHalfOpenEnabled__: This parameter enables or disables automatic transition from the open state to the half-open state when the wait duration in the open state has passed.
- __waitDurationInOpenState__: This determines the duration that the circuit breaker remains in the open state before transitioning to the half-open state. In this case, it is set to 5 seconds.
- __failureRateThreshold__: This sets the failure rate threshold in percentage. If the failure rate exceeds this threshold within the sliding window, the circuit breaker transitions to the open state.
- __eventConsumerBufferSize__: This parameter determines the size of the buffer used by the event consumer for tracking circuit breaker events.

### Code Implementation

```java
@GetMapping("/countries")
    @CircuitBreaker(name = "countriesCircuitBreaker", fallbackMethod = "getCountries")
    public List<Object> getCountries() throws Exception {
        return countriesService.getCountries();
    }

    public List<Object> getCountries(Throwable throwable) {
        List<Object> countries = new ArrayList<>();
        countries.add("Country service unavailable!");
        return countries;
    }
```

Here we can see that when the external service is unavailable it returns a message “Country service unavailable!”.

```
Note : The fallback method should have the same parameter list and return type as the circuit breaker method.
```

These are the controller and service classes that I have utilized.

```java
package com.maheshbabu.circuitbreaker.controller;

import com.maheshbabu.circuitbreaker.service.CountriesService;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;

@RestController
public class CountriesController {


    private final CountriesService countriesService;

    public CountriesController(CountriesService countriesService) {
        this.countriesService = countriesService;
    }

    @GetMapping("/countries")
    @CircuitBreaker(name = "countriesCircuitBreaker", fallbackMethod = "getCountries")
    public List<Object> getCountries() throws Exception {
        return countriesService.getCountries();
    }

    public List<Object> getCountries(Throwable throwable) {
        List<Object> countries = new ArrayList<>();
        countries.add("Country service unavailable!");
        return countries;
    }

}
```
---
```java
package com.maheshbabu.circuitbreaker.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.List;

@Service
public class CountriesService {

    private final RestTemplate restTemplate;

    public CountriesService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public List<Object> getCountries() throws Exception {
        Object[] countries = null;
        try {
            countries = restTemplate.getForObject("https://restcountries.com/v3.1/all", Object[].class);
        } catch (Exception e) {
            throw new Exception("Failed to fetch countries from the API");
        }
        return Arrays.stream(countries).toList().subList(1, 10);
    }
}
```
Source :

[Link](https://medium.com/spring-boot/exploring-resilience4j-enhancing-circuit-breaker-patterns-for-robust-applications-6cb8093d0b9)
[Link](https://salithachathuranga94.medium.com/micro-service-patterns-circuit-breaker-with-spring-boot-253e4a829f94)
