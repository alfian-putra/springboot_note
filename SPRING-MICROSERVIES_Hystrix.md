# Hystrix
 [Home](README.md)

Basically Hystrix have some functionaity with Resillience4j, and there is a note that i got from stackoverflow when someone asking which better between hystrix and Resillience4j :

"
*I can say it really does not matter which implementation you choose unless there are specific requirements that would favor a particular implementation. I would not pick anything from Netflix Hystrix as it is in maintenance mode as of 2018 (https://spring.io/blog/2018/12/12/spring-cloud-greenwich-rc1-available-now). Read the Hystrix status at GitHub: https://github.com/Netflix/Hystrix#hystrix-status.*

*Let me emphasize this: "What I find more important from the architectural point of view is to enable an environment where it is easy to replace such implementation as needed."*

*I can recommend using Spring Cloud Circuit Breaker as a framework that has a consistent API and allows developers to pick the implementation: Netflix Hystrix, reactive or non-reactive Resilience4j, Sentinel, and Spring Retry.*

*All can be configured as necessary, and all provide a basic default configuration to change value thresholds, slow call thresholds, sliding window size, etc.*
"

And in the other source i got more detail explanation that said :

"*Hystrix is an Open Source library offered by Netflix that aims to improve the resiliency of a distributed system that makes HTTP requests to communicate among its distributed components.*
*It does so by implementing the Circuit Breaker pattern.*

*Resilience4J is a standalone library inspired by Hystrix but build on the principles of Functional Programming. The most prominent difference between the two is the fact that while Hystrix embraces an Object-Oriented design where calls to external systems have to be wrapped in a HystrixCommand offering multiple functionalities, Resilience4J relies on function composition to let you stack the specific decorators you need.*

*Those decorators include of course the Circuit Breaker, but also a Rate Limiter, Retry and Bulkhead. Such decorators can be executed synchronously or asynchronously, taking full advantage of lambdas, introduced in Java 8.*"

Source :

[Link](https://stackoverflow.com/questions/70587963/resilience4j-vs-hystrix-what-would-be-the-best-for-fault-tolerance)

[Link](https://www.exoscale.com/syslog/migrate-from-hystrix-to-resilience4j/)