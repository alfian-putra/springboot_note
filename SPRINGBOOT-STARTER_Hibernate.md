# Hibernate
 [Home](README.md)

ORM frameworks like Hibernate introduce runtime overhead in translating between object-oriented and relational models, impacting performance in high-throughput scenarios. Complex scenarios may involve intricate configurations, especially in dealing with advanced caching strategies or complex database structures.

## Hibernate Setup and Configuration with Spring Boot

__Dependency__

```xml
<dependencies> <!-- Includes Spring Boot Starter Data JPA, Hibernate --> 
<dependency> <groupId>org.springframework.boot</groupId> 
<artifactId>spring-boot-starter-data-jpa</artifactId> </dependency> 
</dependencies>
```

## Annotation

__@Entity__ 

This annotation indicates that a class is a Hibernate entity class. So, this class will be associated with a database table.

```java
@Entity
public class Product {
//…  }
```
__@Table__
This annotation indicates which database table an entity corresponds to. If you do not specify the table name, the class name is used by default.
```java
@Entity
@Table(name = "products")
public class Product {
//… }
```

__@Id__ and __@GeneratedValue__
These annotations indicate what a property is a primary key and how to create it. Strategy can be specified with @GeneratedValue (IDENTITY, SEQUENCE, AUTO etc.).
```java
@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)
private Long id;
```

__@Column__
This annotation specifies the name, type and other properties of a field’s (property) column in the database.
```java
@Column(name = "product_name", nullable = false, length = 100)
private String productName;
```


## Relationship Annotation

__@ManyToOne__ and __@OneToMany__
```java
@ManyToOne
@JoinColumn(name = "category_id") private Category category;
@OneToMany(mappedBy = "category")
private List<Product> products;
```

__@OneToOne__
```java
@OneToOne
@JoinColumn(name = "customer_id")
private Customer customer;
```

__@ManyToMany__
```java
@ManyToMany
@JoinTable( name = "order_product", joinColumns =@JoinColumn(name = "order_id"),
             inverseJoinColumns = @JoinColumn(name = "product_id") )
private List<Product> products;
```

Source :
[Link](https://medium.com/@utkuyavuzX/hibernate-and-spring-boot-a-detailed-guide-for-powerful-database-operations-7b8f6f2839d3)