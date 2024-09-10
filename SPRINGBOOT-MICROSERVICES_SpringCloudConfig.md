# Spring CLoud Config
 [Home](README.md)

Spring Cloud Config is Spring’s client/server approach for storing and serving distributed configurations across multiple applications and environments.

This configuration store is ideally versioned under Git version control and can be modified at application runtime. While it fits very well in Spring applications using all the supported configuration file formats together with constructs like Environment, PropertySource, or @Value, it can be used in any environment running any programming language.

In this tutorial, we’ll focus on how to set up a Git-backed config server, use it in a simple REST application server, and set up a secure environment including encrypted property values.

## Dependency 

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-config</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

## Config Server Implementation

The main part of the application is a config class, more specifically a @SpringBootApplication, which pulls in all the required setup through the auto-configure annotation @EnableConfigServer:

```java
@SpringBootApplication
@EnableConfigServer
public class ConfigServer {
    
    public static void main(String[] arguments) {
        SpringApplication.run(ConfigServer.class, arguments);
    }
}
```

We also need to set a username and password for the Basic-Authentication in our application.properties to avoid an auto-generated password on every application restart:

```ini
server.port=8888
spring.cloud.config.server.git.uri=ssh://localhost/config-repo
spring.cloud.config.server.git.clone-on-start=true
spring.security.user.name=root
spring.security.user.password=s3cr3t
```

## Git Repository as Configuration Storage

To complete our server, we have to initialize a Git repository under the configured url, create some new properties files, and populate them with some values.

The name of the configuration file is composed like a normal Spring application.properties, but instead of the word ‘application,’ a configured name, such as the value of the property ‘spring.application.name’, of the client is used, followed by a dash and the active profile. For example:

```sh
$> git init
$> echo 'user.role=Developer' > config-client-development.properties
$> echo 'user.role=User'      > config-client-production.properties
$> git add .
$> git commit -m 'Initial config-client properties'
```
## Querying the Configuration

Now we’re able to start our server. The Git-backed configuration API provided by our server can be queried using the following paths:

```
/{application}/{profile}[/{label}]
/{application}-{profile}.yml
/{label}/{application}-{profile}.yml
/{application}-{profile}.properties
/{label}/{application}-{profile}.properties
```

The {label} placeholder refers to a Git branch, {application} to the client’s application name, and the {profile} to the client’s current active application profile.

So we can retrieve the configuration for our planned config client running under the development profile in branch master via:

```sh
$> curl http://root:s3cr3t@localhost:8888/config-client/development/master
```

## The Client Implementation

Next, let’s take care of the client. This will be a very simple client application, consisting of a REST controller with one GET method.

To fetch our server, the configuration must be placed in the application.properties file. Spring Boot 2.4 introduced a new way to load configuration data using the spring.config.import property, which is now the default way to bind to Config Server:

```java
@SpringBootApplication
@RestController
public class ConfigClient {
    
    @Value("${user.role}")
    private String role;

    public static void main(String[] args) {
        SpringApplication.run(ConfigClient.class, args);
    }

    @GetMapping(
      value = "/whoami/{username}",  
      produces = MediaType.TEXT_PLAIN_VALUE)
    public String whoami(@PathVariable("username") String username) {
        return String.format("Hello! 
          You're %s and you'll become a(n) %s...\n", username, role);
    }
}
```

In addition to the application name, we also put the active profile and the connection-details in our application.properties:

```ini
spring.application.name=config-client
spring.profiles.active=development
spring.config.import=optional:configserver:http://root:s3cr3t@localhost:8888
```

This will connect to the Config Server at http://localhost:8888 and will also use HTTP basic security while initiating the connection. We can also set the username and password separately using spring.cloud.config.username and spring.cloud.config.password properties, respectively.

In some cases, we may want to fail the startup of a service if it isn’t able to connect to the Config Server. If this is the desired behavior, we can remove the optional: prefix to make the client halt with an exception.

To test if the configuration is properly received from our server, and the role value gets injected in our controller method, we simply curl it after booting the client:

```sh
$> curl http://localhost:8080/whoami/Mr_Pink
```

If the response is as follows, our Spring Cloud Config Server and its client are working fine for now:

```
Hello! You're Mr_Pink and you'll become a(n) Developer...
```

## CSRF

By default, Spring Security enables CSRF protection for all the requests sent to our application.

Therefore, to be able to use the /encrypt and /decrypt endpoints, let’s disable the CSRF for them:

```java
@Configuration
public class SecurityConfiguration {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.csrf(csrf -> csrf.ignoringRequestMatchers(
           "/encrypt/**", "/decrypt/**"
        ))

        //...
    }
}
```

## Key Management

By default, the config server is able to encrypt property values in a symmetric or asymmetric way.

__To use symmetric cryptography__, we simply have to set the property ‘encrypt.key’ in our application.properties to a secret of our choice. Alternatively, we can pass-in the environment variable ENCRYPT_KEY.

__For asymmetric cryptography__, we can set ‘encrypt.key’ to a PEM-encoded string value or configure a keystore to use.

Since we need a highly secured environment for our demo server, we’ll choose the latter option, along with generating a new keystore, including a RSA key-pair, with the Java keytool first:

```sh
$> keytool -genkeypair -alias config-server-key \
       -keyalg RSA -keysize 4096 -sigalg SHA512withRSA \
       -dname 'CN=Config Server,OU=Spring Cloud,O=Baeldung' \
       -keypass my-k34-s3cr3t -keystore config-server.jks \
       -storepass my-s70r3-s3cr3t
```

Then we’ll add the created keystore to our server’s application.properties and re-run it:

```ini
encrypt.keyStore.location=classpath:/config-server.jks
encrypt.keyStore.password=my-s70r3-s3cr3t
encrypt.keyStore.alias=config-server-key
encrypt.keyStore.secret=my-k34-s3cr3t
```

Next, we’ll query the encryption-endpoint, and add the response as a value to a configuration in our repository:

```sh
$> export PASSWORD=$(curl -X POST --data-urlencode d3v3L \
       http://root:s3cr3t@localhost:8888/encrypt)
$> echo "user.password={cipher}$PASSWORD" >> config-client-development.properties
$> git commit -am 'Added encrypted password'
$> curl -X POST http://root:s3cr3t@localhost:8888/refresh
```

To test if our setup works correctly, we’ll modify the ConfigClient class and restart our client:

```java
@SpringBootApplication
@RestController
public class ConfigClient {

    ...
    
    @Value("${user.password}")
    private String password;

    ...
    public String whoami(@PathVariable("username") String username) {
        return String.format("Hello! 
          You're %s and you'll become a(n) %s, " +
          "but only if your password is '%s'!\n", 
          username, role, password);
    }
}
```

Finally, a query against our client will show us if our configuration value is being correctly decrypted:
freestar

```sh
$> curl http://localhost:8080/whoami/Mr_Pink
Hello! You're Mr_Pink and you'll become a(n) Developer, \
  but only if your password is 'd3v3L'!
```

## Using Multiple Keys

If we want to use multiple keys for encryption and decryption, such as a dedicated one for each served application, we can add another prefix in the form of {name:value} between the {cipher} prefix and the BASE64-encoded property value.

The config server understands prefixes like {secret:my-crypto-secret} or {key:my-key-alias} almost out-of-the-box. The latter option needs a configured keystore in our application.properties. This keystore is searched for a matching key alias. For example:

```ini
user.password={cipher}{secret:my-499-s3cr3t}AgAMirj1DkQC0WjRv...
user.password={cipher}{key:config-client-key}AgAMirj1DkQC0WjRv...
```

For scenarios without keystore, we have to implement a @Bean of type TextEncryptorLocator, which handles the lookup and returns a TextEncryptor-Object for each key.

##  Serving Encrypted Properties

If we want to disable server-side cryptography and handle the decryption of property-values locally, we can put the following in our server’s application.properties:

```ini
spring.cloud.config.server.encrypt.enabled=false
```

Furthermore, we can delete all the other ‘encrypt.*’ properties to disable the REST endpoints.


Source :
[Link](https://www.baeldung.com/spring-cloud-configuration)
[Link](https://medium.com/@AlexanderObregon/a-beginners-guide-to-centralized-configuration-with-spring-cloud-config-6dfb6c70b5ad)

