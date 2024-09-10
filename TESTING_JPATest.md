# Testing 
 [Home](README.md)

The @DataJpaTest annotation is used to test JPA repositories in Spring Boot applications. It’s a specialized test annotation that provides a minimal Spring context for testing the persistence layer. This annotation can be used in conjunction with other testing annotations like @RunWith and @SpringBootTest.

In addition, the scope of @DataJpaTest is limited to the JPA repository layer of the application. It doesn’t load the entire application context, which can make testing faster and more focused. This annotation also provides a pre-configured EntityManager and TestEntityManager for testing JPA entities.

## properties

This parameter allows us to specify Spring Boot configuration properties that will be applied to our test context. This can be useful for adjusting settings like database connection details, transaction behavior, or other application properties relevant to our testing needs:

```java
@DataJpaTest(properties = {
    "spring.datasource.url=jdbc:h2:mem:testdb",
    "spring.jpa.hibernate.ddl-auto=create-drop"
})
public class UserRepositoryTest {
    // ... test methods
}
```

## showSql

This enables SQL logging for our tests and allows us to see the actual SQL queries executed by the repository methods. Moreover, this can help debug or understand how the JPA queries are translated. By default, the SQL logging is enabled. We can turn it off by setting the value to false:

```java
@DataJpaTest(showSql = false)
public class UserRepositoryTest {
    // ... test methods
}
```

## includeFilters and excludeFilters

These parameters enable us to include or exclude specific components during component scanning. We can use them to narrow down the scanning scope and optimize test performance by focusing only on the relevant components:

```java
@DataJpaTest(includeFilters = @ComponentScan.Filter(
    type = FilterType.ASSIGNABLE_TYPE, 
    classes = UserRepository.class),
  excludeFilters = @ComponentScan.Filter(
    type = FilterType.ASSIGNABLE_TYPE, 
    classes = SomeIrrelevantRepository.class))
public class UserRepositoryTest {
    // ... test methods
}
```

## Test Environment Configuration

Setting up a proper test environment for JPA repositories can be time-consuming and tricky. @DataJpaTest provides a ready-made testing environment that includes essential components for testing JPA repositories, such as the EntityManager and DataSource.

This environment is specifically designed for testing JPA repositories. It ensures that our repository methods run within the context of a test transaction, interacting with a safe, in-memory database like H2 instead of the production database.

### Setting up the Test Class

To begin, let’s set up the test class by annotating it with @DataJpaTest. This annotation scans for entity classes annotated with @Entity and Spring Data JPA repositories interfaces. This ensures that only relevant components are loaded for testing, improving test focus and performance:
freestar

```java
@DataJpaTest
public class UserRepositoryTest {
    // Add test methods here
}

To create a repository test case, we first need to inject the repository that we want to test into our test class. This can be done using the @Autowired annotation:

@Autowired
private UserRepository userRepository;
```

### Test Lifecycle Management

In the context of test lifecycle management, @BeforeEach and @AfterEach annotations are used to perform setup and teardown operations before and after each test method, respectively. This ensures that each test method runs in a clean and isolated environment, with consistent initial conditions and cleanup procedures.

Here’s how we can incorporate test lifecycle management into our test class:

```java
private User testUser;

@BeforeEach
public void setUp() {
    // Initialize test data before each test method
    testUser = new User();
    testUser.setUsername("testuser");
    testUser.setPassword("password");
    userRepository.save(testUser);
}

@AfterEach
public void tearDown() {
    // Release test data after each test method
    userRepository.delete(testUser);
}
```

In the setUp() method annotated with @BeforeEach, we can perform any necessary setup operations required before each test method execution. This might include initializing test data, setting up mock objects, or preparing resources needed for the test.

Conversely, in the tearDown() method annotated with @AfterEach, we can perform cleanup operations after each test method execution. This might involve resetting any changes made during the test, releasing resources, or performing any necessary cleanup tasks to restore the test environment to its original state.

### Testing the Insertion Operation

Now, we can write test methods that interact with the JPA repository. For example, we might want to test that we can save a new user to the database. Since a user is automatically saved before each test, we can directly focus on testing interactions with the JPA repository:

```java
@Test
void givenUser_whenSaved_thenCanBeFoundById() {
    User savedUser = userRepository.findById(testUser.getId()).orElse(null);
    assertNotNull(savedUser);
    assertEquals(testUser.getUsername(), savedUser.getUsername());
    assertEquals(testUser.getPassword(), savedUser.getPassword());
}
```

If we observe the console log for the test case, we’ll notice the following logs:

```
Began transaction (1) for test context  
.....

Rolled back transaction for test:  

These logs indicate that the @BeforeEach and @AfterEach methods are functioning as expected.
freestar
6.4. Testing the Update Operation
```

In addition, we can create a test case for testing the update operation:

```java
@Test
void givenUser_whenUpdated_thenCanBeFoundByIdWithUpdatedData() {
    testUser.setUsername("updatedUsername");
    userRepository.save(testUser);

    User updatedUser = userRepository.findById(testUser.getId()).orElse(null);

    assertNotNull(updatedUser);
    assertEquals("updatedUsername", updatedUser.getUsername());
}
```

### Testing the findByUsername() Method

Now, let’s test the findByUsername() custom query method we created:

```java
@Test
void givenUser_whenFindByUsernameCalled_thenUserIsFound() {
    User foundUser = userRepository.findByUsername("testuser");

    assertNotNull(foundUser);
    assertEquals("testuser", foundUser.getUsername());
}
```
## Transactional Behavior

By default, all tests annotated with @DataJpaTest are executed within a transaction. This means that any changes made to the database during the test are rolled back at the end of the test, ensuring that the database is left in its original state. This default behavior simplifies testing by preventing interference between tests and data corruption.

However, there may be cases where we need to disable transactional behavior to test certain scenarios. For instance, testing results may need to persist beyond the test.

In such a case, we can disable transactions for a specific test class using the @Transactional annotation with propagation = propagation.NOT_SUPPORTED:

```java
@DataJpaTest
@Transactional(propagation = Propagation.NOT_SUPPORTED)
public class UserRepositoryIntegrationTest {
    // ... test methods
}
```

Or we can disable transactions for an individual test method:

```java
@Test
@Transactional(propagation = Propagation.NOT_SUPPORTED)
public void testMyMethodWithoutTransactions() {
    // ... code that modifies the database
}
```

Source :

[Link](https://www.baeldung.com/junit-datajpatest-repository)