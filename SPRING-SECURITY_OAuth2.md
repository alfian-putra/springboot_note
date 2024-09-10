# SPring OAuth2
 [Home](README.md)

OAuth 2.0 is an authorization framework that enables third-party applications to access protected resources on behalf of a user without requiring the user’s credentials. This is achieved through the use of access tokens, which are issued by an OAuth provider and used by third-party applications to access the user’s resources.

## Add Dependency

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-client</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-oauth2-jose</artifactId>
</dependency>
```
## Configure

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .authorizeRequests()
                .antMatchers("/oauth2/**", "/login/**", "/logout/**")
                .permitAll()
                .anyRequest()
                .authenticated()
                .and()
            .oauth2Login()
                .loginPage("/login")
                .defaultSuccessURL("/home")
                .and()
            .logout()
                .logoutSuccessUrl("/")
                .logoutUrl("/logout")
                .and()
            .csrf().disable();
    }

}
```

## Generate Token

```java
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.jwt.JwtBuilder;
import org.springframework.security.oauth2.jwt.Jwts;
import org.springframework.security.oauth2.jwt.NimbusJwtEncoder;

import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.time.Instant;
import java.util.Date;

public class TokenGenerator {

    public static void main(String[] args) throws NoSuchAlgorithmException {
        // Generate a key pair
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("RSA");
        keyPairGenerator.initialize(2048);
        KeyPair keyPair = keyPairGenerator.generateKeyPair();

        // Build the JWT
        JwtBuilder jwtBuilder = Jwts.builder()
                .setIssuer("https://example.com")
                .setAudience("https://example.com/resources")
                .setId("123")
                .setSubject("user@example.com")
                .setExpiration(Date.from(Instant.now().plusSeconds(3600)))
                .setIssuedAt(new Date())
                .signWith(new NimbusJwtEncoder(keyPair.getPrivate()));

        Jwt jwt = jwtBuilder.build();
        System.out.println(jwt.getTokenValue());
    }

}
```

## OAuth2 Client

```ini
spring.security.oauth2.client.registration.example.client-id=client-id
spring.security.oauth2.client.registration.example.client-secret=client-secret
spring.security.oauth2.client.registration.example.scope=read,write
spring.security.oauth2.client.registration.example.redirect-uri=http://localhost:8080/login/oauth2/code/example
spring.security.oauth2.client.provider.example.authorization-uri=https://example.com/oauth2/authorize
spring.security.oauth2.client.provider.example.token-uri=https://example.com/oauth2/token
spring.security.oauth2.client.provider.example.user-info-uri=https://example.com/userinfo
spring.security.oauth2.client.provider.example.user-name-attribute=name
```

## Use Token

```java
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

public class ResourceClient {

    public static void main(String[] args) {
        // Create a RestTemplate
        RestTemplate restTemplate = new RestTemplate();

        // Set the authorization header
        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth("token");

        // Make the request
        HttpEntity<String> entity = new HttpEntity<>(headers);
        ResponseEntity<String> response = restTemplate.exchange(
                "https://example.com/resource",
                HttpMethod.GET,
                entity,
                String.class
        );

        // Print the response body
        System.out.println(response.getBody());
    }

}
```

## Protect Endpoint

```java
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MyController {

    @GetMapping("/admin")
    @PreAuthorize("hasRole('ADMIN')")
    public String adminEndpoint() {
        return "Hello, admin!";
    }

}
```

Source :
[Link 1](https://medium.com/@bubu.tripathy/oauth-2-using-spring-boot-99c17292f228)