# MockMVC
 [Home](README.md)

`MockMvc` and `Mockito` are both popular tools used in Java for testing, but they serve different purposes and are used in different contexts.

MockMVC

1. **Purpose:**
— `MockMvc` is a part of the Spring Test framework, specifically designed for testing Spring MVC applications.
— It allows you to test the behavior of your controllers in isolation.

2. **Usage:**
— It is used for testing the entire MVC stack, including controllers, filters, and other MVC components.
— `MockMvc` allows you to perform requests (GET, POST, PUT, DELETE) and validate the response.

3. **Integration:**
— It integrates well with Spring’s testing infrastructure and is typically used in conjunction with JUnit.

4. **Example:**

    ```java
    java
    mockMvc.perform(get("/api/users"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.name").value("John Doe"));
    ```

__Mockito__

1. **Purpose:**
— `Mockito` is a mocking framework used for creating and managing mock objects in unit tests.

2. **Usage:**
— It is used for testing individual units (like classes or methods) in isolation, particularly in unit tests.
— Mockito helps in simulating dependencies to focus on the behavior of the unit under test.

3. **Integration:**
— Mockito can be used with any testing framework, not limited to Spring.

4. **Example:**

```java
java
 // Creating a mock object
 UserRepository userRepositoryMock = mock(UserRepository.class);
// Setting up behavior of the mock object
 when(userRepositoryMock.findById(1L)).thenReturn(new User(1L, "John Doe"));
// Verifying interactions with the mock
 verify(userRepositoryMock).findById(1L);
```

Difference between MockMvc & Mockito

- `MockMvc` is used for testing Spring MVC applications, focusing on the behavior of controllers and the entire MVC stack.
- `Mockito` is used for creating mock objects to isolate the behavior of individual units (like classes or methods) in unit tests.
- While `MockMvc` is typically used for integration tests, `Mockito` is used for unit tests.
- Both tools can be used together in a testing suite to cover different aspects of testing (integration and unit testing).

In practice, you might use `MockMvc` to test the behavior of your controllers in conjunction with `Mockito` to mock the dependencies used by those controllers. This way, you can achieve comprehensive testing coverage for your application.

Explanation With An Example

Let’s create an example of a Spring Boot application with CRUD (Create, Read, Update, Delete) operations. We’ll then write both unit tests and integration tests for the controller and service layers.

### Example Application: Book Management System

Let’s assume we’re building a simple Book Management System. We have a `Book` entity with fields `id`, `title`, and `author`.

#### 1. Entity Class (`Book.java`):

```java
@Entity
public class Book {
 @Id
 @GeneratedValue(strategy = GenerationType.IDENTITY)
 private Long id;
 private String title;
 private String author;
 
 // Getters and setters
}
```

#### 2. Repository Interface (`BookRepository.java`):

```java
public interface BookRepository extends JpaRepository<Book, Long> {
}
```

#### 3. Service Class (`BookService.java`):

```java
@Service
public class BookService{
@Autowired
private BookRepository bookRepository;
public List<Book>getAllBooks(){return bookRepository.findAll();}
public Book getBookById(Long id){return bookRepository.findById(id).orElse(null);}
public Book saveBook(Book book){return bookRepository.save(book);}
public void deleteBook(Long id){return bookRepository.deleteById(id);}
}
```

#### 4. Controller Class (`BookController.java`):

```java
@RestController
@RequestMapping("/api/books")
public class BookController{
@Autowired
private BookService bookService;
@GetMapping
public List<Book> getAllBooks(){return bookService.getAllBooks();}
@GetMapping("/{id}")
public Book getBookById(@PathVariable Long id){return bookService.getBookById(id);}
@PostMapping
public Book createBook(@RequestBody Book book){return bookService.saveBook(book);}
@PutMapping("/{id}")
public Book updateBook(@PathVariable Long id, @RequestBody Book book){
Book existingBook = bookService.getBookById(id);
if(existingBook != null){
existingBook.setTitle(book.getTitle());
existingBook.setAuthor(book.getAuthor());
return bookService.saveBook(existingBook);
}
return null;
}
@DeleteMapping("/{id}")
public void deleteBook(@PathVariable Long id){return BookService.deleteBook(id);}
}
```

### Unit Tests

#### 1. Service Unit Tests (`BookServiceTest.java`):

```java
@ExtendWith(MockitoExtension.class)
public class BookServiceTest {

    @Mock
    private BookRepository bookRepository;

    @InjectMocks
    private BookService bookService;

    @Test
    public void testGetAllBooks() {
        // Mock data
        List<Book> books = Arrays.asList(
                new Book(1L, "Book 1", "Author 1"),
                new Book(2L, "Book 2", "Author 2")
        );

        // Define behavior of mock
        when(bookRepository.findAll()).thenReturn(books);

        // Test the service method
        List<Book> result = bookService.getAllBooks();

        // Assertions
        assertEquals(2, result.size());
    }

    @Test
    public void testGetBookById() {
        // Mock data
        Long id = 1L;
        Book book = new Book(id, "Book 1", "Author 1");

        // Define behavior of mock
        when(bookRepository.findById(id)).thenReturn(Optional.of(book));

        // Test the service method
        Book result = bookService.getBookById(id);

        // Assertions
        assertNotNull(result);
        assertEquals(id, result.getId());
    }

    @Test
    public void testSaveBook() {
        // Mock data
        Book bookToSave = new Book(null, "New Book", "New Author");
        Book savedBook = new Book(1L, "New Book", "New Author");

        // Define behavior of mock
        when(bookRepository.save(bookToSave)).thenReturn(savedBook);

        // Test the service method
        Book result = bookService.saveBook(bookToSave);

        // Assertions
        assertNotNull(result);
        assertEquals(savedBook.getId(), result.getId());
    }

    @Test
    public void testDeleteBook() {
        // Mock data
        Long id = 1L;

        // Test the service method
        bookService.deleteBook(id);

        // Verify that the delete method was called
        verify(bookRepository, times(1)).deleteById(id);
    }
}
```

### Integration Tests

#### 2. Controller Integration Tests (`BookControllerIntegrationTest.java`):

```java
@SpringBootTest
@AutoConfigureMockMvc
public class BookControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private BookRepository bookRepository;

    @Test
    public void testCreateBook() throws Exception {
        // Mock data
        Book bookToCreate = new Book(null, "New Book", "New Author");

        // Send POST request
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.post("/api/books")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(bookToCreate)))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andReturn();

        // Deserialize response
        Book createdBook = objectMapper.readValue(result.getResponse().getContentAsString(), Book.class);

        // Assertions
        assertNotNull(createdBook.getId());
        assertEquals(bookToCreate.getTitle(), createdBook.getTitle());
        assertEquals(bookToCreate.getAuthor(), createdBook.getAuthor());
    }

    @Test
    public void testUpdateBook() throws Exception {
        // Populate test data
        Book existingBook = bookRepository.save(new Book(null, "Existing Book", "Existing Author"));

        // Mock data
        Book updatedBook = new Book(existingBook.getId(), "Updated Book", "Updated Author");

        // Send PUT request
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.put("/api/books/{id}", existingBook.getId())
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updatedBook)))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andReturn();

        // Deserialize response
        Book modifiedBook = objectMapper.readValue(result.getResponse().getContentAsString(), Book.class);

        // Assertions
        assertEquals(existingBook.getId(), modifiedBook.getId());
        assertEquals(updatedBook.getTitle(), modifiedBook.getTitle());
        assertEquals(updatedBook.getAuthor(), modifiedBook.getAuthor());
    }

    @Test
    public void testDeleteBook() throws Exception {
        // Populate test data
        Book existingBook = bookRepository.save(new Book(null, "Existing Book", "Existing Author"));

        // Send DELETE request
        mockMvc.perform(MockMvcRequestBuilders.delete("/api/books/{id}", existingBook.getId()))
                .andExpect(MockMvcResultMatchers.status().isOk());

        // Verify that the book was deleted
        assertFalse(bookRepository.existsById(existingBook.getId()));
    }
}
```

### Running Tests

You can run the tests using your IDE or with Maven using the command `mvn test`.

These examples cover both unit tests for the service layer and integration tests for the controller layer. The controller tests use MockMvc to simulate HTTP requests and check the responses.

Please note that in a real-world scenario, you would want to use a test database or mock the database interactions to isolate the tests from the actual database. This example assumes the use of an H2 in-memory database for simplicity.