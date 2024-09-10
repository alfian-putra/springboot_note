# Sleuth
 [Home](README.md)

Sleuth configures everything you need to get started. This includes where trace data (spans) are reported to, how many traces to keep (sampling), if remote fields (baggage) are sent, and which libraries are traced.

Specifically, Spring Cloud Sleuth…​

- Adds trace and span ids to the Slf4J MDC, so you can extract all the logs from a given trace or span in a log aggregator.

- Instruments common ingress and egress points from Spring applications (servlet filter, rest template, scheduled actions, message channels, feign client).

- If spring-cloud-sleuth-zipkin is available then the app will generate and report Zipkin-compatible traces via HTTP. By default it sends them to a Zipkin collector service on localhost (port 9411). Configure the location of the service using spring.zipkin.baseUrl.

## Getting Started

### Controller

Create a simple controller that exposes an endpoint:

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.sleuth.Span;
import org.springframework.cloud.sleuth.Tracer;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SleuthDemoController {

    private final Logger logger = LoggerFactory.getLogger(SleuthDemoController.class);

    @Autowired
    private Tracer tracer;

    @GetMapping("/hello")
    public String hello() {
        Span currentSpan = tracer.currentSpan();
        String correlationId = currentSpan.context().traceId();
        logger.info("Handling hello request with trace ID: {}", correlationId);
        return "Hello from Sleuth Demo!";
    }
}
```

In this code snippet, a Tracer bean provided by Spring Cloud Sleuth is used to obtain the current Span, which represents a unit of work in a distributed trace. The trace ID, extracted from the current span's context, is then assigned to the correlationId variable. Finally, this trace ID is logged using a logger with an informational message indicating the handling of a "hello" request, providing visibility into the trace context of the operation. The method returns a simple greeting message, showcasing the integration of distributed tracing capabilities in the Sleuth-enabled Spring Boot application.

### Test

Run your microservice application. Make a GET request to http://localhost:8080/hello using your preferred tool (e.g., a web browser or cURL). Check the console logs of your microservice. You should see log entries with trace information.

### Output

The trace information is typically sent to your logs. In a real-world scenario, logs would be aggregated centrally. However, for this example, you can observe the trace information in your microservice’s console logs. The log entry should look similar to this:

```log
2023-04-04 15:30:45.789  INFO [sleuth-demo-service,traceId=7d483a8cd4e57d42,spanId=7d483a8cd4e57d42,parentId=,exportable=true] 9888 --- [nio-8080-exec-1] c.e.sleuthdemo.SleuthDemoController      : Handling hello request with trace ID: 7d483a8cd4e57d42
```

In this log entry, the trace ID (7d483a8cd4e57d42) is associated with the handling of the "hello" request.

## Log Aggregation

Log aggregation, a critical aspect of monitoring distributed systems, involves consolidating logs from various microservices into a central repository for streamlined analysis. Spring Cloud Sleuth seamlessly integrates with log aggregation solutions, such as the ELK Stack (Elasticsearch, Logstash, Kibana), enhancing trace visibility and enabling efficient troubleshooting across microservices.

- Step 1

    To enable Sleuth and the ELK Stack integration, add the following dependencies to your Spring Boot project’s pom.xml:

    <dependency>
        <groupId>net.logstash.logback</groupId>
        <artifactId>logstash-logback-encoder</artifactId>
        <version>6.6</version>
    </dependency>

    Logstash Logback encoder formats logs in a way that is compatible with Logstash.
- Step 2

    Create a logback-spring.xml file in the src/main/resources directory to configure Logback:

    ```xml
    <configuration>
        <include resource="org/springframework/boot/logging/logback/base.xml"/>
        <appender name="LOGSTASH" class="net.logstash.logback.appender.LogstashTcpSocketAppender">
            <!-- Logstash server host and port -->
            <destination>localhost:5000</destination>
            <!-- Encoder to format the log messages -->
            <encoder class="net.logstash.logback.encoder.LogstashEncoder"/>
        </appender>
        <!-- Attach the appender to the root logger -->
        <root level="INFO">
            <appender-ref ref="LOGSTASH"/>
        </root>
    </configuration>
    ```

    This configuration sends logs to Logstash via TCP on localhost:5000.

- Step 3

    Run the ELK Stack using Docker by creating a docker-compose.yml file:

    ```yaml
    version: '3'
    services:
    elasticsearch:
        image: docker.elastic.co/elasticsearch/elasticsearch:7.15.1
        environment:
        - discovery.type=single-node
    logstash:
        image: docker.elastic.co/logstash/logstash:7.15.1
        volumes:
        - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
        ports:
        - "5000:5000"
    kibana:
        image: docker.elastic.co/kibana/kibana:7.15.1
        ports:
        - "5601:5601"
        depends_on:
        - elasticsearch
    ```

    This Docker Compose file defines three services: Elasticsearch, Logstash, and Kibana. Elasticsearch, a distributed search and analytics engine, is configured to run as a single node. Logstash, a log processing pipeline, is set up with a volume mount for a Logstash configuration file and exposes port 5000. Kibana, a visualization and exploration platform, is configured to run on port 5601 and depends on the Elasticsearch service to be available before starting. This configuration is a basic setup for the ELK (Elasticsearch, Logstash, Kibana) Stack, commonly used for log aggregation and analysis in distributed systems.

- Step 4

    Create a logstash.conf file in the same directory with the following content:

    ```ini
    input {
    tcp {
        port => 5000
    }
    }

    output {
    elasticsearch {
        hosts => ["elasticsearch:9200"]
        index => "spring-cloud-sleuth-%{+YYYY.MM.dd}"
    }
    }
    ```

    This is a Logstash configuration file specifying an input and output configuration. The input section defines a TCP input on port 5000, indicating Logstash should listen for logs arriving via TCP. The output section configures Logstash to forward processed logs to Elasticsearch at the specified hosts and to index them under the pattern “spring-cloud-sleuth-%{+YYYY.MM.dd}” with daily rolling indices based on the current date.

- Step 4

    Start the ELK Stack:

    ```
    docker-compose -f docker-compose.yml up
    ```

    Run the Spring Boot application. Logs generated by Sleuth will be sent to Logstash and stored in Elasticsearch.

- Step 5

    Access Kibana at http://localhost:5601. Set up an index pattern matching the one specified in the Logstash configuration (spring-cloud-sleuth-*). You can now explore and visualize logs in Kibana.

    Source :

    [Link](https://spring.io/projects/spring-cloud-sleuth)
    
    [Link](https://medium.com/@bubu.tripathy/distributed-tracing-with-spring-cloud-sleuth-and-zipkin-9106c8afd349)