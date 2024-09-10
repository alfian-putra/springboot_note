# Java Persistance API (JPA)
 [Home](README.md)

Spring Data JPA or JPA stands for Java Persistence API, so before looking into that, we must know about ORM (Object Relation Mapping). So Object relation mapping is simply the process of persisting any java object directly into a database table. Usually, the name of the object being persisted becomes the name of the table, and each field within that object becomes a column. With the table setup, each row corresponds to a record in the application. Hibernate is one example of ORM. In short, JPA is the interface while hibernate is the implementation. 

The java persistence API provides a specification for persisting, reading, and managing data from your java object to your relational tables in the database. JPA specifies the set of rules and guidelines for developing interfaces that follow standards. Straight to the point: JPA is just guidelines to implement ORM and there is no underlying code for the implementation. Spring Data JPA is part of the spring framework. The goal of spring data repository abstraction is to significantly reduce the amount of boilerplate code required to implement a data access layer for various persistence stores. Spring Data JPA is not a JPA provider, it is a library/framework that adds an extra layer of abstraction on the top of our JPA provider line Hibernate. 

The implementation of JPA cannot be separated from Hibernate or another implementer, there is an information from StackOverflow :

"
*You are right JPA is a specification. Hibernate, and EclipseLink are a couple of its implementations.*

*You have to specify the persistence provider(Hibernate, EclipseLink) in order to use the JPA implementation. The persistence providers have the implementation classes for JPA specifications.*
"

Source :

[Link](https://www.geeksforgeeks.org/spring-boot-spring-data-jpa/)

[Link](https://stackoverflow.com/questions/15487631/can-we-use-jpa-without-hibernate)