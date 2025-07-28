import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ContactTest {

    @Test
    public void testContactCreationValid() {
        Contact contact = new Contact("1", "John", "Doe", "1234567890", "123 Street");
        assertEquals("John", contact.getFirstName());
        assertEquals("Doe", contact.getLastName());
        assertEquals("1234567890", contact.getPhone());
        assertEquals("123 Street", contact.getAddress());
    }

    @Test
    public void testInvalidIdTooLong() {
        assertThrows(IllegalArgumentException.class, () -> {
            new Contact("12345678901", "John", "Doe", "1234567890", "123 Street");
        });
    }

    @Test
    public void testInvalidPhoneLength() {
        assertThrows(IllegalArgumentException.class, () -> {
            new Contact("1", "John", "Doe", "1234", "123 Street");
        });
    }

    @Test
    public void testSetInvalidFirstName() {
        Contact contact = new Contact("1", "John", "Doe", "1234567890", "123 Street");
        assertThrows(IllegalArgumentException.class, () -> {
            contact.setFirstName(null);
        });
        assertThrows(IllegalArgumentException.class, () -> {
            contact.setFirstName("ThisNameIsWayTooLong");
        });
    }
}
