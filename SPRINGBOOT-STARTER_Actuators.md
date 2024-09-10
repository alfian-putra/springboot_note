# Actuators
 [Home](README.md)

1. Spring Boot Actuator module allows you to monitor your applications in 2 ways; either by leveraging HTTP endpoints or JMX (Java Management Extension). Most of the applications leverage HTTP endpoints.

2. Endpoints: Actuator module is bundled with a rich set of HTTP endpoints to monitor and interact with the application. You can even create custom endpoints to fulfil your needs, and also leverage spring-security to secure actuator endpoints. Few examples are
    - info
    - health
    - metrics
    - beans
    - caches
    - loggers
    - mappings

3. Metrics: Spring Boot Actuator provides support for a instrumentation library, called Micrometer, which is a vendor neutral application metrics facade that captures and exposes application metrics to different monitoring solutions such as Prometheus, Dynatrace, New Relic, DataDog and many more... It provides interfaces for timers, gauges, counters, distribution summaries, and long task timers with a dimensional data model.

4. Actuator module is highly (yet simply) configurable and you can utilise your application.[properties|yaml] file to meet most of your customised needs.

## Geting Started

__Import Dependency__

```xml
<dependency>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>

```
__Accessing Actuators Endpoint__

The application is started on port 8080, Let's hit '/actuator' endpoint to see all the available actuator endpoints.

There is only '/actuator/health' endpoint is exposed, By default all the other endpoints are disabled, because of security reasons, Since some of the actuator endpoints can expose sensitive data, So be careful...

Update your 'application.properties' file by setting 'management.endpoints.web.exposure.include' property

```ini
management.endpoints.web.exposure.include=*
```

'*' pattern will enable all the endpoints exposed by actuator module. But it is recommended to expose a specific set of endpoints (comma separated list) which is necessary for your operational requirement to avoid any security issues.
NOTE: 'shutdown' endpoint will still be disabled since it is highly critical for your application. It is used to gracefully shutdown your application.
Let's try by hitting 'http://localhost:8080/actuator'

```json
{
   "_links" : {
      "beans" : {
         "href" : "http://localhost:8080/actuator/beans",
         "templated" : false
      },
      "caches" : {
         "href" : "http://localhost:8080/actuator/caches",
         "templated" : false
      },
      "caches-cache" : {
         "href" : "http://localhost:8080/actuator/caches/{cache}",
         "templated" : true
      },
      "conditions" : {
         "href" : "http://localhost:8080/actuator/conditions",
         "templated" : false
      },
      "configprops" : {
         "href" : "http://localhost:8080/actuator/configprops",
         "templated" : false
      },
      "configprops-prefix" : {
         "href" : "http://localhost:8080/actuator/configprops/{prefix}",
         "templated" : true
      },
      "env" : {
         "href" : "http://localhost:8080/actuator/env",
         "templated" : false
      },
      "env-toMatch" : {
         "href" : "http://localhost:8080/actuator/env/{toMatch}",
         "templated" : true
      },
      "health" : {
         "href" : "http://localhost:8080/actuator/health",
         "templated" : false
      },
      "health-path" : {
         "href" : "http://localhost:8080/actuator/health/{*path}",
         "templated" : true
      },
      "heapdump" : {
         "href" : "http://localhost:8080/actuator/heapdump",
         "templated" : false
      },
      "info" : {
         "href" : "http://localhost:8080/actuator/info",
         "templated" : false
      },
      "loggers" : {
         "href" : "http://localhost:8080/actuator/loggers",
         "templated" : false
      },
      "loggers-name" : {
         "href" : "http://localhost:8080/actuator/loggers/{name}",
         "templated" : true
      },
      "mappings" : {
         "href" : "http://localhost:8080/actuator/mappings",
         "templated" : false
      },
      "metrics" : {
         "href" : "http://localhost:8080/actuator/metrics",
         "templated" : false
      },
      "metrics-requiredMetricName" : {
         "href" : "http://localhost:8080/actuator/metrics/{requiredMetricName}",
         "templated" : true
      },
      "scheduledtasks" : {
         "href" : "http://localhost:8080/actuator/scheduledtasks",
         "templated" : false
      },
      "self" : {
         "href" : "http://localhost:8080/actuator",
         "templated" : false
      },
      "threaddump" : {
         "href" : "http://localhost:8080/actuator/threaddump",
         "templated" : false
      }
   }
}
```
Another config can be included to actuators :

```ini
#1. Update default port for actuator endpoints
management.server.port=2121

#2. Update base-path to use **'/manage'** instead of **'/actuator'**
management.endpoints.web.base-path=/manage

#3. Following will ensure include all actuator endpoints except 'mappings' and 'heapdump'
management.endpoints.web.exposure.include=*
management.endpoints.web.exposure.exclude=mappings,heapdump

# ---
management.endpoint.health.show-details=always
# Possible values for health.show-details can be one of the following
# never|always|when_authorized
# by default it is set to 'never', 
# 'always' will display all the details,
# 'when_autorized' will display details when requesting user is autho

# ---
# Pattern: management.endpoint.{endpoint-name}.{property}=value
# property attribute can vary according to endpoint
management.endpoint.configprops.enabled=true
management.endpoint.info.enabled=false
management.endpoint.beans.cache.time-to-live=10s
management.endpoint.logfile.external-file=~/app.log

# ---
management.info.env.enabled=true

app.cusomInfo=This is Custom Info
info.app.cusomInfo=${app.cusomInfo}
info.app.java-version=${java.version}
info.app.java-vendor=${java.vendor}
info.app.excluded-actuator-enpoints=${management.endpoints.web.exposure.exclude}
## Let's now see output of '/actuator/info' endpoint:
```

Source :
[Link](https://dev.to/manojshr/spring-boot-actuators-to-expose-operational-info-2aok)