# JSON Web Token (JWT)
 [Home](README.md)


JSON Web Token or JWT, as it is more commonly called, is an open Internet standard (RFC 7519) for securely transmitting trusted information between parties in a compact way. The tokens contain claims that are encoded as a JSON object and are digitally signed using a private secret or a public key/private key pair. They are self-contained and verifiable as they are digitally signed. JWT’s can be signed and/or encrypted. The signed tokens verify the integrity of the claims contained in the token, while the encrypted ones hide the claims from other parties.

JWT's can also be used for the exchange of information though they more commonly used for authorization as they offer a lot of advantages over session management using in-memory random tokens. The biggest of them being the enabling the delegation of authentication logic to a third-party server like AuthO etc.

A JWT token is divided into 3 parts namely – header, payload, and signature in the format of

```
[Header].[Payload].[Signature]
```

---

- __Header__ 

The Header of a JWT token contains the list cryptographic operations that are applied to the JWT. This can be the signing technique, metadata information about the content-type and so on. The header is presented as a JSON object which is encoded to a base64URL. An example of a valid JWT header would be
```json
{ "alg": "HS256", "typ": "JWT" }
```
Here, "alg" gives us information about the type of algorithm used and "typ gives us the type of the information.

- __Payload__ 

The payload part of JWT contains the actual data to be transferred using the token. This part is also known as the "claims" part of the JWT token. The claims can be of three types – registered, public and private.

Example of a payload object could be.

```json
{ "sub": "12345", "name": "Johnny Hill", "admin": false }
```

- __Signature__ 

The signature part of the JWT is used for the verification that the message wasn’t changed along the way. If the tokens are signed with private key, it also verifies that the sender is who it says it is. It is created using the encoded header, encoded payload, a secret and the algorithm specified in the header. An example of a signature would be.

```java
HMACSHA256( base64UrlEncode(header) + "." + base64UrlEncode(payload), secret)
```
If we put the header, payload and signature we get a token as given below.

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6I
kpvaG4gRG9lIiwiYWRtaW4iOmZhbHNlfQ.gWDlJdpCTIHVYKkJSfAVNUn0ZkAjMxskDDm-5Fhe
WJ7xXgW8k5CllcGk4C9qPrfa1GdqfBrbX_1x1E39JY8BYLobAfAg1fs_Ky8Z7U1oCl6HL63yJq_
wVNBHp49hWzg3-ERxkqiuTv0tIuDOasIdZ5FtBdtIP5LM9Oc1tsuMXQXCGR8GqGf1Hl2qv8MCyn
NZJuVdJKO_L3WGBJouaTpK1u2SEleVFGI2HFvrX_jS2ySzDxoO9KjbydK0LNv_zOI7kWv-gAmA
j-v0mHdJrLbxD7LcZJEGRScCSyITzo6Z59_jG_97oNLFgBKJbh12nvvPibHpUYWmZuHkoGvuy5RLUA
```

## JWT on Springboot

__JWT Secret__

The JWT includes a secret which we will define in our application.properties file as given below.
application.properties

```ini
spring.application.name=formlogin
secret=somerandomsecretsomerandomsecretsomerandomsecretsomerandomsecret
```

__TokenManager.java__

```java
package com.tutorialspoint.security.formlogin.jwtutils;

import java.security.Key;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;

@Component
public class TokenManager {

   private static final long serialVersionUID = 7008375124389347049L; 
   public static final long TOKEN_VALIDITY = 10 * 60 * 60; 

   @Value("${secret}") 
   private String jwtSecret; 

   // Generates a token on successful authentication by the user 
   // using username, issue date of token and the expiration date of the token.
   public String generateJwtToken(UserDetails userDetails) { 
      Map<String, Object> claims = new HashMap<>(); 
      return Jwts
         .builder()
         .setClaims(claims)  // set the claims
         .setSubject(userDetails.getUsername())  // set the username as subject in payload
         .setIssuedAt(new Date(System.currentTimeMillis()))
         .setExpiration(new Date(System.currentTimeMillis() + TOKEN_VALIDITY * 1000))
         .signWith(getKey(), SignatureAlgorithm.HS256)  // signature part
         .compact();
   }

   // Validates the token 
   // Checks if user is an authenticatic one and using the token is the one that was generated and sent to the user. 
   // Token is parsed for the claims such as username, roles, authorities, validity period etc.
   public Boolean validateJwtToken(String token, UserDetails userDetails) { 
      final String username = getUsernameFromToken(token);
      final Claims claims = Jwts
         .parserBuilder()
         .setSigningKey(getKey())
         .build()
         .parseClaimsJws(token).getBody(); 
      Boolean isTokenExpired = claims.getExpiration().before(new Date());
      return (username.equals(userDetails.getUsername())) && !isTokenExpired;
   }

   // get the username by checking subject of JWT Token
   public String getUsernameFromToken(String token) {
      final Claims claims = Jwts
         .parserBuilder()
         .setSigningKey(getKey())
         .build()
         .parseClaimsJws(token).getBody(); 
      return claims.getSubject(); 
   }
   
   // create a signing key based on secret
   private Key getKey() {
      byte[] keyBytes = Decoders.BASE64.decode(jwtSecret);		
      Key key = Keys.hmacShaKeyFor(keyBytes);
      return key;
   }
}
```

__JwtUserDetailsService.java__

```java
package com.tutorialspoint.security.formlogin.jwtutils;

import java.util.ArrayList; 
import org.springframework.security.core.userdetails.User; 
import org.springframework.security.core.userdetails.UserDetails; 
import org.springframework.security.core.userdetails.UserDetailsService; 
import org.springframework.security.core.userdetails.UsernameNotFoundException; 
import org.springframework.stereotype.Service; 

@Service
public class JwtUserDetailsService implements UserDetailsService { 
   @Override 
   public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
      // create a user for "randomuser123"/"password".
      if ("randomuser123".equals(username)) { 
         return new User("randomuser123", // username
            "$2a$10$slYQmyNdGzTn7ZLBXBChFOC9f6kFjAqPhccnP6DxlWXx2lPk1C3G6", // encoded password
            new ArrayList<>()); 
      } else { 
         throw new UsernameNotFoundException("User not found with username: " + username); 
      } 
   } 
}
```

Now it’s time we created our Filter. The filter class will be used to track our requests and detect if they contain the valid token in the header. If the token is valid we let the request proceed otherwise we send a 401 error (Unauthorized).

__JwtFilter.java__

```java
package com.tutorialspoint.security.formlogin.jwtutils;

import java.io.IOException;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import io.jsonwebtoken.ExpiredJwtException;


// filter to run for every request
@Component
public class JwtFilter extends OncePerRequestFilter {
   @Autowired
   private JwtUserDetailsService userDetailsService;
   @Autowired
   private TokenManager tokenManager;
   @Override
   protected void doFilterInternal(HttpServletRequest request,
      HttpServletResponse response, FilterChain filterChain)
      throws ServletException, IOException {

      String tokenHeader = request.getHeader("Authorization");
      String username = null;
      String token = null;
      // if bearer token is provided, get the username 	  
      if (tokenHeader != null && tokenHeader.startsWith("Bearer ")) {
         token = tokenHeader.substring(7);
         try {
            username = tokenManager.getUsernameFromToken(token);
         } catch (IllegalArgumentException e) {
            System.out.println("Unable to get JWT Token");
         } catch (ExpiredJwtException e) {
            System.out.println("JWT Token has expired");
         }
      } else {
         System.out.println("Bearer String not found in token");
      }
      // validate the JWT Token and create a new authentication token and set in security context	  
      if (null != username && SecurityContextHolder.getContext().getAuthentication() == null) {
         UserDetails userDetails = userDetailsService.loadUserByUsername(username);
         if (tokenManager.validateJwtToken(token, userDetails)) {
            UsernamePasswordAuthenticationToken
               authenticationToken = new UsernamePasswordAuthenticationToken(
                  userDetails, null, userDetails.getAuthorities());
               authenticationToken.setDetails(new
                  WebAuthenticationDetailsSource().buildDetails(request));
            SecurityContextHolder.getContext().setAuthentication(authenticationToken);
         }
      }
      filterChain.doFilter(request, response);
   }
}
```

Having created the filter for our requests, we now create the JwtAutheticationEntryPoint class. This class extends Spring’s AuthenticationEntryPoint class and rejects every unauthenticated request with an error code 401 sent back to the client. We have overridden the commence() method of AuthenticationEntryPoint class to do that.

__JwtAuthenticationEntryPoint.java__

```java
package com.tutorialspoint.security.formlogin.jwtutils;

import java.io.IOException;
import java.io.Serializable;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.stereotype.Component;

@Component
public class JwtAuthenticationEntryPoint implements AuthenticationEntryPoint, Serializable {

   private static final long serialVersionUID = 1L;

   @Override
   public void commence(HttpServletRequest request, HttpServletResponse response, 
      AuthenticationException authException) throws IOException, ServletException {
      response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Unauthorized");
   }
}
```
Next, we create classes for our Request and Response models under package models. These models determine how our request and response formats would be for authentication.

__JwtRequestModel.java__

```java
package com.tutorialspoint.security.formlogin.jwtutils.models;

import java.io.Serializable; 
public class JwtRequestModel implements Serializable { 
   /** 
   * 
   */ 
   private static final long serialVersionUID = 2636936156391265891L; 
   private String username; 
   private String password; 
   public JwtRequestModel() { 
   } 
   public JwtRequestModel(String username, String password) { 
      super(); 
      this.username = username; this.password = password; 
   } 
   public String getUsername() { 
      return username;
   } 
   public void setUsername(String username) { 
      this.username = username; 
   } 
   public String getPassword() { 
      return password; 
   } 
   public void setPassword(String password) { 
      this.password = password; 
   } 
}
```

__JwtResponseModel.java__

```java
package com.tutorialspoint.security.formlogin.jwtutils.models;

import java.io.Serializable; 
public class JwtRequestModel implements Serializable { 
   /** 
   * 
   */ 
   private static final long serialVersionUID = 2636936156391265891L; 
   private String username; 
   private String password; 
   public JwtRequestModel() { 
   } 
   public JwtRequestModel(String username, String password) { 
      super(); 
      this.username = username; this.password = password; 
   } 
   public String getUsername() { 
      return username;
   } 
   public void setUsername(String username) { 
      this.username = username; 
   } 
   public String getPassword() { 
      return password; 
   } 
   public void setPassword(String password) { 
      this.password = password; 
   } 
}
```

__JwtController.java__

```java
package com.tutorialspoint.security.formlogin.jwtutils;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.DisabledException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.tutorialspoint.security.formlogin.jwtutils.models.JwtRequestModel;
import com.tutorialspoint.security.formlogin.jwtutils.models.JwtResponseModel;

@RestController
@CrossOrigin
public class JwtController {
   @Autowired
   private JwtUserDetailsService userDetailsService;
   @Autowired
   private AuthenticationManager authenticationManager;
   @Autowired
   private TokenManager tokenManager;
   
   // Get a JWT Token once user is authenticated, otherwise throw BadCredentialsException
   @PostMapping("/login")
   public ResponseEntity<JwtResponseModel> createToken(@RequestBody JwtRequestModel
      request) throws Exception {
      try {
         authenticationManager.authenticate(
            new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword()));
      } catch (DisabledException e) {
         throw new Exception("USER_DISABLED", e);
      } catch (BadCredentialsException e) {
         throw new Exception("INVALID_CREDENTIALS", e);
      }
      final UserDetails userDetails = userDetailsService.loadUserByUsername(request.getUsername());
      final String jwtToken = tokenManager.generateJwtToken(userDetails);
      return ResponseEntity.ok(new JwtResponseModel(jwtToken));
   }
}

```

__Spring Security Configuration Class__

Inside of our config package, we have created the WebSecurityConfig class. We shall be using this class for our security configurations, so let's annotate it with an @Configuration annotation and @EnableWebSecurity. As a result, Spring Security knows to treat this class a configuration class. As we can see, configuring applications have been made very easy by Spring.

__WebSecurityConfig__

```java
package com.tutorialspoint.security.formlogin.config; 

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

import com.tutorialspoint.security.formlogin.jwtutils.JwtAuthenticationEntryPoint;
import com.tutorialspoint.security.formlogin.jwtutils.JwtFilter; 

@Configuration 
@EnableWebSecurity
public class WebSecurityConfig {

   @Autowired
   private JwtAuthenticationEntryPoint authenticationEntryPoint;
   @Autowired
   private JwtFilter filter;

   @Bean 
   protected PasswordEncoder passwordEncoder() { 
      return new BCryptPasswordEncoder(); 
   }

   @Bean
   protected SecurityFilterChain filterChain(HttpSecurity http) throws Exception { 
      return http
         .csrf(AbstractHttpConfigurer::disable)
         .authorizeHttpRequests(request -> request.requestMatchers("/login").permitAll()
         .anyRequest().authenticated())
         // Send a 401 error response if user is not authentic.		 
         .exceptionHandling(exception -> exception.authenticationEntryPoint(authenticationEntryPoint))
         // no session management
         .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS)) 
         // filter the request and add authentication token		 
         .addFilterBefore(filter,  UsernamePasswordAuthenticationFilter.class)
         .build();
   }

   @Bean
   AuthenticationManager customAuthenticationManager() {
      return authentication -> new UsernamePasswordAuthenticationToken("randomuser123","password");
   }
}
```

__Controller Class : HelloController__


```java
package com.tutorialspoint.security.formlogin.controllers;

import org.springframework.web.bind.annotation.GetMapping; 
import org.springframework.web.bind.annotation.RestController; 

@RestController 
public class HelloController {
   @GetMapping("/hello") 
   public String hello() { 
      return "hello"; 
   } 
}
```

Source :

[Link](https://www.tutorialspoint.com/spring_security/spring_security_with_jwt.htm)